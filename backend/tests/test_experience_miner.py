"""
经历挖掘器测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ai.enhancers.experience_miner import (
    ExperienceDimensions,
    ExperienceMiner,
    mine_work_experience
)


class TestExperienceDimensions:
    """经历五维度数据类测试"""

    def test_create_full_dimensions(self):
        """测试: 创建完整的五维度数据"""
        dims = ExperienceDimensions(
            tech_stack=["Python", "Django"],
            architecture_contribution="微服务架构设计",
            technical_challenges=["高并发处理", "数据库优化"],
            business_context="电商交易平台",
            metrics={"before": "100", "after": "1000", "unit": "QPS"},
            business_impact="提升系统性能10倍",
            team_size=10,
            cross_functional=True,
            stakeholder_management=["产品经理", "设计师"],
            innovations=["引入缓存机制", "CDN加速"],
            lessons_learned=["缓存一致性", "监控告警"],
            skills_gained=["架构设计", "团队管理"],
            leadership_growth="带领5人小组完成项目"
        )

        assert dims.tech_stack == ["Python", "Django"]
        assert dims.architecture_contribution == "微服务架构设计"
        assert dims.technical_challenges == ["高并发处理", "数据库优化"]
        assert dims.business_context == "电商交易平台"
        assert dims.metrics == {"before": "100", "after": "1000", "unit": "QPS"}
        assert dims.business_impact == "提升系统性能10倍"
        assert dims.team_size == 10
        assert dims.cross_functional is True
        assert len(dims.stakeholder_management) == 2

    def test_create_empty_dimensions(self):
        """测试: 创建空维度数据"""
        dims = ExperienceDimensions(
            tech_stack=[],
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

        assert dims.tech_stack == []
        assert dims.team_size == 0
        assert dims.cross_functional is False

    def test_dimensions_with_partial_data(self):
        """测试: 创建部分数据的维度"""
        dims = ExperienceDimensions(
            tech_stack=["React"],
            architecture_contribution="前端组件开发",
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

        assert len(dims.tech_stack) == 1
        assert dims.architecture_contribution == "前端组件开发"


class TestExperienceMinerInit:
    """经历挖掘器初始化测试"""

    def test_init_with_ai_provider(self):
        """测试: 使用 AI 提供商初始化"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        assert miner.ai == mock_ai


class TestMineExperience:
    """深度挖掘经历测试"""

    async def test_mine_experience_success(self):
        """测试: 成功挖掘经历"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "tech": {
                    "stack": ["Python", "Django"],
                    "architecture": "RESTful API 设计",
                    "challenges": ["高并发", "数据一致性"]
                },
                "business": {
                    "context": "电商平台",
                    "metrics": {"before": "100", "after": "1000", "unit": "订单/秒"},
                    "impact": "提升10倍处理能力"
                },
                "collaboration": {
                    "team_size": 8,
                    "cross_functional": true,
                    "stakeholders": ["产品", "设计"]
                },
                "innovation": {
                    "innovations": ["引入Redis缓存"],
                    "lessons": ["缓存预热"]
                },
                "growth": {
                    "skills": ["架构设计"],
                    "leadership": "技术负责人"
                }
            }'''
        )

        miner = ExperienceMiner(mock_ai)
        result = await miner.mine_experience(
            title="后端工程师",
            company="某公司",
            description="负责电商平台后端开发",
            period="2020-2023"
        )

        assert result.tech_stack == ["Python", "Django"]
        assert result.architecture_contribution == "RESTful API 设计"
        assert result.team_size == 8
        assert result.cross_functional is True

    async def test_mine_experience_with_context(self):
        """测试: 带上下文挖掘"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "tech": {"stack": ["Java"], "architecture": "", "challenges": []},
                "business": {"context": "", "metrics": {}, "impact": ""},
                "collaboration": {"team_size": 0, "cross_functional": false, "stakeholders": []},
                "innovation": {"innovations": [], "lessons": []},
                "growth": {"skills": [], "leadership": ""}
            }'''
        )

        miner = ExperienceMiner(mock_ai)
        result = await miner.mine_experience(
            title="Java开发",
            company="某公司",
            description="Java后端开发",
            context={"industry": "金融", "company_size": "1000+"}
        )

        mock_ai.optimize_content.assert_called_once()
        assert "金融" in str(mock_ai.optimize_content.call_args)

    async def test_mine_experience_ai_failure(self):
        """测试: AI 调用失败返回默认值"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(side_effect=Exception("AI Error"))

        miner = ExperienceMiner(mock_ai)
        result = await miner.mine_experience(
            title="测试职位",
            company="测试公司",
            description="测试描述"
        )

        # 返回默认值
        assert result.tech_stack == []
        assert result.team_size == 0
        assert result.cross_functional is False

    async def test_mine_experience_invalid_json(self):
        """测试: 无效 JSON 返回默认值"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(return_value="invalid json")

        miner = ExperienceMiner(mock_ai)
        result = await miner.mine_experience(
            title="测试职位",
            company="测试公司",
            description="测试描述"
        )

        assert result.tech_stack == []

    async def test_mine_experience_partial_json(self):
        """测试: 部分 JSON 数据解析"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "tech": {
                    "stack": ["React"]
                }
            }'''
        )

        miner = ExperienceMiner(mock_ai)
        result = await miner.mine_experience(
            title="前端工程师",
            company="某公司",
            description="前端开发"
        )

        assert result.tech_stack == ["React"]
        assert result.architecture_contribution == ""


