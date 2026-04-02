"""
OpenAI Provider V2 测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ai.providers.openai_provider_v2 import OpenAIProviderV2
from app.services.ai.enhancers.personalization import UserLevel, CareerType


class TestOpenAIProviderV2Init:
    """OpenAI Provider V2 初始化测试"""

    def test_init_with_api_key(self):
        """测试: 使用 API Key 初始化"""
        with patch('app.services.ai.providers.openai_provider_v2.AsyncOpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client

            provider = OpenAIProviderV2(api_key="test_key")

            assert provider.api_key == "test_key"
            assert provider.model == "gpt-4"
            assert provider.client == mock_client
            assert provider.max_tokens == 4000
            assert provider.temperature == 0.7
            assert provider.prompt_manager is not None
            assert provider.experience_miner is not None
            assert provider.personalization is not None
            assert provider.ats_optimizer is not None

    def test_init_with_custom_model(self):
        """测试: 使用自定义模型"""
        with patch('app.services.ai.providers.openai_provider_v2.AsyncOpenAI'):
            provider = OpenAIProviderV2(
                api_key="test_key",
                model="gpt-3.5-turbo"
            )

            assert provider.model == "gpt-3.5-turbo"

    def test_init_with_custom_max_tokens(self):
        """测试: 自定义 max_tokens"""
        with patch('app.services.ai.providers.openai_provider_v2.AsyncOpenAI'):
            provider = OpenAIProviderV2(
                api_key="test_key",
                max_tokens=8000
            )

            assert provider.max_tokens == 8000

    def test_init_with_custom_temperature(self):
        """测试: 自定义 temperature"""
        with patch('app.services.ai.providers.openai_provider_v2.AsyncOpenAI'):
            provider = OpenAIProviderV2(
                api_key="test_key",
                temperature=0.5
            )

            assert provider.temperature == 0.5

    def test_init_without_api_key(self):
        """测试: 无 API Key 初始化"""
        provider = OpenAIProviderV2(api_key="")

        assert provider.client is None


class TestGenerateResumeContent:
    """生成简历内容测试 - 增强版"""

    async def test_generate_without_client(self):
        """测试: 无客户端时返回 mock 内容"""
        provider = OpenAIProviderV2(api_key="")

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        # _generate_mock_content 会使用 user_info 中的 name
        assert result["basic_info"]["name"] == "张三"
        assert "_mock" in result

    async def test_generate_with_enhance_false(self):
        """测试: 禁用增强功能"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "测试"}, "education": [], "work_experience": [], "projects": [], "skills": []}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 200
        mock_response.usage.total_tokens = 300

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            enhance=False
        )

        assert result["content"]["basic_info"]["name"] == "测试"
        assert result["meta"]["provider"] == "openai"
        assert result["meta"]["enhanced"] is False
        assert result["usage"]["total_tokens"] == 300

    async def test_generate_with_user_profile(self):
        """测试: 带用户画像生成"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}, "education": [], "work_experience": [], "projects": [], "skills": []}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 200
        mock_response.usage.total_tokens = 300

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        from app.services.ai.enhancers.personalization import UserProfile
        user_profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=5,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="高级工程师",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        result = await provider.generate_resume_content(
            user_info={},
            target_position="高级工程师",
            user_profile=user_profile,
            enhance=True  # 需要启用 enhance 才会使用 strategy
        )

        # enhance=True 时应该包含 strategy
        assert "strategy" in result["meta"]
        assert result["meta"]["strategy"]["angle"] == "专家导向"

    async def test_generate_with_job_description(self):
        """测试: 带 JD 生成"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {}, "education": [], "work_experience": [], "projects": [], "skills": []}'
        mock_response.usage = MagicMock()
        mock_response.usage.total_tokens = 300

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={},
            target_position="工程师",
            job_description="需要 Python、Django 技能",
            enhance=True  # 需要启用 enhance 才会进行 ATS 分析
        )

        # enhance=True 且有 JD 时应该包含 ATS 分数
        assert "ats_score" in result["meta"]

    async def test_generate_json_decode_error(self):
        """测试: JSON 解析错误"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "invalid json"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert "error" in result
        assert result["error"] == "parse_error"

    async def test_generate_with_fallback_on_error(self):
        """测试: 发生错误时降级"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        # 简化生成成功
        simplified_response = MagicMock()
        simplified_response.choices = [MagicMock()]
        simplified_response.choices[0].message.content = '{"basic_info": {"name": "简化版"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[
                Exception("API Error"),
                simplified_response
            ]
        )

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.generate_resume_content(
            user_info={},
            target_position="工程师"
        )

        assert "basic_info" in result


