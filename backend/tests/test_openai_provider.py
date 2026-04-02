"""
OpenAI 提供商测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ai.providers.openai_provider import OpenAIProvider


class TestOpenAIProviderInit:
    """OpenAI 提供商初始化测试"""

    def test_init_with_api_key(self):
        """测试: 使用 API Key 初始化"""
        with patch('app.services.ai.providers.openai_provider.AsyncOpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client

            provider = OpenAIProvider(api_key="test_key")

            assert provider.api_key == "test_key"
            assert provider.model == "gpt-4"
            assert provider.client == mock_client
            assert provider.max_tokens == 4000
            assert provider.temperature == 0.7

    def test_init_with_custom_model(self):
        """测试: 使用自定义模型"""
        with patch('app.services.ai.providers.openai_provider.AsyncOpenAI'):
            provider = OpenAIProvider(
                api_key="test_key",
                model="gpt-3.5-turbo"
            )

            assert provider.model == "gpt-3.5-turbo"

    def test_init_with_custom_max_tokens(self):
        """测试: 自定义 max_tokens"""
        with patch('app.services.ai.providers.openai_provider.AsyncOpenAI'):
            provider = OpenAIProvider(
                api_key="test_key",
                max_tokens=8000
            )

            assert provider.max_tokens == 8000

    def test_init_with_custom_temperature(self):
        """测试: 自定义 temperature"""
        with patch('app.services.ai.providers.openai_provider.AsyncOpenAI'):
            provider = OpenAIProvider(
                api_key="test_key",
                temperature=0.5
            )

            assert provider.temperature == 0.5

    def test_init_without_api_key(self):
        """测试: 无 API Key 初始化"""
        provider = OpenAIProvider(api_key="")

        assert provider.client is None

    def test_init_with_none_api_key(self):
        """测试: API Key 为 None"""
        provider = OpenAIProvider(api_key=None)

        assert provider.client is None


class TestGenerateResumeContent:
    """生成简历内容测试 - 三元协同Agent架构（带降级）"""

    async def test_generate_full_three_phase_flow(self):
        """测试: 完整的三阶段流程"""
        dialogue_response = MagicMock()
        dialogue_response.choices = [MagicMock()]
        dialogue_response.choices[0].message.content = '{"key_strengths": ["Python"], "skill_gaps": [], "highlight_areas": ["技术"], "industry_keywords": ["AI"]}'

        planning_response = MagicMock()
        planning_response.choices = [MagicMock()]
        planning_response.choices[0].message.content = '{"basic_info_strategy": "简洁", "experience_strategy": "STAR", "education_strategy": "倒序", "skills_strategy": "分类", "projects_strategy": "突出成果"}'

        execution_response = MagicMock()
        execution_response.choices = [MagicMock()]
        execution_response.choices[0].message.content = '{"basic_info": {"name": "测试"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=[
            dialogue_response,
            planning_response,
            execution_response
        ])

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="软件工程师"
        )

        assert result["basic_info"]["name"] == "测试"

    async def test_generate_without_client(self):
        """测试: 无客户端时返回 mock 内容"""
        provider = OpenAIProvider(api_key="")

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "张三"
        assert result["basic_info"]["job_intention"] == "工程师"

    async def test_generate_with_fallback_on_error(self):
        """测试: 发生错误时降级到简化生成"""
        # 对话阶段失败
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        # 简化生成成功
        simplified_response = MagicMock()
        simplified_response.choices = [MagicMock()]
        simplified_response.choices[0].message.content = '{"basic_info": {"name": "简化版"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[
                Exception("API Error"),  # 第一次调用失败
                simplified_response      # 简化生成成功
            ]
        )

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "简化版"

    async def test_generate_dialogue_phase_json_error(self):
        """测试: 对话阶段 JSON 解析错误返回默认值"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid json"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider._dialogue_phase(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            language="zh"
        )

        assert result["user_info"]["basic_info"]["name"] == "张三"
        assert result["analysis"]["key_strengths"] == []
        assert result["analysis"]["highlight_areas"] == ["工程师"]

    async def test_generate_execution_phase_json_error(self):
        """测试: 执行阶段 JSON 解析错误返回降级内容"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid json"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        plan = {
            "user_info": {"basic_info": {"name": "张三"}, "education": []},
            "target_position": "工程师",
            "plan": {}
        }

        result = await provider._execution_phase(plan, "zh")

        # 返回降级内容
        assert "basic_info" in result

    async def test_generate_execution_phase_missing_required_fields(self):
        """测试: 执行阶段缺少必需字段时补充"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        # 返回缺少部分字段的内容
        mock_response.choices[0].message.content = '{"basic_info": {"name": "测试"}, "education": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        plan = {
            "user_info": {"work_experience": [{"company": "ABC"}], "projects": [], "skills": ["Python"]},
            "target_position": "工程师",
            "plan": {}
        }

        result = await provider._execution_phase(plan, "zh")

        # 缺失字段应该被补充
        assert "basic_info" in result
        assert "work_experience" in result
        assert "projects" in result
        assert "skills" in result

    async def test_generate_simplified_without_client(self):
        """测试: 简化生成无客户端时返回 mock"""
        provider = OpenAIProvider(api_key="")

        result = await provider._generate_simplified(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            language="zh"
        )

        assert result["basic_info"]["name"] == "张三"

    async def test_generate_simplified_success(self):
        """测试: 简化生成成功"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "简化版"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider._generate_simplified(
            user_info={},
            target_position="工程师",
            language="zh"
        )

        assert result["basic_info"]["name"] == "简化版"

    async def test_generate_simplified_english(self):
        """测试: 简化生成英文"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        await provider._generate_simplified({}, "Engineer", "en")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "Write in English" in system_prompt

    async def test_build_fallback_content(self):
        """测试: 构建降级内容"""
        provider = OpenAIProvider(api_key="test_key")

        user_info = {
            "basic_info": {"name": "张三"},
            "education": [],
            "work_experience": [],
            "projects": [],
            "skills": ["Python"]
        }

        result = provider._build_fallback_content(user_info)

        assert result["basic_info"]["name"] == "张三"
        assert result["skills"] == ["Python"]
        assert result["_fallback"] is True


