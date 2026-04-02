"""
个性化生成策略测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ai.enhancers.personalization import (
    UserLevel,
    CareerType,
    UserProfile,
    ContentStrategy,
    PersonalizationEngine,
    create_personalization
)


class TestUserLevel:
    """用户级别枚举测试"""

    def test_user_level_values(self):
        """测试: 用户级别枚举值"""
        assert UserLevel.NEW_GRAD == "new_grad"
        assert UserLevel.JUNIOR == "junior"
        assert UserLevel.SENIOR == "senior"
        assert UserLevel.STAFF == "staff"
        assert UserLevel.LEAD == "lead"
        assert UserLevel.MANAGER == "manager"

    def test_user_level_comparison(self):
        """测试: 用户级别比较"""
        assert UserLevel.NEW_GRAD == UserLevel.NEW_GRAD
        assert UserLevel.NEW_GRAD != UserLevel.SENIOR


class TestCareerType:
    """职业类型枚举测试"""

    def test_career_type_values(self):
        """测试: 职业类型枚举值"""
        assert CareerType.TECHNICAL == "technical"
        assert CareerType.MANAGEMENT == "management"
        assert CareerType.HYBRID == "hybrid"


class TestUserProfile:
    """用户画像数据类测试"""

    def test_create_user_profile_full(self):
        """测试: 创建完整用户画像"""
        profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=5,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="高级工程师",
            strengths=["架构设计", "团队管理"],
            skill_focus=["Java", "Spring"],
            avoid_keywords=["初级", "助理"]
        )

        assert profile.level == UserLevel.SENIOR
        assert profile.years_of_experience == 5
        assert profile.career_type == CareerType.TECHNICAL
        assert profile.target_company_type == "大厂"
        assert len(profile.strengths) == 2

    def test_create_user_profile_minimal(self):
        """测试: 创建最小用户画像"""
        profile = UserProfile(
            level=UserLevel.NEW_GRAD,
            years_of_experience=0,
            career_type=CareerType.TECHNICAL,
            target_company_type="创业公司",
            target_position="前端工程师",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        assert profile.level == UserLevel.NEW_GRAD
        assert profile.years_of_experience == 0
        assert profile.target_position == "前端工程师"


class TestContentStrategy:
    """内容策略数据类测试"""

    def test_create_content_strategy(self):
        """测试: 创建内容策略"""
        strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构", "领导力"],
            structure="成果优先",
            tone="专业",
            highlight_sections=["work", "skills"]
        )

        assert strategy.angle == "专家导向"
        assert len(strategy.keywords_emphasis) == 2
        assert strategy.structure == "成果优先"


class TestPersonalizationEngineInit:
    """个性化引擎初始化测试"""

    def test_init_with_ai_provider(self):
        """测试: 使用 AI 提供商初始化"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        assert engine.ai == mock_ai


class TestCreateStrategy:
    """创建策略测试"""

    def test_new_grad_technical_strategy(self):
        """测试: 应届生技术路线策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.NEW_GRAD,
            years_of_experience=0,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="初级工程师",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "潜力导向"
        assert "学习能力" in strategy.keywords_emphasis
        assert "项目经验" in strategy.keywords_emphasis
        assert "projects" in strategy.highlight_sections

    def test_junior_technical_strategy(self):
        """测试: 初级技术路线策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.JUNIOR,
            years_of_experience=2,
            career_type=CareerType.TECHNICAL,
            target_company_type="外企",
            target_position="软件工程师",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "成长导向"
        assert "快速学习" in strategy.keywords_emphasis
        assert "独立负责" in strategy.keywords_emphasis

    def test_senior_technical_strategy(self):
        """测试: 高级技术路线策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=4,
            career_type=CareerType.TECHNICAL,
            target_company_type="创业公司",
            target_position="高级工程师",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "专家导向"
        assert "技术领导力" in strategy.keywords_emphasis
        assert "架构设计" in strategy.keywords_emphasis

    def test_staff_technical_strategy(self):
        """测试: 资深技术路线策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.STAFF,
            years_of_experience=6,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="资深工程师",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "影响力导向"
        assert "技术影响力" in strategy.keywords_emphasis

    def test_senior_management_strategy(self):
        """测试: 高级管理路线策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=4,
            career_type=CareerType.MANAGEMENT,
            target_company_type="国企",
            target_position="技术经理",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "领导力导向"
        assert "团队管理" in strategy.keywords_emphasis
        assert "项目交付" in strategy.keywords_emphasis

    def test_lead_management_strategy(self):
        """测试: 负责人管理路线策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.LEAD,
            years_of_experience=10,
            career_type=CareerType.MANAGEMENT,
            target_company_type="大厂",
            target_position="技术总监",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "战略导向"
        assert "战略规划" in strategy.keywords_emphasis
        assert "组织建设" in strategy.keywords_emphasis

    def test_default_strategy_for_unknown_level(self):
        """测试: 未知级别使用默认策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        # 使用 Manager 和 Technical 组合（未在策略映射中）
        profile = UserProfile(
            level=UserLevel.MANAGER,
            years_of_experience=15,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="CTO",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        assert strategy.angle == "专业导向"
        assert "专业能力" in strategy.keywords_emphasis

    def test_strategy_includes_custom_skill_focus(self):
        """测试: 策略包含自定义技能重点"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=5,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="高级工程师",
            strengths=[],
            skill_focus=["Go", "Kubernetes", "Istio"],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        # 自定义技能应该被包含
        assert "Go" in strategy.keywords_emphasis
        assert "Kubernetes" in strategy.keywords_emphasis


