"""
DeepSeek AI提供商实现
DeepSeek是中国的AI模型提供商，提供高性能的中文语言模型
API文档: https://platform.deepseek.com/api-docs/
"""
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI

from app.services.ai.base import AIProviderBase


class DeepSeekProvider(AIProviderBase):
    """DeepSeek提供商 - 使用OpenAI兼容API"""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
        **kwargs
    ):
        super().__init__(api_key, model, **kwargs)
        self.base_url = base_url
        # DeepSeek使用OpenAI兼容的API
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        ) if api_key else None
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)

    async def generate_resume_content(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        style: str = "professional",
        language: str = "zh"
    ) -> Dict[str, Any]:
        """生成简历内容"""
        if not self.client:
            return self._generate_mock_content(user_info, target_position)

        lang_instruction = "使用中文撰写" if language == "zh" else "Write in English"

        system_prompt = f"""你是专业的简历撰写专家。{lang_instruction}。

        请根据用户信息和目标岗位，生成完整的简历内容。

        要求：
        1. 使用STAR法则描述工作经历和项目（Situation情境、Task任务、Action行动、Result结果）
        2. 突出与目标岗位相关的技能和经验
        3. 使用专业的术语和表达
        4. 内容简洁有力，避免冗余

        返回JSON格式的简历内容，包含：
        - basic_info: 基本信息（姓名、求职意向、自我评价）
        - education: 教育经历列表
        - work_experience: 工作经历列表（使用STAR法则）
        - projects: 项目经历列表（使用STAR法则）
        - skills: 技能列表（分为专业技能、工具技能、软技能）
        - certifications: 证书列表（如有）
        """

        user_prompt = f"""
        用户信息: {json.dumps(user_info, ensure_ascii=False)}
        目标岗位: {target_position}
        风格要求: {style}

        请生成完整的简历内容。
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
                - Situation (情境): 背景和挑战
                - Task (任务): 承担的职责和目标
                - Action (行动): 采取的具体措施和方法
                - Result (结果): 量化的成果和影响

                确保改写后的内容更加具体、有说服力。""",

            "quantify": """将以下内容中的模糊描述转化为具体的量化数据。
                - 添加百分比、数字、金额等具体指标
                - 使用"提升X%"、"节省X万元"、"覆盖X用户"等量化表达
                - 如果没有具体数据，给出合理的估计范围

                让内容更有说服力。""",

            "keywords": """优化以下内容，增加与岗位相关的关键词：
                - 添加行业标准术语
                - 增加技术栈关键词
                - 使用强有力的动词（如"主导"、"推动"、"优化"等）
                - 确保对ATS（ applicant tracking system）系统友好

                提升简历的专业性和匹配度。""",

            "polish": """润色以下内容：
                - 使用更专业、更精准的表达
                - 增强语句的力度和感染力
                - 提升整体可读性和逻辑性
                - 保持简洁有力，去除冗余
                - 确保符合中文表达习惯

                让内容更加专业、流畅。"""
        }

        system_prompt = prompts.get(optimization_type, prompts["polish"])
        user_prompt = f"原文内容：\n{original}"
        if context:
            user_prompt += f"\n\n上下文信息：{context}"
        user_prompt += "\n\n请直接返回优化后的内容，不要添加任何解释。"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    async def analyze_jd_match(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """分析简历与JD的匹配度"""
        if not self.client:
            return self._mock_jd_match()

        system_prompt = """你是专业的HR和招聘专家。分析简历与职位描述的匹配度。

        返回JSON格式：
        {
            "match_score": 0-100的匹配分数（整数）,
            "matched_keywords": ["匹配的关键词1", "匹配的关键词2", ...],
            "missing_keywords": ["缺失的关键词1", "缺失的关键词2", ...],
            "suggestions": ["优化建议1", "优化建议2", ...],
            "strengths": ["优势点1", "优势点2", ...],
            "weaknesses": ["待改进点1", "待改进点2", ...]
        }

        分析维度：
        1. 技能匹配度
        2. 经验相关性
        3. 教育背景
        4. 项目经历
        5. 证书资质
        """

        user_prompt = f"""简历内容：{json.dumps(resume_content, ensure_ascii=False)}

        职位描述：{job_description}

        请进行详细的匹配度分析。"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
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

        company_context = f"\n公司类型: {company_type}" if company_type else ""

        system_prompt = """你是一位经验丰富的HR面试官和招聘专家。

        根据候选人的简历和目标岗位，生成可能被问到的面试问题。

        返回JSON格式：{"questions": [...]}

        每个问题包含：
        - question: 问题内容
        - category: 分类 (行为面试/技术面试/专业知识/综合能力)
        - difficulty: 难度 (基础/中等/进阶)
        - suggested_answer: 回答要点和建议（2-3条要点）

        要求：
        1. 生成15-20个问题
        2. 覆盖不同类别和难度
        3. 问题要针对简历内容设计
        4. 回答建议要具体、可操作
        """

        user_prompt = f"""简历内容：{json.dumps(resume_content, ensure_ascii=False)}

        目标岗位：{target_position}{company_context}

        请生成面试问题。"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("questions", []) if isinstance(result, dict) else result

    async def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """解析简历文本，提取结构化信息"""
        if not self.client:
            return self._mock_parsed_resume()

        system_prompt = """你是专业的简历解析专家。从简历文本中提取结构化信息。

        返回JSON格式：
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

        注意：
        1. 如果某项信息无法提取，使用空字符串或空数组
        2. 尽可能提取所有有效信息
        3. 日期统一格式：YYYY-MM
        """

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

    # ===== Mock方法（无API Key时使用）=====

    def _generate_mock_content(
        self,
        user_info: Dict[str, Any],
        target_position: str
    ) -> Dict[str, Any]:
        """生成模拟内容"""
        return {
            "basic_info": {
                "name": user_info.get("basic_info", {}).get("name", "张三"),
                "job_intention": target_position,
                "self_introduction": f"具有丰富{target_position}经验的专业人才。"
            },
            "education": user_info.get("education", []),
            "work_experience": user_info.get("work_experience", []),
            "projects": user_info.get("projects", []),
            "skills": user_info.get("skills", []),
            "certifications": user_info.get("certifications", [])
        }

    def _mock_optimize(self, original: str, optimization_type: str) -> str:
        """模拟优化"""
        prefixes = {
            "star_method": "【DeepSeek STAR优化】",
            "quantify": "【DeepSeek 量化优化】",
            "keywords": "【DeepSeek 关键词优化】",
            "polish": "【DeepSeek 润色】"
        }
        return f"{prefixes.get(optimization_type, '【DeepSeek优化】')}{original}"

    def _mock_jd_match(self) -> Dict[str, Any]:
        """模拟JD匹配分析"""
        return {
            "match_score": 75,
            "matched_keywords": ["Python", "项目开发"],
            "missing_keywords": ["团队管理", "架构设计"],
            "suggestions": ["补充团队管理经验", "突出架构设计能力"],
            "strengths": ["技术扎实", "项目经验丰富"],
            "weaknesses": ["管理经验不足"]
        }

    def _mock_interview_questions(self, target_position: str) -> List[Dict[str, Any]]:
        """模拟面试问题"""
        return [
            {
                "question": "请简单介绍一下你自己",
                "category": "综合能力",
                "difficulty": "基础",
                "suggested_answer": "突出与岗位最相关的经验"
            },
            {
                "question": f"你为什么应聘{target_position}这个岗位？",
                "category": "行为面试",
                "difficulty": "基础",
                "suggested_answer": "展示对岗位的理解和职业规划"
            }
        ]

    def _mock_parsed_resume(self) -> Dict[str, Any]:
        """模拟简历解析"""
        return {
            "basic_info": {"name": "", "phone": "", "email": ""},
            "education": [],
            "work_experience": [],
            "projects": [],
            "skills": []
        }

    @property
    def provider_name(self) -> str:
        return "DeepSeek"

    @property
    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)
