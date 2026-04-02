"""
小米 MiMo AI 提供商测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ai.providers.xiaomi_provider import XiaomiProvider


class TestXiaomiProviderInit:
    """小米提供商初始化测试"""

    def test_init_with_api_key(self):
        """测试: 使用 API Key 初始化"""
        with patch('app.services.ai.providers.xiaomi_provider.AsyncOpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client

            provider = XiaomiProvider(api_key="test_key")

            assert provider.api_key == "test_key"
            assert provider.model == "MiMo-V2-Flash"
            assert provider.client == mock_client
            assert provider.max_tokens == 4000
            assert provider.temperature == 0.7

    def test_init_with_custom_model(self):
        """测试: 使用自定义模型初始化"""
        with patch('app.services.ai.providers.xiaomi_provider.AsyncOpenAI') as mock_openai:
            provider = XiaomiProvider(
                api_key="test_key",
                model="MiMo-V2-Pro"
            )

            assert provider.model == "MiMo-V2-Pro"

    def test_init_with_custom_base_url(self):
        """测试: 使用自定义 base_url"""
        with patch('app.services.ai.providers.xiaomi_provider.AsyncOpenAI') as mock_openai:
            provider = XiaomiProvider(
                api_key="test_key",
                base_url="https://custom.api.com/v1"
            )

            mock_openai.assert_called_once()

    def test_init_with_custom_max_tokens(self):
        """测试: 自定义 max_tokens"""
        with patch('app.services.ai.providers.xiaomi_provider.AsyncOpenAI'):
            provider = XiaomiProvider(
                api_key="test_key",
                max_tokens=8000
            )

            assert provider.max_tokens == 8000

    def test_init_with_custom_temperature(self):
        """测试: 自定义 temperature"""
        with patch('app.services.ai.providers.xiaomi_provider.AsyncOpenAI'):
            provider = XiaomiProvider(
                api_key="test_key",
                temperature=0.5
            )

            assert provider.temperature == 0.5

    def test_init_without_api_key(self):
        """测试: 无 API Key 初始化"""
        provider = XiaomiProvider(api_key="")

        assert provider.client is None

    def test_init_with_none_api_key(self):
        """测试: API Key 为 None"""
        provider = XiaomiProvider(api_key=None)

        assert provider.client is None


class TestGenerateResumeContent:
    """生成简历内容测试"""

    async def test_generate_resume_content_success(self):
        """测试: 成功生成简历内容"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "测试"}}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="软件工程师"
        )

        assert result["basic_info"]["name"] == "测试"

    async def test_generate_resume_content_chinese(self):
        """测试: 中文简历生成"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "李四"}}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.generate_resume_content(
            user_info={},
            target_position="工程师",
            language="zh"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "中文撰写" in system_prompt

    async def test_generate_resume_content_english(self):
        """测试: 英文简历生成"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "John"}}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.generate_resume_content(
            user_info={},
            target_position="Engineer",
            language="en"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "Write in English" in system_prompt

    async def test_generate_resume_content_invalid_json(self):
        """测试: 无效 JSON 返回 mock 内容"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid json"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        # 应该返回 mock 内容
        assert result["basic_info"]["name"] == "张三"

    async def test_generate_resume_content_without_client(self):
        """测试: 无客户端时返回 mock 内容"""
        provider = XiaomiProvider(api_key="")

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "张三"
        assert result["basic_info"]["job_intention"] == "工程师"

    async def test_generate_resume_content_with_style(self):
        """测试: 带风格参数生成"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.generate_resume_content(
            user_info={},
            target_position="工程师",
            style="professional"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        user_prompt = call_kwargs["messages"][1]["content"]
        assert "professional" in user_prompt