class TestAdjustForCompany:
    """公司类型调整策略测试"""

    def test_adjust_for_big_company(self):
        """测试: 大厂调整"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        base_strategy = {
            "angle": "专家导向",
            "keywords": ["架构", "技术"],
            "structure": "成果优先",
            "tone": "专业",
            "sections": ["work"]
        }

        adjusted = engine._adjust_for_company("大厂", base_strategy)

        assert "规模化" in adjusted["keywords"]
        assert "高并发" in adjusted["keywords"]
        assert "强调数据和规模" in adjusted["tone"]

    def test_adjust_for_foreign_company(self):
        """测试: 外企调整"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        base_strategy = {
            "angle": "专家导向",
            "keywords": ["架构"],
            "structure": "成果优先",
            "tone": "专业",
            "sections": ["work"]
        }

        adjusted = engine._adjust_for_company("外企", base_strategy)

        assert "跨文化" in adjusted["keywords"]
        assert "全球化" in adjusted["keywords"]
        assert "国际化" in adjusted["tone"]

    def test_adjust_for_startup(self):
        """测试: 创业公司调整"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        base_strategy = {
            "angle": "专家导向",
            "keywords": ["架构"],
            "structure": "成果优先",
            "tone": "专业",
            "sections": ["work"]
        }

        adjusted = engine._adjust_for_company("创业公司", base_strategy)

        assert "从0到1" in adjusted["keywords"]
        assert "多面手" in adjusted["keywords"]
        assert "创业精神" in adjusted["tone"]

    def test_adjust_for_state_owned(self):
        """测试: 国企调整"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        base_strategy = {
            "angle": "专家导向",
            "keywords": ["架构"],
            "structure": "成果优先",
            "tone": "专业",
            "sections": ["work"]
        }

        adjusted = engine._adjust_for_company("国企", base_strategy)

        assert "稳定" in adjusted["keywords"]
        assert "规范" in adjusted["keywords"]
        assert "稳定性" in adjusted["tone"]

    def test_adjust_for_unknown_company(self):
        """测试: 未知公司类型不调整"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        base_strategy = {
            "angle": "专家导向",
            "keywords": ["架构"],
            "structure": "成果优先",
            "tone": "专业",
            "sections": ["work"]
        }

        adjusted = engine._adjust_for_company("未知公司", base_strategy)

        # 不应该有调整
        assert adjusted == base_strategy


class TestEnhanceWithJD:
    """JD 优化策略测试"""

    async def test_enhance_with_jd_success(self):
        """测试: JD 优化成功"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "required_skills": ["Java", "Spring", "MySQL"],
                "preferred_skills": ["Redis"],
                "key_responsibilities": ["后端开发"],
                "culture_keywords": ["协作", "创新"]
            }'''
        )

        engine = PersonalizationEngine(mock_ai)

        base_strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构"],
            structure="成果优先",
            tone="专业",
            highlight_sections=["work"]
        )

        enhanced = await engine.enhance_with_jd(base_strategy, "我们需要Java工程师")

        # JD 关键词应该被合并
        assert "Java" in enhanced.keywords_emphasis
        assert "Spring" in enhanced.keywords_emphasis
        assert "协作" in enhanced.keywords_emphasis
        # 原有关键词也应该保留
        assert "架构" in enhanced.keywords_emphasis

    async def test_enhance_with_jd_empty_response(self):
        """测试: JD 返回空数据"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "required_skills": [],
                "preferred_skills": [],
                "key_responsibilities": [],
                "culture_keywords": []
            }'''
        )

        engine = PersonalizationEngine(mock_ai)

        base_strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构"],
            structure="成果优先",
            tone="专业",
            highlight_sections=["work"]
        )

        enhanced = await engine.enhance_with_jd(base_strategy, "JD")

        # 原有策略应该保留
        assert enhanced.keywords_emphasis == ["架构"]
        assert enhanced.angle == "专家导向"

    async def test_enhance_with_jd_ai_failure(self):
        """测试: AI 调用失败返回原策略"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(side_effect=Exception("AI Error"))

        engine = PersonalizationEngine(mock_ai)

        base_strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构"],
            structure="成果优先",
            tone="专业",
            highlight_sections=["work"]
        )

        enhanced = await engine.enhance_with_jd(base_strategy, "JD")

        # 应该返回原策略
        assert enhanced.keywords_emphasis == ["架构"]
        assert enhanced.angle == "专家导向"
        assert enhanced.structure == "成果优先"

    async def test_enhance_with_jd_invalid_json(self):
        """测试: 无效 JSON 返回原策略"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(return_value="invalid json")

        engine = PersonalizationEngine(mock_ai)

        base_strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构"],
            structure="成果优先",
            tone="专业",
            highlight_sections=["work"]
        )

        enhanced = await engine.enhance_with_jd(base_strategy, "JD")

        # 应该返回原策略
        assert enhanced.keywords_emphasis == ["架构"]