class TestDialoguePhase:
    """对话阶段测试"""

    async def test_dialogue_phase_success(self):
        """测试: 对话阶段成功"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"key_strengths": ["沟通"], "skill_gaps": [], "highlight_areas": [], "industry_keywords": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider._dialogue_phase(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            language="zh"
        )

        assert result["user_info"]["basic_info"]["name"] == "张三"
        assert result["target_position"] == "工程师"
        assert "analysis" in result

    async def test_dialogue_phase_with_temperature(self):
        """测试: 对话阶段使用正确的温度参数"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"key_strengths": [], "skill_gaps": [], "highlight_areas": [], "industry_keywords": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        await provider._dialogue_phase({}, "工程师", "zh")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["temperature"] == 0.3


class TestPlanningPhase:
    """规划阶段测试"""

    async def test_planning_phase_success(self):
        """测试: 规划阶段成功"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info_strategy": "简洁", "experience_strategy": "STAR"}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        context = {
            "user_info": {},
            "target_position": "工程师",
            "analysis": {},
            "language": "zh"
        }

        result = await provider._planning_phase(context, "professional")

        assert "plan" in result
        assert result["style"] == "professional"

    async def test_planning_phase_with_temperature(self):
        """测试: 规划阶段使用正确的温度参数"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info_strategy": "简洁"}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        await provider._planning_phase({
            "user_info": {},
            "target_position": "工程师",
            "analysis": {},
            "language": "zh"
        }, "professional")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["temperature"] == 0.5


