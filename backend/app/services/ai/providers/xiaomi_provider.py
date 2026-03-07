"""
小米MiMo AI提供商实现
小米MiMo AI开放平台 - https://platform.xiaomimimo.com/
支持OpenAI兼容的API格式

官方文档: https://platform.xiaomimimo.com/#/docs/quick-start/first-api-call
API端点: https://api.xiaomimimo.com/v1
"""
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI

from app.services.ai.base import AIProviderBase


class XiaomiProvider(AIProviderBase):
    """小米MiMo AI提供商 - 使用OpenAI兼容API"""

    def __init__(
        self,
        api_key: str,
        model: str = "MiMo-V2-Flash",
        base_url: str = "https://api.xiaomimimo.com/v1",
        **kwargs
    ):
        super().__init__(api_key, model, **kwargs)
        # 小米MiMo使用OpenAI兼容的API
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

        返回JSON格式的简历内容。
        """

        user_prompt = f"""
        用户信息: {json.dumps(user_info, ensure_ascii=False)}
        目标岗位: {target_position}
        风格要求: {style}
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

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return self._generate_mock_content(user_info, target_position)

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
                - Result (结果): 量化的成果和影响""",

            "quantify": """将以下内容中的模糊描述转化为具体的量化数据。
                添加百分比、数字、金额等具体指标。""",

            "keywords": """优化以下内容，增加与岗位相关的关键词：
                - 添加行业标准术语
                - 增加技术关键词
                - 使用强有力的动词""",

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

        return response.choices[0].message.content.strip()

    async def analyze_jd_match(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """分析简历与JD的匹配度"""
        if not self.client:
            return self._mock_jd_match()

        system_prompt = """分析简历与职位描述的匹配度。返回JSON格式：
        {
            "match_score": 0-100的匹配分数,
            "matched_keywords": 匹配的关键词列表,
            "missing_keywords": 缺失的关键词列表,
            "suggestions": 优化建议列表,
            "strengths": 优势点列表,
            "weaknesses": 待改进点列表
        }"""

        user_prompt = f"""简历内容：{json.dumps(resume_content, ensure_ascii=False)}

        职位描述：{job_description}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return self._mock_jd_match()

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

        system_prompt = """你是一位经验丰富的HR面试官。根据候选人的简历和目标岗位，
        生成可能被问到的面试问题。返回JSON格式：{"questions": [...]}

        每个问题包含：
        - question: 问题内容
        - category: 分类(行为面试/技术面试/专业知识/综合能力)
        - difficulty: 难度(基础/中等/进阶)
        - suggested_answer: 回答要点和建议

        生成15-20个问题。"""

        user_prompt = f"""简历内容：{json.dumps(resume_content, ensure_ascii=False)}

        目标岗位：{target_position}{company_context}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", []) if isinstance(result, dict) else result
        except json.JSONDecodeError:
            return self._mock_interview_questions(target_position)

    async def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """解析简历文本，提取结构化信息"""
        if not self.client:
            return self._mock_parsed_resume()

        system_prompt = """你是简历解析专家。从简历文本中提取结构化信息。
        返回JSON格式，包含basic_info, education, work_experience, projects, skills。"""

        user_prompt = f"请解析以下简历文本：\n\n{text[:4000]}"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return self._mock_parsed_resume()

    # ===== Mock方法 =====

    def _generate_mock_content(
        self,
        user_info: Dict[str, Any],
        target_position: str
    ) -> Dict[str, Any]:
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
        prefixes = {
            "star_method": "【小米MiMo STAR优化】",
            "quantify": "【小米MiMo 量化优化】",
            "keywords": "【小米MiMo 关键词优化】",
            "polish": "【小米MiMo 润色】"
        }
        return f"{prefixes.get(optimization_type, '【小米MiMo优化】')}{original}"

    def _mock_jd_match(self) -> Dict[str, Any]:
        return {
            "match_score": 75,
            "matched_keywords": ["项目经验"],
            "missing_keywords": ["团队管理"],
            "suggestions": ["补充管理经验"],
            "strengths": ["技术扎实"],
            "weaknesses": ["管理经验不足"]
        }

    def _mock_interview_questions(self, target_position: str) -> List[Dict[str, Any]]:
        return [
            {
                "question": "请简单介绍一下你自己",
                "category": "综合能力",
                "difficulty": "基础",
                "suggested_answer": "突出相关经验"
            },
            {
                "question": f"你为什么应聘{target_position}这个岗位？",
                "category": "行为面试",
                "difficulty": "基础",
                "suggested_answer": "展示对岗位的理解"
            }
        ]

    def _mock_parsed_resume(self) -> Dict[str, Any]:
        return {
            "basic_info": {"name": "", "phone": "", "email": ""},
            "education": [],
            "work_experience": [],
            "projects": [],
            "skills": []
        }

    @property
    def provider_name(self) -> str:
        return "Xiaomi MiMo"

    @property
    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)