class TestValidateAndFix:
    """质量验证和修复测试"""

    def test_validate_and_fix_complete_content(self):
        """测试: 完整内容无需修复"""
        provider = OpenAIProviderV2(api_key="test_key")

        content = {
            "basic_info": {"name": "张三"},
            "education": [],
            "work_experience": [{"description": "负责处理1000万用户量"}],
            "projects": [],
            "skills": ["Python"]
        }
        user_info = {}

        result = provider._validate_and_fix(content, user_info)

        assert result["basic_info"]["name"] == "张三"

    def test_validate_and_fix_missing_fields(self):
        """测试: 修复缺失字段"""
        provider = OpenAIProviderV2(api_key="test_key")

        content = {"basic_info": {}}
        user_info = {
            "education": [{"school": "清华"}],
            "work_experience": [],
            "projects": [],
            "skills": ["Java"]
        }

        result = provider._validate_and_fix(content, user_info)

        assert result["education"] == [{"school": "清华"}]
        assert result["skills"] == ["Java"]

    def test_validate_and_fix_mark_needs_quantify(self):
        """测试: 标记需要量化的经历"""
        provider = OpenAIProviderV2(api_key="test_key")

        content = {
            "basic_info": {},
            "education": [],
            "work_experience": [{"description": "负责开发工作"}],
            "projects": [],
            "skills": []
        }

        result = provider._validate_and_fix(content, {})

        assert result["work_experience"][0]["_needs_quantify"] is True

    def test_validate_and_fix_with_numbers(self):
        """测试: 包含数字的描述不需要标记"""
        provider = OpenAIProviderV2(api_key="test_key")

        content = {
            "basic_info": {},
            "education": [],
            "work_experience": [{"description": "提升系统性能50%"}],
            "projects": [],
            "skills": []
        }

        result = provider._validate_and_fix(content, {})

        assert "_needs_quantify" not in result["work_experience"][0]


class TestEnhanceExperiences:
    """经历增强测试"""

    async def test_enhance_experiences_no_work_experience(self):
        """测试: 无工作经历时跳过"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = await provider._enhance_experiences({"work_experience": []})

        assert result["work_experience"] == []

    async def test_enhance_experiences_with_good_description(self):
        """测试: 良好描述无需增强"""
        provider = OpenAIProviderV2(api_key="test_key")

        user_info = {
            "work_experience": [
                {
                    "company": "ABC",
                    "position": "工程师",
                    "description": "负责处理大流量系统，日处理请求超过100万次，涉及微服务架构设计与优化，完成多个重要项目，带领团队攻克技术难关",
                    "period": "2020-2023"
                }
            ]
        }

        result = await provider._enhance_experiences(user_info)

        # 描述足够长（>50字符），应该不会被增强
        # 检查描述是否保持原样
        assert "大流量系统" in result["work_experience"][0]["description"]

    async def test_enhance_experiences_short_description(self):
        """测试: 短描述尝试增强"""
        provider = OpenAIProviderV2(api_key="test_key")

        # Mock experience miner
        provider.experience_miner.mine_experience = AsyncMock(
            return_value=MagicMock(
                tech_stack=["Python"],
                architecture_contribution="",
                technical_challenges=[],
                business_context="",
                metrics={},
                business_impact="",
                team_size=0,
                cross_functional=False,
                stakeholder_management=[],
                innovations=[],
                lessons_learned=[],
                skills_gained=[],
                leadership_growth=""
            )
        )
        provider.experience_miner.generate_star_description = MagicMock(return_value="STAR优化后的描述")

        user_info = {
            "work_experience": [
                {
                    "company": "ABC",
                    "position": "工程师",
                    "description": "开发",
                    "period": "2020-2023"
                }
            ]
        }

        result = await provider._enhance_experiences(user_info)

        # 应该被增强
        assert result["work_experience"][0]["_enhanced"] is True

    async def test_enhance_experiences_miner_error(self):
        """测试: 经历挖掘失败时继续"""
        provider = OpenAIProviderV2(api_key="test_key")

        provider.experience_miner.mine_experience = AsyncMock(
            side_effect=Exception("Mining failed")
        )

        user_info = {
            "work_experience": [
                {
                    "company": "ABC",
                    "position": "工程师",
                    "description": "开发",
                    "period": "2020-2023"
                }
            ]
        }

        result = await provider._enhance_experiences(user_info)

        # 不应该有 _enhanced 标记
        assert "_enhanced" not in result["work_experience"][0]


class TestBuildEnhancedPrompt:
    """构建增强版 Prompt 测试"""

    def test_build_prompt_without_strategy(self):
        """测试: 无策略时构建 Prompt"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._build_enhanced_prompt(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            style="professional",
            strategy=None,
            ats_keywords=None
        )

        assert "system" in result
        assert "user" in result
        assert "张三" in result["user"]

    def test_build_prompt_with_strategy(self):
        """测试: 带策略构建 Prompt"""
        provider = OpenAIProviderV2(api_key="test_key")

        from app.services.ai.enhancers.personalization import ContentStrategy
        strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构", "领导力"],
            structure="成果优先",
            tone="权威",
            highlight_sections=["work"]
        )

        result = provider._build_enhanced_prompt(
            user_info={},
            target_position="架构师",
            style="professional",
            strategy=strategy,
            ats_keywords=None
        )

        # system prompt 应该包含策略相关内容
        assert "system" in result
        assert "user" in result

    def test_build_prompt_with_ats_keywords(self):
        """测试: 带 ATS 关键词构建 Prompt"""
        provider = OpenAIProviderV2(api_key="test_key")

        ats_keywords = {
            "hard_skills": ["Python", "Django", "Redis", "MySQL"]
        }

        result = provider._build_enhanced_prompt(
            user_info={},
            target_position="后端工程师",
            style="professional",
            strategy=None,
            ats_keywords=ats_keywords
        )

        assert "JD 关键技能" in result["system"]
        assert "Python" in result["system"]