class TestBuildMiningPrompt:
    """挖掘 Prompt 构建测试"""

    def test_build_prompt_with_all_fields(self):
        """测试: 构建包含所有字段的 Prompt"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        prompt = miner._build_mining_prompt(
            title="高级工程师",
            company="科技公司",
            description="负责系统架构",
            period="2020-2023",
            context={"industry": "互联网", "size": "500人"}
        )

        assert "高级工程师" in prompt
        assert "科技公司" in prompt
        assert "负责系统架构" in prompt
        assert "2020-2023" in prompt
        assert "互联网" in prompt

    def test_build_prompt_minimal(self):
        """测试: 构建最小 Prompt"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        prompt = miner._build_mining_prompt(
            title="工程师",
            company="公司",
            description="开发",
            period="",
            context=None
        )

        assert "工程师" in prompt
        assert "公司" in prompt
        assert "开发" in prompt

    def test_build_prompt_without_period(self):
        """测试: 不带时间段的 Prompt"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        prompt = miner._build_mining_prompt(
            title="测试",
            company="测试公司",
            description="测试工作",
            period="",
            context=None
        )

        assert "测试" in prompt


class TestParseDimensions:
    """维度数据解析测试"""

    def test_parse_full_dimensions(self):
        """测试: 解析完整维度数据"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        data = {
            "tech": {
                "stack": ["Python", "Go"],
                "architecture": "微服务",
                "challenges": ["并发"]
            },
            "business": {
                "context": "电商",
                "metrics": {"before": "10", "after": "100", "unit": "%"},
                "impact": "提升"
            },
            "collaboration": {
                "team_size": 10,
                "cross_functional": True,
                "stakeholders": ["产品"]
            },
            "innovation": {
                "innovations": ["新方案"],
                "lessons": ["经验"]
            },
            "growth": {
                "skills": ["管理"],
                "leadership": "领导力"
            }
        }

        result = miner._parse_dimensions(data)

        assert result.tech_stack == ["Python", "Go"]
        assert result.architecture_contribution == "微服务"
        assert result.business_context == "电商"
        assert result.team_size == 10
        assert result.cross_functional is True

    def test_parse_missing_sections(self):
        """测试: 解析缺失部分的数据"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        data = {
            "tech": {"stack": ["Java"]}
        }

        result = miner._parse_dimensions(data)

        assert result.tech_stack == ["Java"]
        assert result.architecture_contribution == ""
        assert result.business_context == ""
        assert result.team_size == 0

    def test_parse_empty_data(self):
        """测试: 解析空数据"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        result = miner._parse_dimensions({})

        assert result.tech_stack == []
        assert result.team_size == 0
        assert result.cross_functional is False

    def test_parse_nested_missing_fields(self):
        """测试: 解析嵌套缺失字段"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        data = {
            "tech": {},
            "business": {},
            "collaboration": {},
            "innovation": {},
            "growth": {}
        }

        result = miner._parse_dimensions(data)

        assert result.tech_stack == []
        assert result.metrics == {}
        assert result.stakeholder_management == []


class TestDefaultDimensions:
    """默认维度数据测试"""

    def test_default_dimensions_values(self):
        """测试: 默认维度数据值"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        result = miner._default_dimensions()

        assert result.tech_stack == []
        assert result.architecture_contribution == ""
        assert result.technical_challenges == []
        assert result.business_context == ""
        assert result.metrics == {}
        assert result.business_impact == ""
        assert result.team_size == 0
        assert result.cross_functional is False
        assert result.stakeholder_management == []
        assert result.innovations == []
        assert result.lessons_learned == []
        assert result.skills_gained == []
        assert result.leadership_growth == ""


