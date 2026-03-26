"""
优化版 OpenAI Provider - 融合新架构
- 使用 PromptManager 管理 Prompt
- 单次调用生成（减少 API 成本）
- 保持降级容错能力
- 集成增强器（经历挖掘、个性化、ATS优化）
"""
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI

from app.services.ai.base import AIProviderBase
from app.services.ai.prompts.manager import PromptManager, load_prompt
from app.services.ai.enhancers import (
    ExperienceMiner,
    PersonalizationEngine,
    ATSOptimizer,
    UserProfile,
    create_personalization
)


class OpenAIProviderV2(AIProviderBase):
    """
    优化版 OpenAI Provider
    
    改进点：
    1. 使用 PromptManager 分层管理 Prompt
    2. 单次 LLM 调用生成简历（成本降低 66%）
    3. 内置质量验证层
    4. 支持 Few-shot 示例注入
    5. 集成增强器：经历挖掘、个性化、ATS优化
    """

    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)
        self.prompt_manager = PromptManager()
        
        # 初始化增强器
        self.experience_miner = ExperienceMiner(self)
        self.personalization = PersonalizationEngine(self)
        self.ats_optimizer = ATSOptimizer()

    async def generate_resume_content(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        style: str = "professional",
        language: str = "zh",
        user_profile: Optional[UserProfile] = None,
        job_description: Optional[str] = None,
        enhance: bool = True
    ) -> Dict[str, Any]:
        """
        生成简历内容 - 增强版（单次调用）
        
        Args:
            user_info: 用户信息
            target_position: 目标岗位
            style: 风格
            language: 语言
            user_profile: 用户画像（可选，用于个性化）
            job_description: 职位描述（可选，用于ATS优化）
            enhance: 是否启用增强功能
        
        Returns:
            生成的简历内容，包含增强信息
        """
        if not self.client:
            return self._generate_mock_content(user_info, target_position)

        try:
            # 步骤1: 经历挖掘（如果启用）
            if enhance and user_info.get("work_experience"):
                user_info = await self._enhance_experiences(user_info)
            
            # 步骤2: 个性化策略
            strategy = None
            if enhance and user_profile:
                strategy = self.personalization.create_strategy(user_profile)
                if job_description:
                    strategy = await self.personalization.enhance_with_jd(
                        strategy, job_description
                    )
            
            # 步骤3: ATS 预分析
            ats_preview = None
            if enhance and job_description:
                ats_preview = self.ats_optimizer.extract_jd_keywords(job_description)
            
            # 步骤4: 构建增强版 Prompt
            prompt = self._build_enhanced_prompt(
                user_info=user_info,
                target_position=target_position,
                style=style,
                strategy=strategy,
                ats_keywords=ats_preview
            )
            
            # 步骤5: 单次 LLM 调用
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            content = json.loads(response.choices[0].message.content)
            
            # 步骤6: 质量验证
            validated_content = self._validate_and_fix(content, user_info)
            
            # 步骤7: ATS 后检查（如果启用）
            ats_result = None
            if enhance and job_description:
                ats_result = self.ats_optimizer.analyze_match_score(
                    validated_content,
                    {"hard_skills": ats_preview.get("hard_skills", [])}
                )
            
            # 构建最终响应
            result = {
                "content": validated_content,
                "meta": {
                    "provider": "openai_v2",
                    "model": self.model,
                    "enhanced": enhance
                }
            }
            
            if strategy:
                result["meta"]["strategy"] = {
                    "angle": strategy.angle,
                    "keywords": strategy.keywords_emphasis
                }
            
            if ats_result:
                result["meta"]["ats_score"] = ats_result["overall_score"]
                result["meta"]["ats_suggestions"] = ats_result["suggestions"]
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"[WARN] JSON parse error: {e}")
            return {"content": self._build_fallback_content(user_info), "error": "parse_error"}
        except Exception as e:
            print(f"[WARN] Generation failed: {e}")
            return await self._generate_simplified(user_info, target_position, language)

    def _validate_and_fix(
        self,
        content: Dict[str, Any],
        user_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        质量验证和自动修复
        
        检查项：
        1. 关键字段是否存在
        2. 工作经历是否包含量化数据
        3. 技能列表是否为空
        """
        required_fields = ["basic_info", "education", "work_experience", "projects", "skills"]
        
        # 修复缺失字段
        for field in required_fields:
            if field not in content or not content[field]:
                content[field] = user_info.get(field, [])
        
        # 验证工作经历质量
        for exp in content.get("work_experience", []):
            description = exp.get("description", "")
            # 检查是否包含数字
            if not any(c.isdigit() for c in description):
                # 标记需要优化
                exp["_needs_quantify"] = True
        
        return content

    # ========== 增强器集成方法 ==========
    
    async def _enhance_experiences(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """增强工作经历描述"""
        enhanced = user_info.copy()
        work_exps = enhanced.get("work_experience", [])
        
        for i, exp in enumerate(work_exps):
            if not exp.get("description") or len(exp.get("description", "")) < 50:
                # 描述太简单，尝试挖掘
                try:
                    mined = await self.experience_miner.mine_experience(
                        title=exp.get("position", ""),
                        company=exp.get("company", ""),
                        description=exp.get("description", ""),
                        period=exp.get("period", "")
                    )
                    
                    # 生成 STAR 描述
                    star_desc = self.experience_miner.generate_star_description(mined)
                    if star_desc:
                        work_exps[i]["description"] = star_desc
                        work_exps[i]["_enhanced"] = True
                        
                except Exception as e:
                    print(f"[WARN] Experience enhancement failed: {e}")
        
        enhanced["work_experience"] = work_exps
        return enhanced
    
    def _build_enhanced_prompt(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        style: str,
        strategy: Optional[Any],
        ats_keywords: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """构建增强版 Prompt"""
        
        # 系统 Prompt
        if strategy:
            system_prompt = self.personalization.generate_system_prompt(strategy)
        else:
            system_prompt = self.prompt_manager.system("resume_expert_v1").build()["system"]
        
        # 添加 ATS 关键词提示
        if ats_keywords:
            key_skills = ", ".join(ats_keywords.get("hard_skills", [])[:10])
            system_prompt += f"\n\n【JD 关键技能】请在简历中自然融入以下技能关键词：{key_skills}"
        
        # 用户 Prompt
        user_prompt_parts = [
            f"用户信息: {json.dumps(user_info, ensure_ascii=False)}",
            f"目标岗位: {target_position}",
            f"风格要求: {style}"
        ]
        
        if strategy:
            user_prompt_parts.append(f"\n内容角度: {strategy.angle}")
            user_prompt_parts.append(f"重点关键词: {', '.join(strategy.keywords_emphasis[:8])}")
        
        user_prompt = "\n".join(user_prompt_parts)
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
    
    async def analyze_resume_with_jd(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """分析简历与 JD 的匹配度（增强版）"""
        return self.ats_optimizer.optimize_for_ats(resume_content, job_description)

    async def _generate_simplified(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        language: str
    ) -> Dict[str, Any]:
        """简化版生成（降级策略）"""
        if not self.client:
            return self._generate_mock_content(user_info, target_position)
        
        try:
            prompt = load_prompt(
                "resume_expert",
                "generate/full_resume",
                user_info=user_info,
                target_position=target_position,
                style="professional"
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.7,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"[ERROR] Simplified generation failed: {e}")
            return self._build_fallback_content(user_info)

    async def optimize_content(
        self,
        original: str,
        optimization_type: str,
        context: Optional[str] = None
    ) -> str:
        """优化内容"""
        if not self.client:
            return self._mock_optimize(original, optimization_type)

        prompt_map = {
            "star_method": ("optimizer", "optimize/star_method"),
            "quantify": ("optimizer", "optimize/quantify"),
            "keywords": ("optimizer", "optimize/keywords"),
            "polish": ("optimizer", "optimize/polish")
        }
        
        system_name, task_path = prompt_map.get(
            optimization_type, 
            ("optimizer", "optimize/polish")
        )
        
        try:
            prompt = load_prompt(
                system_name,
                task_path,
                original=original,
                context=context or ""
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.6
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[WARN] Optimization failed: {e}")
            return original

    async def analyze_jd_match(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """分析简历与JD的匹配度"""
        if not self.client:
            return {"match_score": 85, "suggestions": ["添加更多相关技能"]}

        try:
            prompt = load_prompt(
                "resume_expert",
                "analyze/jd_match",
                resume=json.dumps(resume_content, ensure_ascii=False),
                jd=job_description
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"[WARN] JD match analysis failed: {e}")
            return {
                "match_score": 70,
                "suggestions": ["请手动检查简历与岗位的匹配度"],
                "error": str(e)
            }

    async def predict_interview_questions(
        self,
        resume_content: Dict[str, Any],
        target_position: str,
        company_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """预测面试问题"""
        if not self.client:
            return self._mock_interview_questions(target_position)

        try:
            prompt = load_prompt(
                "career_advisor",
                "analyze/interview_questions",
                resume=json.dumps(resume_content, ensure_ascii=False),
                position=target_position,
                company_type=company_type or ""
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", [])
            
        except Exception as e:
            print(f"[WARN] Interview prediction failed: {e}")
            return self._mock_interview_questions(target_position)

    async def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """解析简历文本"""
        if not self.client:
            return self._mock_parsed_resume(text)

        try:
            prompt = load_prompt(
                "resume_expert",
                "parse/resume",
                text=text[:4000]
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"[WARN] Resume parsing failed: {e}")
            return self._mock_parsed_resume(text)

    # 辅助方法
    def _build_fallback_content(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """构建降级内容"""
        return {
            "basic_info": user_info.get("basic_info", {}),
            "education": user_info.get("education", []),
            "work_experience": user_info.get("work_experience", []),
            "projects": user_info.get("projects", []),
            "skills": user_info.get("skills", []),
            "certifications": user_info.get("certifications", []),
            "_fallback": True
        }

    def _generate_mock_content(
        self,
        user_info: Dict[str, Any],
        target_position: str
    ) -> Dict[str, Any]:
        """模拟内容"""
        return {
            "basic_info": {
                "name": user_info.get("basic_info", {}).get("name", "用户"),
                "job_intention": target_position
            },
            "education": user_info.get("education", []),
            "work_experience": user_info.get("work_experience", []),
            "projects": user_info.get("projects", []),
            "skills": user_info.get("skills", []),
            "_mock": True
        }

    def _mock_optimize(self, original: str, optimization_type: str) -> str:
        """模拟优化"""
        return f"【{optimization_type}优化】{original}"

    def _mock_interview_questions(self, position: str) -> List[Dict[str, Any]]:
        """模拟面试问题"""
        return [
            {
                "question": "请介绍一下你自己",
                "category": "综合",
                "difficulty": "基础"
            },
            {
                "question": f"为什么选择{position}这个方向？",
                "category": "动机",
                "difficulty": "基础"
            }
        ]

    def _mock_parsed_resume(self, text: str) -> Dict[str, Any]:
        """模拟解析"""
        return {
            "basic_info": {},
            "education": [],
            "work_experience": [],
            "projects": [],
            "skills": []
        }

    @property
    def provider_name(self) -> str:
        return "OpenAI V2 (Optimized)"

    @property
    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)