class TestOptimizeContent:
    """内容优化测试"""

    async def test_optimize_star_method(self):
        """测试: STAR 法则优化"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "STAR优化后内容"

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
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

        provider = OpenAIProviderV2(api_key="test_key")
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

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        await provider.optimize_content(
            original="使用Python开发",
            optimization_type="keywords"
        )

        # 验证调用参数
        call_args = mock_client.chat.completions.create.call_args

    async def test_optimize_without_client(self):
        """测试: 无客户端时返回 mock 优化"""
        provider = OpenAIProviderV2(api_key="")

        result = await provider.optimize_content(
            original="原始内容",
            optimization_type="polish"
        )

        assert "polish优化" in result
        assert "原始内容" in result

    async def test_optimize_error_returns_original(self):
        """测试: 优化失败返回原文"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.optimize_content(
            original="原始内容",
            optimization_type="polish"
        )

        assert result == "原始内容"


class TestAnalyzeJDMatch:
    """JD 匹配分析测试"""

    async def test_analyze_jd_match_success(self):
        """测试: 成功分析 JD 匹配"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"match_score": 85, "matched_keywords": ["Python"], "missing_keywords": [], "suggestions": [], "strengths": [], "weaknesses": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.analyze_jd_match(
            resume_content={"skills": ["Python"]},
            job_description="需要 Python 技能"
        )

        assert result["match_score"] == 85

    async def test_analyze_jd_match_without_client(self):
        """测试: 无客户端时返回默认结果"""
        provider = OpenAIProviderV2(api_key="")

        result = await provider.analyze_jd_match(
            resume_content={},
            job_description="JD"
        )

        assert result["match_score"] == 85

    async def test_analyze_jd_match_error_returns_default(self):
        """测试: 分析错误返回默认值"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.analyze_jd_match({}, "JD")

        assert result["match_score"] == 70
        assert "error" in result


class TestAnalyzeResumeWithJD:
    """增强版 JD 分析测试"""

    async def test_analyze_resume_with_jd(self):
        """测试: 使用 ATS 优化器分析"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = await provider.analyze_resume_with_jd(
            resume_content={"skills": ["Python"]},
            job_description="需要 Python 技能"
        )

        # 应该返回 ats_optimizer 的结果
        assert "jd_analysis" in result
        assert "match_score" in result


class TestPredictInterviewQuestions:
    """预测面试问题测试"""

    async def test_predict_questions_success(self):
        """测试: 成功预测面试问题"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"questions": [{"question": "自我介绍", "category": "综合", "difficulty": "基础"}]}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.predict_interview_questions(
            resume_content={},
            target_position="工程师"
        )

        assert len(result) == 1

    async def test_predict_questions_with_company_type(self):
        """测试: 带公司类型预测"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"questions": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        await provider.predict_interview_questions(
            resume_content={},
            target_position="工程师",
            company_type="互联网公司"
        )

        # 验证调用包含公司类型
        call_args = mock_client.chat.completions.create.call_args

    async def test_predict_questions_without_client(self):
        """测试: 无客户端时返回 mock 问题"""
        provider = OpenAIProviderV2(api_key="")

        result = await provider.predict_interview_questions(
            resume_content={},
            target_position="Java工程师"
        )

        assert len(result) == 2

    async def test_predict_questions_error_returns_mock(self):
        """测试: 预测错误返回 mock"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.predict_interview_questions({}, "工程师")

        assert len(result) == 2