class TestGenerateStarDescription:
    """STAR 法则描述生成测试"""

    def test_generate_star_balanced(self):
        """测试: 生成平衡型 STAR 描述"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=["React", "Redux"],
            architecture_contribution="用户中心模块",
            technical_challenges=[],
            business_context="电商平台",
            metrics={"before": "100", "after": "500", "unit": "ms"},
            business_impact="性能提升",
            team_size=5,
            cross_functional=True,
            stakeholder_management=["产品经理"],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        result = miner.generate_star_description(dims, highlight="balanced")

        assert "电商平台" in result
        assert "用户中心模块" in result
        assert "React" in result
        assert "5" in result
        assert "100" in result or "500" in result

    def test_generate_star_tech_highlight(self):
        """测试: 技术突出型 STAR 描述"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=["Python", "Go", "Kubernetes", "Istio"],
            architecture_contribution="服务网格平台",
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

        result = miner.generate_star_description(dims, highlight="tech")

        assert "服务网格平台" in result
        assert "Python" in result

    def test_generate_star_business_highlight(self):
        """测试: 业务突出型 STAR 描述"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
            architecture_contribution="核心交易系统",
            technical_challenges=[],
            business_context="金融交易",
            metrics={"before": "1000", "after": "5000", "unit": "TPS"},
            business_impact="收入翻倍",
            team_size=0,
            cross_functional=False,
            stakeholder_management=[],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        result = miner.generate_star_description(dims, highlight="business")

        assert "金融交易" in result
        assert "核心交易系统" in result
        assert "1000" in result or "5000" in result

    def test_generate_star_leadership_highlight(self):
        """测试: 领导力突出型 STAR 描述"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
            architecture_contribution="团队管理",
            technical_challenges=[],
            business_context="技术部门",
            metrics={},
            business_impact="团队效率提升",
            team_size=15,
            cross_functional=True,
            stakeholder_management=["HR", "业务"],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth="管理10人团队"
        )

        result = miner.generate_star_description(dims, highlight="leadership")

        assert "15" in result
        assert "技术部门" in result

    def test_generate_star_minimal_data(self):
        """测试: 最小数据生成 STAR"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
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

        result = miner.generate_star_description(dims)

        # 应该包含默认的"核心功能开发"
        assert "核心功能开发" in result

    def test_generate_star_with_metrics_only_after(self):
        """测试: 只有 after 指标的 STAR"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
            architecture_contribution="项目开发",
            technical_challenges=[],
            business_context="",
            metrics={"after": "100万", "unit": "用户"},
            business_impact="",
            team_size=0,
            cross_functional=False,
            stakeholder_management=[],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        result = miner.generate_star_description(dims)

        assert "100万" in result
        assert "用户" in result


class TestSuggestQuantification:
    """量化建议生成测试"""

    def test_suggest_no_metrics(self):
        """测试: 无指标时建议"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
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

        suggestions = miner.suggest_quantification(dims)

        assert any("性能" in s or "用户" in s or "收入" in s for s in suggestions)

    def test_suggest_no_team_size(self):
        """测试: 无团队规模时建议"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=["React"],
            architecture_contribution="前端开发",
            technical_challenges=["性能优化"],
            business_context="",
            metrics={"before": "100", "after": "200", "unit": "%"},
            business_impact="提升",
            team_size=0,
            cross_functional=False,
            stakeholder_management=[],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        suggestions = miner.suggest_quantification(dims)

        assert any("团队" in s or "规模" in s or "层级" in s for s in suggestions)

    def test_suggest_no_challenges(self):
        """测试: 无技术难题时建议"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
            architecture_contribution="",
            technical_challenges=[],
            business_context="",
            metrics={},
            business_impact="",
            team_size=5,
            cross_functional=False,
            stakeholder_management=[],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        suggestions = miner.suggest_quantification(dims)

        assert any("技术" in s and ("难点" in s or "架构" in s) for s in suggestions)

    def test_suggest_complete_data(self):
        """测试: 完整数据无建议"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=["Python"],
            architecture_contribution="后端开发",
            technical_challenges=["并发处理"],
            business_context="",
            metrics={"before": "100", "after": "200", "unit": "%"},
            business_impact="",
            team_size=10,
            cross_functional=False,
            stakeholder_management=[],
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        suggestions = miner.suggest_quantification(dims)

        # 应该没有建议或建议很少
        assert len(suggestions) == 0