class TestGenerateSystemPrompt:
    """系统 Prompt 生成测试"""

    def test_generate_prompt_potential_angle(self):
        """测试: 潜力导向 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="潜力导向",
            keywords_emphasis=["学习能力", "项目经验"],
            structure="教育优先",
            tone="积极进取",
            highlight_sections=["education"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "资深 HR" in prompt
        assert "应届生" in prompt
        assert "学习能力" in prompt
        assert "项目经验" in prompt
        assert "中文撰写" in prompt
        assert "JSON 格式" in prompt

    def test_generate_prompt_growth_angle(self):
        """测试: 成长导向 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="成长导向",
            keywords_emphasis=["技术深度"],
            structure="技能优先",
            tone="专业可靠",
            highlight_sections=["skills"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "技术经理" in prompt
        assert "成长轨迹" in prompt
        assert "技术深度" in prompt

    def test_generate_prompt_expert_angle(self):
        """测试: 专家导向 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["架构设计"],
            structure="成果优先",
            tone="权威专业",
            highlight_sections=["work"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "技术专家" in prompt
        assert "架构设计" in prompt
        assert "权威专业" in prompt

    def test_generate_prompt_influence_angle(self):
        """测试: 影响力导向 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="影响力导向",
            keywords_emphasis=["技术影响力"],
            structure="影响优先",
            tone="谦逊有力",
            highlight_sections=["work"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "资深架构师" in prompt
        assert "技术影响力" in prompt

    def test_generate_prompt_leadership_angle(self):
        """测试: 领导力导向 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="领导力导向",
            keywords_emphasis=["团队管理"],
            structure="管理成果优先",
            tone="稳重果断",
            highlight_sections=["work"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "技术管理者" in prompt
        assert "团队管理" in prompt

    def test_generate_prompt_strategic_angle(self):
        """测试: 战略导向 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="战略导向",
            keywords_emphasis=["战略规划"],
            structure="战略成果优先",
            tone="高屋建瓴",
            highlight_sections=["work"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "CTO" in prompt or "VP" in prompt
        assert "战略规划" in prompt
        assert "战略思维" in prompt

    def test_generate_prompt_unknown_angle(self):
        """测试: 未知角度使用默认 Prompt"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="未知角度",
            keywords_emphasis=["技能"],
            structure="经历优先",
            tone="专业",
            highlight_sections=["work"]
        )

        prompt = engine.generate_system_prompt(strategy)

        assert "专业简历撰写专家" in prompt

    def test_generate_prompt_limits_keywords(self):
        """测试: 关键词限制为前8个"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        strategy = ContentStrategy(
            angle="专家导向",
            keywords_emphasis=["技能1", "技能2", "技能3", "技能4", "技能5",
                               "技能6", "技能7", "技能8", "技能9", "技能10"],
            structure="成果优先",
            tone="专业",
            highlight_sections=["work"]
        )

        prompt = engine.generate_system_prompt(strategy)

        # 应该只显示前8个
        assert "技能1" in prompt
        assert "技能8" in prompt
        # 技能9和10可能不在（取决于截断）
        keywords_line = [line for line in prompt.split('\n') if '重点关键词' in line][0]
        assert keywords_line.count("技能") <= 8


class TestCreatePersonalization:
    """便捷函数测试"""

    def test_create_personalization_full(self):
        """测试: 完整参数创建画像"""
        profile = create_personalization(
            level="senior",
            years=5,
            career_type="technical",
            target_company="大厂",
            target_position="高级工程师",
            strengths=["架构"],
            skill_focus=["Go"],
            avoid_keywords=["初级"]
        )

        assert profile.level == UserLevel.SENIOR
        assert profile.years_of_experience == 5
        assert profile.career_type == CareerType.TECHNICAL
        assert profile.target_company_type == "大厂"
        assert profile.target_position == "高级工程师"
        assert profile.strengths == ["架构"]
        assert profile.skill_focus == ["Go"]
        assert profile.avoid_keywords == ["初级"]

    def test_create_personalization_minimal(self):
        """测试: 最小参数创建画像"""
        profile = create_personalization(
            level="new_grad",
            years=0,
            career_type="technical",
            target_company="创业公司",
            target_position="实习生"
        )

        assert profile.level == UserLevel.NEW_GRAD
        assert profile.years_of_experience == 0
        assert profile.career_type == CareerType.TECHNICAL
        assert profile.strengths == []
        assert profile.skill_focus == []
        assert profile.avoid_keywords == []

    def test_create_personalization_invalid_level(self):
        """测试: 无效级别值"""
        with pytest.raises(ValueError):
            create_personalization(
                level="invalid_level",
                years=5,
                career_type="technical",
                target_company="大厂",
                target_position="工程师"
            )

    def test_create_personalization_invalid_career_type(self):
        """测试: 无效职业类型"""
        with pytest.raises(ValueError):
            create_personalization(
                level="senior",
                years=5,
                career_type="invalid_type",
                target_company="大厂",
                target_position="工程师"
            )


class TestStrategyIntegration:
    """策略集成测试"""

    def test_full_strategy_creation_flow(self):
        """测试: 完整策略创建流程"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        # 创建用户画像
        profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=5,
            career_type=CareerType.TECHNICAL,
            target_company_type="大厂",
            target_position="高级工程师",
            strengths=["架构设计"],
            skill_focus=["Go", "Kubernetes"],
            avoid_keywords=[]
        )

        # 生成策略
        strategy = engine.create_strategy(profile)

        # 验证策略内容
        assert strategy.angle == "专家导向"
        assert "架构设计" in strategy.keywords_emphasis
        assert "Go" in strategy.keywords_emphasis
        assert "Kubernetes" in strategy.keywords_emphasis

    def test_strategy_with_hybrid_career_type(self):
        """测试: 混合职业类型策略"""
        mock_ai = MagicMock()
        engine = PersonalizationEngine(mock_ai)

        profile = UserProfile(
            level=UserLevel.SENIOR,
            years_of_experience=5,
            career_type=CareerType.HYBRID,  # 混合类型未在映射中
            target_company_type="大厂",
            target_position="技术经理",
            strengths=[],
            skill_focus=[],
            avoid_keywords=[]
        )

        strategy = engine.create_strategy(profile)

        # 应该使用默认策略
        assert strategy.angle == "专业导向"