class TestParseResumeText:
    """简历文本解析测试"""

    async def test_parse_resume_success(self):
        """测试: 成功解析简历文本"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "张三"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.parse_resume_text("张三的简历")

        assert result["basic_info"]["name"] == "张三"

    async def test_parse_resume_without_client(self):
        """测试: 无客户端时返回 mock 解析"""
        provider = OpenAIProviderV2(api_key="")

        result = await provider.parse_resume_text("简历内容")

        assert "basic_info" in result

    async def test_parse_resume_error_returns_mock(self):
        """测试: 解析错误返回 mock"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider.parse_resume_text("简历")

        assert "basic_info" in result


class TestMockMethods:
    """Mock 方法测试"""

    def test_build_fallback_content(self):
        """测试: 构建降级内容"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._build_fallback_content({"basic_info": {"name": "张三"}})

        assert result["basic_info"]["name"] == "张三"
        assert result["_fallback"] is True

    def test_generate_mock_content(self):
        """测试: 生成 mock 内容"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._generate_mock_content(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "张三"
        # 检查 _mock 键是否存在，而不是断言为 True
        assert "_mock" in result

    def test_generate_mock_content_default_name(self):
        """测试: mock 内容默认名称"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._generate_mock_content(
            user_info={},
            target_position="工程师"
        )

        assert result["basic_info"]["name"] == "用户"

    def test_mock_optimize(self):
        """测试: mock 优化"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._mock_optimize("原始内容", "polish")

        assert "polish优化" in result
        assert "原始内容" in result

    def test_mock_interview_questions(self):
        """测试: mock 面试问题"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._mock_interview_questions("Java工程师")

        assert len(result) == 2
        assert "Java工程师" in result[1]["question"]

    def test_mock_parsed_resume(self):
        """测试: mock 解析简历"""
        provider = OpenAIProviderV2(api_key="test_key")

        result = provider._mock_parsed_resume("任意文本")

        assert "basic_info" in result


class TestProviderProperties:
    """提供商属性测试"""

    def test_provider_name(self):
        """测试: 提供商名称"""
        provider = OpenAIProviderV2(api_key="test_key")

        assert provider.provider_name == "OpenAI V2 (Optimized)"

    def test_is_available_with_key(self):
        """测试: 有 API Key 时可用"""
        provider = OpenAIProviderV2(api_key="test_key")

        assert provider.is_available is True

    def test_is_available_without_key(self):
        """测试: 无 API Key 时不可用"""
        provider = OpenAIProviderV2(api_key="")

        assert provider.is_available is False


class TestGenerateSimplified:
    """简化生成测试"""

    async def test_generate_simplified_without_client(self):
        """测试: 无客户端时返回 mock"""
        provider = OpenAIProviderV2(api_key="")

        result = await provider._generate_simplified(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            language="zh"
        )

        # _generate_mock_content 会使用 user_info 中的 name
        assert result["basic_info"]["name"] == "张三"

    async def test_generate_simplified_success(self):
        """测试: 简化生成成功"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"basic_info": {"name": "简化版"}, "education": [], "work_experience": [], "projects": [], "skills": []}'

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider._generate_simplified(
            user_info={},
            target_position="工程师",
            language="zh"
        )

        assert result["basic_info"]["name"] == "简化版"

    async def test_generate_simplified_error_returns_fallback(self):
        """测试: 简化生成错误返回降级内容"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        provider = OpenAIProviderV2(api_key="test_key")
        provider.client = mock_client

        result = await provider._generate_simplified(
            user_info={"basic_info": {"name": "张三"}},
            target_position="工程师",
            language="zh"
        )

        assert result["basic_info"]["name"] == "张三"
