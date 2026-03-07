"""
OpenAI AI提供商实现
"""
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI

from app.services.ai.base import AIProviderBase


class OpenAIProvider(AIProviderBase):
    """OpenAI提供商"""

    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)

    async def generate_resume_content(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        style: str = "professional",
        language: str = "zh"
    ) -> Dict[str, Any]:
        """生成简历内容 - 三元协同Agent架构"""
        if not self.client:
            return self._generate_mock_content(user_info, target_position)

        # 阶段1: 对话理解
        context = await self._dialogue_phase(user_info, target_position, language)

        # 阶段2: 规划
        plan = await self._planning_phase(context, style)

        # 阶段3: 执行
        content = await self._execution_phase(plan, language)

        return content

    async def _dialogue_phase(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        language: str
    ) -> Dict[str, Any]:
        """对话阶段：理解用户需求"""
        system_prompt = """你是一位专业的简历顾问。分析用户信息和目标岗位，提取关键信息点。
        返回JSON格式的分析结果，包含：
        - key_strengths: 用户的核心优势
        - skill_gaps: 可能需要补充的技能
        - highlight_areas: 应该重点突出的领域
        - industry_keywords: 相关行业关键词"""

        user_prompt = f"""
        用户信息: {json.dumps(user_info, ensure_ascii=False)}
        目标岗位: {target_position}

        请分析并返回JSON格式的结果。
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        return {
            "user_info": user_info,
            "target_position": target_position,
            "analysis": json.loads(response.choices[0].message.content),
            "language": language
        }

    async def _planning_phase(
        self,
        context: Dict[str, Any],
        style: str
    ) -> Dict[str, Any]:
        """计划阶段：制定生成策略"""
        system_prompt = """你是简历生成策略规划师。根据分析结果，制定简历各模块的生成策略。
        返回JSON格式的计划，包含：
        - basic_info_strategy: 基本信息呈现策略
        - experience_strategy: 工作经历描述策略（使用STAR法则）
        - education_strategy: 教育背景呈现策略
        - skills_strategy: 技能展示策略
        - projects_strategy: 项目经历策略"""

        user_prompt = f"""
        分析结果: {json.dumps(context['analysis'], ensure_ascii=False)}
        目标岗位: {context['target_position']}
        风格要求: {style}

        请制定详细的生成计划。
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )

        return {
            **context,
            "style": style,
            "plan": json.loads(response.choices[0].message.content)
        }

    async def _execution_phase(
        self,
        plan: Dict[str, Any],
        language: str
    ) -> Dict[str, Any]:
        """执行阶段：生成简历内容"""
        lang_instruction = "使用中文撰写" if language == "zh" else "Write in English"

        system_prompt = f"""你是专业简历撰写专家。根据策略计划生成完整的简历内容。
        {lang_instruction}。

        使用STAR法则描述工作经历和项目：
        - Situation: 情境背景
        - Task: 任务目标
        - Action: 采取行动
        - Result: 量化成果

        返回JSON格式的完整简历内容。"""

        user_prompt = f"""
        用户信息: {json.dumps(plan['user_info'], ensure_ascii=False)}
        目标岗位: {plan['target_position']}
        生成策略: {json.dumps(plan['plan'], ensure_ascii=False)}

        请生成完整的简历内容，包含以下模块：
        - basic_info: 基本信息
        - education: 教育经历列表
        - work_experience: 工作经历列表
        - projects: 项目经历列表
        - skills: 技能列表
        - certifications: 证书列表（如有）
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    async def optimize_content(
        self,
        original: str,
        optimization_type: str,
        context: Optional[str] = None
    ) -> str:
        """优化内容"""
        if not self.client:
            return self._mock_optimize(original, optimization_type)

        prompts = {
            "star_method": """使用STAR法则改写以下内容，突出：
                - 情境(Situation): 背景和挑战
                - 任务(Task): 承担的职责
                - 行动(Action): 采取的具体措施
                - 结果(Result): 量化的成果和影响""",

            "quantify": """将以下内容中的模糊描述转化为具体的量化数据。
                添加百分比、数字、金额等具体指标。
                如果没有具体数据，请给出合理的估计范围。""",

            "keywords": """优化以下内容，增加与岗位相关的关键词：
                - 添加行业术语
                - 增加技术关键词
                - 优化动词使用
                确保对ATS系统友好。""",

            "polish": """润色以下内容：
                - 使用更专业的表达
                - 增强语句的力度
                - 提升整体可读性
                - 保持简洁有力"""
        }

        system_prompt = prompts.get(optimization_type, prompts["polish"])
        user_prompt = f"原文内容：\n{original}"
        if context:
            user_prompt += f"\n\n上下文信息：{context}"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6
        )

        return response.choices[0].message.content

    async def analyze_jd_match(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """分析简历与JD的匹配度"""
        if not self.client:
            return {"match_score": 85, "suggestions": ["添加更多相关技能", "突出项目成果"]}

        system_prompt = """分析简历与职位描述的匹配度。返回JSON格式：
        {
            "match_score": 0-100的匹配分数,
            "matched_keywords": 匹配的关键词列表,
            "missing_keywords": 缺失的关键词列表,
            "suggestions": 优化建议列表,
            "strengths": 优势点列表,
            "weaknesses": 待改进点列表
        }"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"简历内容：{json.dumps(resume_content, ensure_ascii=False)}\n\n职位描述：{job_description}"}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    async def predict_interview_questions(
        self,
        resume_content: Dict[str, Any],
        target_position: str,
        company_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """预测面试问题"""
        if not self.client:
            return self._mock_interview_questions(target_position)

        company_context = f"公司类型: {company_type}" if company_type else ""

        system_prompt = """你是一位经验丰富的HR面试官。根据候选人的简历和目标岗位，
        生成可能被问到的面试问题。返回JSON数组格式，每个问题包含：
        - question: 问题内容
        - category: 分类(行为面试/技术面试/专业知识/综合能力)
        - difficulty: 难度(基础/中等/进阶)
        - suggested_answer: 回答要点和建议

        生成15-20个问题，覆盖不同类别和难度。"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"简历内容：{json.dumps(resume_content, ensure_ascii=False)}\n\n目标岗位：{target_position}\n{company_context}"}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("questions", result) if isinstance(result, dict) else result

    async def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """解析简历文本，提取结构化信息"""
        if not self.client:
            return self._mock_parsed_resume(text)

        system_prompt = """你是简历解析专家。从简历文本中提取结构化信息。
        返回JSON格式，包含：
        {
            "basic_info": {
                "name": "姓名",
                "phone": "电话",
                "email": "邮箱",
                "location": "地点",
                "title": "岗位/头衔"
            },
            "education": [{
                "school": "学校",
                "degree": "学历",
                "major": "专业",
                "start_date": "开始时间",
                "end_date": "结束时间"
            }],
            "work_experience": [{
                "company": "公司",
                "position": "职位",
                "start_date": "开始时间",
                "end_date": "结束时间",
                "description": "职责描述"
            }],
            "projects": [{
                "name": "项目名",
                "role": "角色",
                "description": "描述"
            }],
            "skills": ["技能1", "技能2"]
        }
        如果某项信息无法提取，请使用空字符串或空数组。"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请解析以下简历文本：\n\n{text[:4000]}"}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def _mock_interview_questions(self, target_position: str) -> List[Dict[str, Any]]:
        """模拟面试问题"""
        return [
            {
                "question": "请简单介绍一下你自己",
                "category": "综合能力",
                "difficulty": "基础",
                "suggested_answer": "结合岗位要求，突出相关经验和技能"
            },
            {
                "question": f"你为什么选择{target_position}这个岗位？",
                "category": "行为面试",
                "difficulty": "基础",
                "suggested_answer": "结合个人职业规划和岗位匹配度回答"
            }
        ]

    def _mock_parsed_resume(self, text: str) -> Dict[str, Any]:
        """模拟简历解析"""
        return {
            "basic_info": {"name": "", "phone": "", "email": ""},
            "education": [],
            "work_experience": [],
            "projects": [],
            "skills": []
        }

    def _generate_mock_content(
        self,
        user_info: Dict[str, Any],
        target_position: str
    ) -> Dict[str, Any]:
        """生成模拟内容（无API Key时使用）"""
        return {
            "basic_info": {
                "name": user_info.get("basic_info", {}).get("name", "张三"),
                "job_intention": target_position,
                "self_introduction": f"具有丰富{target_position}经验的专业人才，善于团队协作，追求卓越。"
            },
            "education": user_info.get("education", []),
            "work_experience": user_info.get("work_experience", []),
            "projects": user_info.get("projects", []),
            "skills": user_info.get("skills", []),
            "certifications": user_info.get("certifications", [])
        }

    def _mock_optimize(self, original: str, optimization_type: str) -> str:
        """模拟优化（无API Key时使用）"""
        prefixes = {
            "star_method": "【优化后】",
            "quantify": "【量化后】",
            "keywords": "【关键词优化】",
            "polish": "【润色后】"
        }
        return f"{prefixes.get(optimization_type, '【优化后】')}{original}（已使用AI优化）"

    @property
    def provider_name(self) -> str:
        return "OpenAI"

    @property
    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)
