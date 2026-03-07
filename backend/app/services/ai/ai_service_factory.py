"""
AI服务工厂和配置管理
支持多个AI提供商的动态切换
"""
from typing import Dict, Any, Optional
from enum import Enum

from app.services.ai.base import AIProviderBase
from app.services.ai.providers import (
    OpenAIProvider,
    DeepSeekProvider,
    XiaomiProvider,
)


class AIProvider(str, Enum):
    """AI提供商枚举"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    XIAOMI = "xiaomi"
    # 未来可扩展
    # ANTHROPIC = "anthropic"
    # QWEN = "qwen"
    # BAICHUAN = "baichuan"
    # ERNIE = "ernie"


class AIModelConfig:
    """AI模型配置"""

    # OpenAI配置
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.7

    # DeepSeek配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MAX_TOKENS: int = 4000
    DEEPSEEK_TEMPERATURE: float = 0.7

    # 小米配置
    XIAOMI_API_KEY: str = ""
    XIAOMI_MODEL: str = "xiaoai-chat"
    XIAOMI_BASE_URL: str = "https://api.xiaomi.com/v1"
    XIAOMI_MAX_TOKENS: int = 4000
    XIAOMI_TEMPERATURE: float = 0.7

    # 默认使用的提供商
    DEFAULT_PROVIDER: AIProvider = AIProvider.OPENAI


class AIServiceFactory:
    """AI服务工厂"""

    def __init__(self, config: Optional[AIModelConfig] = None):
        """
        初始化工厂

        Args:
            config: AI模型配置，如果为None则使用默认配置
        """
        self.config = config or AIModelConfig()
        self._providers: Dict[AIProvider, AIProviderBase] = {}
        self._current_provider: Optional[AIProvider] = None

    def get_provider(
        self,
        provider: Optional[AIProvider] = None
    ) -> AIProviderBase:
        """
        获取AI提供商实例

        Args:
            provider: 提供商类型，如果为None则使用默认提供商

        Returns:
            AI提供商实例
        """
        provider = provider or self.config.DEFAULT_PROVIDER

        # 如果已经创建过该provider，直接返回
        if provider in self._providers:
            return self._providers[provider]

        # 创建新的provider实例
        provider_instance = self._create_provider(provider)
        self._providers[provider] = provider_instance
        self._current_provider = provider

        return provider_instance

    def _create_provider(self, provider: AIProvider) -> AIProviderBase:
        """创建AI提供商实例"""
        if provider == AIProvider.OPENAI:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                model=self.config.OPENAI_MODEL,
                max_tokens=self.config.OPENAI_MAX_TOKENS,
                temperature=self.config.OPENAI_TEMPERATURE
            )

        elif provider == AIProvider.DEEPSEEK:
            return DeepSeekProvider(
                api_key=self.config.DEEPSEEK_API_KEY,
                model=self.config.DEEPSEEK_MODEL,
                base_url=self.config.DEEPSEEK_BASE_URL,
                max_tokens=self.config.DEEPSEEK_MAX_TOKENS,
                temperature=self.config.DEEPSEEK_TEMPERATURE
            )

        elif provider == AIProvider.XIAOMI:
            return XiaomiProvider(
                api_key=self.config.XIAOMI_API_KEY,
                model=self.config.XIAOMI_MODEL,
                base_url=self.config.XIAOMI_BASE_URL,
                max_tokens=self.config.XIAOMI_MAX_TOKENS,
                temperature=self.config.XIAOMI_TEMPERATURE
            )

        else:
            raise ValueError(f"不支持的AI提供商: {provider}")

    def switch_provider(self, provider: AIProvider) -> AIProviderBase:
        """
        切换到指定的AI提供商

        Args:
            provider: 目标提供商

        Returns:
            AI提供商实例
        """
        return self.get_provider(provider)

    def get_available_providers(self) -> list[Dict[str, Any]]:
        """
        获取所有可用的提供商列表

        Returns:
            提供商信息列表
        """
        providers_info = []

        # 检查OpenAI
        openai = self._create_provider(AIProvider.OPENAI)
        providers_info.append({
            "provider": AIProvider.OPENAI.value,
            "name": openai.provider_name,
            "available": openai.is_available,
            "model": self.config.OPENAI_MODEL
        })

        # 检查DeepSeek
        deepseek = self._create_provider(AIProvider.DEEPSEEK)
        providers_info.append({
            "provider": AIProvider.DEEPSEEK.value,
            "name": deepseek.provider_name,
            "available": deepseek.is_available,
            "model": self.config.DEEPSEEK_MODEL
        })

        # 检查小米
        xiaomi = self._create_provider(AIProvider.XIAOMI)
        providers_info.append({
            "provider": AIProvider.XIAOMI.value,
            "name": xiaomi.provider_name,
            "available": xiaomi.is_available,
            "model": self.config.XIAOMI_MODEL
        })

        return providers_info

    def update_config(
        self,
        provider: AIProvider,
        **kwargs
    ):
        """
        更新指定提供商的配置

        Args:
            provider: 提供商类型
            **kwargs: 配置参数（如api_key, model等）
        """
        if provider == AIProvider.OPENAI:
            if "api_key" in kwargs:
                self.config.OPENAI_API_KEY = kwargs["api_key"]
            if "model" in kwargs:
                self.config.OPENAI_MODEL = kwargs["model"]

        elif provider == AIProvider.DEEPSEEK:
            if "api_key" in kwargs:
                self.config.DEEPSEEK_API_KEY = kwargs["api_key"]
            if "model" in kwargs:
                self.config.DEEPSEEK_MODEL = kwargs["model"]
            if "base_url" in kwargs:
                self.config.DEEPSEEK_BASE_URL = kwargs["base_url"]

        elif provider == AIProvider.XIAOMI:
            if "api_key" in kwargs:
                self.config.XIAOMI_API_KEY = kwargs["api_key"]
            if "model" in kwargs:
                self.config.XIAOMI_MODEL = kwargs["model"]
            if "base_url" in kwargs:
                self.config.XIAOMI_BASE_URL = kwargs["base_url"]

        # 清除已创建的provider实例，以便使用新配置重新创建
        if provider in self._providers:
            del self._providers[provider]

    @property
    def current_provider(self) -> Optional[AIProvider]:
        """当前使用的提供商"""
        return self._current_provider


# 全局单例
_factory_instance: Optional[AIServiceFactory] = None


def get_ai_service_factory(config: Optional[AIModelConfig] = None) -> AIServiceFactory:
    """
    获取AI服务工厂单例

    Args:
        config: AI模型配置（仅在第一次调用时有效）

    Returns:
        AI服务工厂实例
    """
    global _factory_instance
    if _factory_instance is None:
        _factory_instance = AIServiceFactory(config)
    return _factory_instance


def get_ai_provider(provider: Optional[AIProvider] = None) -> AIProviderBase:
    """
    便捷函数：获取AI提供商实例

    Args:
        provider: 提供商类型

    Returns:
        AI提供商实例
    """
    factory = get_ai_service_factory()
    return factory.get_provider(provider)