class TestExecutionPhase:
    """执行阶段测试"""

    async def test_execution_phase_success(self):
        """测试: 执行阶段成功"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "李四"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        plan = {
            "user_info": {},
            "target_position": "工程师",
            "plan": {"basic_info_strategy": "简洁"}
        }

        result = await provider._execution_phase(plan, "zh")

        assert result["basic_info"]["name"] == "李四"

    async def test_execution_phase_chinese(self):
        """测试: 执行阶段中文"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        await provider._execution_phase({"user_info": {}, "target_position": "工程师", "plan": {}}, "zh")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        system_prompt = call_kwargs["messages"][0]["content"]
        assert "中文撰写" in system_prompt

    async def test_execution_phase_with_max_tokens(self):
        """测试: 执行阶段使用 max_tokens"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key", max_tokens=8000)
        provider.client = mock_client

        await provider._execution_phase({"user_info": {}, "target_position": "工程师", "plan": {}}, "zh")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["max_tokens"] == 8000


class TestOptimizeContent:
    """内容优化测试"""

    async def test_optimize_star_method(self):
        """测试: STAR 法则优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "STAR优化后内容"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.optimize_content(
            original="负责项目开发",
            optimization_type="star_method"
        )

        assert result == "STAR优化后内容"

    async def test_optimize_quantify(self):
        """测试: 量化优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "量化后内容"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.optimize_content(
            original="提升性能",
            optimization_type="quantify"
        )

        assert result == "量化后内容"

    async def test_optimize_keywords(self):
        """测试: 关键词优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "关键词优化后"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
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

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.optimize_content(
            original="原始内容",
            optimization_type="polish"
        )

        assert result == "润色后内容"

    async def test_optimize_with_context(self):
        """测试: 带上下文优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "优化结果"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
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
        provider = OpenAIProvider(api_key="")

        result = await provider.optimize_content(
            original="原始内容",
            optimization_type="polish"
        )

        assert "【润色后】" in result
        assert "AI优化" in result


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

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.analyze_jd_match(
            resume_content={"skills": ["Python", "Django"]},
            job_description="需要 Python、Django、Redis 经验"
        )

        assert result["match_score"] == 85

    async def test_analyze_jd_match_without_client(self):
        """测试: 无客户端时返回默认结果"""
        provider = OpenAIProvider(api_key="")

        result = await provider.analyze_jd_match(
            resume_content={},
            job_description="JD"
        )

        assert result["match_score"] == 85
        assert len(result["suggestions"]) == 2


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

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.predict_interview_questions(
            resume_content={"basic_info": {"name": "张三"}},
            target_position="软件工程师"
        )

        assert len(result) == 1

    async def test_predict_questions_with_company_type(self):
        """测试: 带公司类型预测"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"questions": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
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
        provider = OpenAIProvider(api_key="")

        result = await provider.predict_interview_questions(
            resume_content={},
            target_position="Java工程师"
        )

        assert len(result) == 2
        assert "Java工程师" in result[1]["question"]

    async def test_predict_questions_list_response(self):
        """测试: 直接返回列表格式"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '''[
            {"question": "问题1", "category": "技术", "difficulty": "基础", "suggested_answer": "答案1"}
        ]'''

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
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

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        result = await provider.parse_resume_text("张三的简历内容")

        assert result["basic_info"]["name"] == "张三"

    async def test_parse_resume_without_client(self):
        """测试: 无客户端时返回 mock 解析"""
        provider = OpenAIProvider(api_key="")

        result = await provider.parse_resume_text("简历内容")

        assert "basic_info" in result

    async def test_parse_resume_long_text_truncated(self):
        """测试: 长文本被截断"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")
        provider.client = mock_client

        long_text = "a" * 5000
        await provider.parse_resume_text(long_text)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        user_prompt = call_kwargs["messages"][1]["content"]
        # 长度应该被限制到 4000
        assert len(user_prompt) < 4500


class TestMockMethods:
    """Mock 方法测试"""

    def test_mock_interview_questions(self):
        """测试: mock 面试问题"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._mock_interview_questions("Java工程师")

        assert len(result) == 2
        assert result[0]["category"] == "综合能力"
        assert "Java工程师" in result[1]["question"]

    def test_mock_parsed_resume(self):
        """测试: mock 解析简历"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._mock_parsed_resume("任意文本")

        assert "basic_info" in result
        assert result["basic_info"]["name"] == ""

    def test_generate_mock_content(self):
        """测试: 生成 mock 简历内容"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._generate_mock_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "张三"
        assert result["basic_info"]["job_intention"] == "工程师"

    def test_mock_optimize(self):
        """测试: mock 优化"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._mock_optimize("原始内容", "polish")

        assert "【润色后】" in result
        assert "AI优化" in result

    def test_mock_optimize_star_method(self):
        """测试: STAR 方法 mock 优化"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "star_method")

        assert "【优化后】" in result

    def test_mock_optimize_quantify(self):
        """测试: 量化 mock 优化"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "quantify")

        assert "【量化后】" in result

    def test_mock_optimize_keywords(self):
        """测试: 关键词 mock 优化"""
        provider = OpenAIProvider(api_key="test_key")

        result = provider._mock_optimize("内容", "keywords")

        assert "【关键词优化】" in result


class TestProviderProperties:
    """提供商属性测试"""

    def test_provider_name(self):
        """测试: 提供商名称"""
        provider = OpenAIProvider(api_key="test_key")

        assert provider.provider_name == "OpenAI"

    def test_is_available_with_key(self):
        """测试: 有 API Key 时可用"""
        provider = OpenAIProvider(api_key="test_key")

        assert provider.is_available is True

    def test_is_available_without_key(self):
        """测试: 无 API Key 时不可用"""
        provider = OpenAIProvider(api_key="")

        assert provider.is_available is False

    def test_is_available_with_none_key(self):
        """测试: API Key 为 None 时不可用"""
        provider = OpenAIProvider(api_key=None)

        assert provider.is_available is False