class TestMineWorkExperience:
    """快速挖掘工作经历便捷函数测试"""

    async def test_mine_work_experience_full_result(self):
        """测试: 完整的快速挖掘结果"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "tech": {"stack": ["Java"], "architecture": "", "challenges": []},
                "business": {"context": "", "metrics": {}, "impact": ""},
                "collaboration": {"team_size": 0, "cross_functional": false, "stakeholders": []},
                "innovation": {"innovations": [], "lessons": []},
                "growth": {"skills": [], "leadership": ""}
            }'''
        )

        result = await mine_work_experience(
            ai_provider=mock_ai,
            title="Java工程师",
            company="某公司",
            description="Java开发"
        )

        assert "dimensions" in result
        assert "star_description" in result
        assert "suggestions" in result

    async def test_mine_work_experience_with_period(self):
        """测试: 带时间段的快速挖掘"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "tech": {"stack": ["Python"], "architecture": "", "challenges": []},
                "business": {"context": "", "metrics": {}, "impact": ""},
                "collaboration": {"team_size": 0, "cross_functional": false, "stakeholders": []},
                "innovation": {"innovations": [], "lessons": []},
                "growth": {"skills": [], "leadership": ""}
            }'''
        )

        result = await mine_work_experience(
            ai_provider=mock_ai,
            title="Python工程师",
            company="某公司",
            description="Python开发",
            period="2020-2023"
        )

        assert result["dimensions"]["tech_stack"] == ["Python"]

    async def test_mine_work_experience_with_context(self):
        """测试: 带上下文的快速挖掘"""
        mock_ai = AsyncMock()
        mock_ai.optimize_content = AsyncMock(
            return_value='''{
                "tech": {"stack": ["Go"], "architecture": "", "challenges": []},
                "business": {"context": "", "metrics": {}, "impact": ""},
                "collaboration": {"team_size": 0, "cross_functional": false, "stakeholders": []},
                "innovation": {"innovations": [], "lessons": []},
                "growth": {"skills": [], "leadership": ""}
            }'''
        )

        result = await mine_work_experience(
            ai_provider=mock_ai,
            title="Go工程师",
            company="某公司",
            description="Go开发",
            context={"industry": "区块链"}
        )

        assert result["dimensions"]["tech_stack"] == ["Go"]


class TestStarDescriptionEdgeCases:
    """STAR 描述生成边界情况测试"""

    def test_star_description_truncates_long_tech_stack(self):
        """测试: 长技术栈截断"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=["React", "Vue", "Angular", "Svelte", "Solid", "Next.js", "Nuxt"],
            architecture_contribution="前端开发",
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

        result = miner.generate_star_description(dims)

        # 应该只显示前3个技术栈
        assert "React" in result
        # 检查是否包含过多技术（应该被截断）
        tech_count = sum(1 for tech in dims.tech_stack[:3] if tech in result)
        assert tech_count <= 3

    def test_star_description_no_stakeholders(self):
        """测试: 无利益相关方时处理"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
            architecture_contribution="开发",
            technical_challenges=[],
            business_context="",
            metrics={},
            business_impact="",
            team_size=5,
            cross_functional=True,
            stakeholder_management=[],  # 空列表
            innovations=[],
            lessons_learned=[],
            skills_gained=[],
            leadership_growth=""
        )

        result = miner.generate_star_description(dims)

        assert "5" in result  # 团队规模
        assert "协作" in result or "多方" in result

    def test_star_description_filters_empty_parts(self):
        """测试: 过滤空的部分"""
        mock_ai = MagicMock()
        miner = ExperienceMiner(mock_ai)

        dims = ExperienceDimensions(
            tech_stack=[],
            architecture_contribution="",
            technical_challenges=[],
            business_context="",  # 空
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

        result = miner.generate_star_description(dims)

        # 不应该出现连续的句号
        assert "。。" not in result
        # 应该有默认内容
        assert "核心功能开发" in result
