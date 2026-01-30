"""
AI服务抽象基类
定义所有AI提供商需要实现的接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class AIProviderBase(ABC):
    """AI提供商抽象基类"""

    def __init__(self, api_key: str, model: str, **kwargs):
        """
        初始化AI提供商

        Args:
            api_key: API密钥
            model: 模型名称
            **kwargs: 其他配置参数
        """
        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
    async def generate_resume_content(
        self,
        user_info: Dict[str, Any],
        target_position: str,
        style: str = "professional",
        language: str = "zh"
    ) -> Dict[str, Any]:
        """
        生成简历内容

        Args:
            user_info: 用户信息
            target_position: 目标岗位
            style: 风格要求
            language: 语言（zh/en）

        Returns:
            生成的简历内容
        """
        pass

    @abstractmethod
    async def optimize_content(
        self,
        original: str,
        optimization_type: str,
        context: Optional[str] = None
    ) -> str:
        """
        优化内容

        Args:
            original: 原始内容
            optimization_type: 优化类型 (star_method/quantify/keywords/polish)
            context: 上下文信息

        Returns:
            优化后的内容
        """
        pass

    @abstractmethod
    async def analyze_jd_match(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """
        分析简历与JD的匹配度

        Args:
            resume_content: 简历内容
            job_description: 职位描述

        Returns:
            匹配度分析结果
        """
        pass

    @abstractmethod
    async def predict_interview_questions(
        self,
        resume_content: Dict[str, Any],
        target_position: str,
        company_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        预测面试问题

        Args:
            resume_content: 简历内容
            target_position: 目标岗位
            company_type: 公司类型

        Returns:
            面试问题列表
        """
        pass

    @abstractmethod
    async def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """
        解析简历文本，提取结构化信息

        Args:
            text: 简历文本

        Returns:
            结构化的简历信息
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供商名称"""
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """检查服务是否可用（是否有有效的API密钥）"""
        pass