class TestOptimizeContent:
    """内容优化测试"""

    async def test_optimize_star_method(self):
        """测试: STAR 法则优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "优化后的内容"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.optimize_content(
            original="负责项目开发",
            optimization_type="star_method"
        )

        assert result == "优化后的内容"

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "STAR法则" in system_prompt

    async def test_optimize_quantify(self):
        """测试: 量化优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "量化后内容"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.optimize_content(
            original="提升性能",
            optimization_type="quantify"
        )

        assert result == "量化后内容"

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "量化" in system_prompt

    async def test_optimize_keywords(self):
        """测试: 关键词优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "关键词优化后"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.optimize_content(
            original="使用Python开发",
            optimization_type="keywords"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "关键词" in system_prompt

    async def test_optimize_polish(self):
        """测试: 润色优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "润色后内容"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.optimize_content(
            original="原始内容",
            optimization_type="polish"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "润色" in system_prompt

    async def test_optimize_with_context(self):
        """测试: 带上下文优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "优化结果"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.optimize_content(
            original="原始内容",
            optimization_type="polish",
            context="这是前端开发岗位"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        user_prompt = call_kwargs["messages"][1]["content"]
        assert "上下文" in user_prompt

    async def test_optimize_without_client(self):
        """测试: 无客户端时返回 mock 优化"""
        provider = XiaomiProvider(api_key="")

        result = await provider.optimize_content(
            original="原始内容",
            optimization_type="polish"
        )

        assert "【小米MiMo 润色】" in result

    async def test_optimize_unknown_type_defaults_to_polish(self):
        """测试: 未知优化类型默认为润色"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "默认润色"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.optimize_content(
            original="内容",
            optimization_type="unknown_type"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "润色" in system_prompt


class TestAnalyzeJDMatch:
    """JD 匹配分析测试"""

    async def test_analyze_jd_match_success(self):
        """测试: 成功分析 JD 匹配"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '''{
            "match_score": 85,
            "matched_keywords": ["Python", "Django"],
            "missing_keywords": ["Redis"],
            "suggestions": ["补充 Redis 经验"],
            "strengths": ["技术扎实"],
            "weaknesses": ["缺少缓存经验"]
        }'''

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.analyze_jd_match(
            resume_content={"skills": ["Python", "Django"]},
            job_description="需要 Python、Django、Redis 经验"
        )

        assert result["match_score"] == 85
        assert "Python" in result["matched_keywords"]

    async def test_analyze_jd_match_without_client(self):
        """测试: 无客户端时返回 mock 匹配"""
        provider = XiaomiProvider(api_key="")

        result = await provider.analyze_jd_match(
            resume_content={},
            job_description="JD"
        )

        assert result["match_score"] == 75
        assert "项目经验" in result["matched_keywords"]

    async def test_analyze_jd_match_invalid_json(self):
        """测试: 无效 JSON 返回 mock"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid json"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.analyze_jd_match({}, "JD")

        assert result["match_score"] == 75


class TestPredictInterviewQuestions:
    """预测面试问题测试"""

    async def test_predict_questions_success(self):
        """测试: 成功预测面试问题"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '''{
            "questions": [
                {
                    "question": "自我介绍",
                    "category": "综合能力",
                    "difficulty": "基础",
                    "suggested_answer": "突出亮点"
                }
            ]
        }'''

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.predict_interview_questions(
            resume_content={"basic_info": {"name": "张三"}},
            target_position="软件工程师"
        )

        assert len(result) == 1
        assert result[0]["question"] == "自我介绍"

    async def test_predict_questions_with_company_type(self):
        """测试: 带公司类型预测"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"questions": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        await provider.predict_interview_questions(
            resume_content={},
            target_position="工程师",
            company_type="互联网公司"
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        user_prompt = call_kwargs["messages"][1]["content"]
        assert "互联网公司" in user_prompt

    async def test_predict_questions_without_client(self):
        """测试: 无客户端时返回 mock 问题"""
        provider = XiaomiProvider(api_key="")

        result = await provider.predict_interview_questions(
            resume_content={},
            target_position="Java工程师"
        )

        assert len(result) == 2
        assert result[0]["category"] == "综合能力"
        assert "Java工程师" in result[1]["question"]

    async def test_predict_questions_invalid_json(self):
        """测试: 无效 JSON 返回 mock"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.predict_interview_questions({}, "工程师")

        assert len(result) == 2

    async def test_predict_questions_list_response(self):
        """测试: 直接返回列表格式"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '''[
            {"question": "问题1", "category": "技术", "difficulty": "基础", "suggested_answer": "答案1"}
        ]'''

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.predict_interview_questions({}, "工程师")

        assert len(result) == 1


class TestParseResumeText:
    """简历文本解析测试"""

    async def test_parse_resume_success(self):
        """测试: 成功解析简历文本"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '''{
            "basic_info": {"name": "张三", "phone": "123456"},
            "education": [],
            "work_experience": [],
            "projects": [],
            "skills": []
        }'''

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.parse_resume_text("张三的简历内容")

        assert result["basic_info"]["name"] == "张三"

    async def test_parse_resume_without_client(self):
        """测试: 无客户端时返回 mock 解析"""
        provider = XiaomiProvider(api_key="")

        result = await provider.parse_resume_text("简历内容")

        assert "basic_info" in result
        assert result["basic_info"]["name"] == ""

    async def test_parse_resume_invalid_json(self):
        """测试: 无效 JSON 返回 mock"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.parse_resume_text("简历")

        assert "basic_info" in result

    async def test_parse_resume_long_text_truncated(self):
        """测试: 长文本被截断"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = XiaomiProvider(api_key="test_key")
        provider.client = mock_client

        long_text = "a" * 5000
        await provider.parse_resume_text(long_text)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        user_prompt = call_kwargs["messages"][1]["content"]
        # 长度应该被限制到 4000
        assert len(user_prompt) < 4500


class TestMockMethods:
    """Mock 方法测试"""

    def test_generate_mock_content(self):
        """测试: 生成 mock 简历内容"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._generate_mock_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "张三"
        assert result["basic_info"]["job_intention"] == "工程师"

    def test_mock_optimize_star_method(self):
        """测试: STAR 方法 mock 优化"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "star_method")

        assert "【小米MiMo STAR优化】" in result
        assert "内容" in result

    def test_mock_optimize_quantify(self):
        """测试: 量化 mock 优化"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "quantify")

        assert "【小米MiMo 量化优化】" in result

    def test_mock_optimize_keywords(self):
        """测试: 关键词 mock 优化"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "keywords")

        assert "【小米MiMo 关键词优化】" in result

    def test_mock_optimize_polish(self):
        """测试: 润色 mock 优化"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "polish")

        assert "【小米MiMo 润色】" in result

    def test_mock_optimize_unknown_type(self):
        """测试: 未知类型 mock 优化"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "unknown")

        assert "【小米MiMo优化】" in result

    def test_mock_jd_match(self):
        """测试: mock JD 匹配"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_jd_match()

        assert result["match_score"] == 75
        assert "项目经验" in result["matched_keywords"]
        assert "团队管理" in result["missing_keywords"]

    def test_mock_interview_questions(self):
        """测试: mock 面试问题"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_interview_questions("Java工程师")

        assert len(result) == 2
        assert "Java工程师" in result[1]["question"]

    def test_mock_parsed_resume(self):
        """测试: mock 解析简历"""
        provider = XiaomiProvider(api_key="test_key")

        result = provider._mock_parsed_resume()

        assert "basic_info" in result
        assert result["basic_info"]["name"] == ""
        assert result["education"] == []


class TestProviderProperties:
    """提供商属性测试"""

    def test_provider_name(self):
        """测试: 提供商名称"""
        provider = XiaomiProvider(api_key="test_key")

        assert provider.provider_name == "Xiaomi MiMo"

    def test_is_available_with_key(self):
        """测试: 有 API Key 时可用"""
        provider = XiaomiProvider(api_key="test_key")

        # client 会被创建，所以 is_available 为 True
        assert provider.is_available is True

    def test_is_available_without_key(self):
        """测试: 无 API Key 时不可用"""
        provider = XiaomiProvider(api_key="")

        assert provider.is_available is False

    def test_is_available_with_none_key(self):
        """测试: API Key 为 None 时不可用"""
        provider = XiaomiProvider(api_key=None)

        assert provider.is_available is False
