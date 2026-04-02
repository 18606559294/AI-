"""
ATS 关键词优化器测试
"""
import pytest
from app.services.ai.enhancers.ats_optimizer import (
    ATSOptimizer,
    quick_ats_check
)


class TestATSOptimizerInit:
    """ATS 优化器初始化测试"""

    def test_init_creates_empty_state(self):
        """测试: 初始化创建空状态"""
        optimizer = ATSOptimizer()

        assert optimizer.jd_keywords == set()
        assert optimizer.jd_requirements == []


class TestExtractJDKeywords:
    """JD 关键词提取测试"""

    def test_extract_frontend_keywords(self):
        """测试: 提取前端技能关键词"""
        optimizer = ATSOptimizer()
        jd = """
        我们需要一名前端开发工程师，熟悉 React、Vue、TypeScript。
        需要掌握 HTML、CSS、JavaScript，有 Webpack 使用经验。
        """

        result = optimizer.extract_jd_keywords(jd)

        assert "react" in result["hard_skills"]
        assert "vue" in result["hard_skills"]
        assert "typescript" in result["hard_skills"]
        assert "html" in result["hard_skills"]
        assert "css" in result["hard_skills"]
        assert "javascript" in result["hard_skills"]
        assert "webpack" in result["hard_skills"]

    def test_extract_backend_keywords(self):
        """测试: 提取后端技能关键词"""
        optimizer = ATSOptimizer()
        jd = """
        后端工程师，熟悉 Python、Django、FastAPI。
        需要 MySQL、Redis、Docker 经验。
        """

        result = optimizer.extract_jd_keywords(jd)

        assert "python" in result["hard_skills"]
        assert "django" in result["hard_skills"]
        assert "fastapi" in result["hard_skills"]
        assert "mysql" in result["hard_skills"]
        assert "redis" in result["hard_skills"]
        assert "docker" in result["hard_skills"]

    def test_extract_devops_keywords(self):
        """测试: 提取 DevOps 技能关键词"""
        optimizer = ATSOptimizer()
        jd = """
        DevOps 工程师，熟悉 Linux、Shell、Git。
        需要 Kubernetes、Helm、Terraform 经验。
        了解 AWS、Prometheus、Grafana。
        """

        result = optimizer.extract_jd_keywords(jd)

        assert "linux" in result["hard_skills"]
        assert "shell" in result["hard_skills"]
        assert "git" in result["hard_skills"]
        assert "kubernetes" in result["hard_skills"]
        assert "helm" in result["hard_skills"]
        assert "terraform" in result["hard_skills"]
        assert "aws" in result["hard_skills"]

    def test_extract_mobile_keywords(self):
        """测试: 提取移动端技能关键词"""
        optimizer = ATSOptimizer()
        jd = """
        移动端开发，熟悉 iOS、Android、Swift、Kotlin。
        有 Flutter、React Native 经验。
        """

        result = optimizer.extract_jd_keywords(jd)

        assert "ios" in result["hard_skills"]
        assert "android" in result["hard_skills"]
        assert "swift" in result["hard_skills"]
        assert "kotlin" in result["hard_skills"]
        assert "flutter" in result["hard_skills"]
        assert "react native" in result["hard_skills"]

    def test_extract_soft_skills(self):
        """测试: 提取软技能"""
        optimizer = ATSOptimizer()
        jd = """
        需要良好的沟通能力和团队协作精神。
        具备领导力和问题解决能力。
        """

        result = optimizer.extract_jd_keywords(jd)

        assert "沟通" in result["soft_skills"] or "communication" in result["soft_skills"]
        assert "协作" in result["soft_skills"] or "collaboration" in result["soft_skills"]

    def test_extract_years_requirement(self):
        """测试: 提取工作年限要求"""
        optimizer = ATSOptimizer()
        jd = "需要3年以上工作经验，5年及以上优先。"

        result = optimizer.extract_jd_keywords(jd)

        assert any("3" in req for req in result["requirements"])

    def test_extract_education_requirement(self):
        """测试: 提取学历要求"""
        optimizer = ATSOptimizer()
        jd = "本科及以上学历，硕士优先。"

        result = optimizer.extract_jd_keywords(jd)

        assert any("本科" in req for req in result["requirements"])

    def test_case_insensitive_matching(self):
        """测试: 大小写不敏感匹配"""
        optimizer = ATSOptimizer()
        jd = "需要掌握 REACT、Vue、AnGuLaR 框架。"

        result = optimizer.extract_jd_keywords(jd)

        assert "react" in result["hard_skills"]
        assert "vue" in result["hard_skills"]
        assert "angular" in result["hard_skills"]

    def test_updates_internal_state(self):
        """测试: 更新内部状态"""
        optimizer = ATSOptimizer()
        jd = "需要 React 和 Vue 技能。"

        result = optimizer.extract_jd_keywords(jd)

        assert "react" in optimizer.jd_keywords
        assert "vue" in optimizer.jd_keywords

    def test_empty_jd(self):
        """测试: 空 JD 处理"""
        optimizer = ATSOptimizer()
        result = optimizer.extract_jd_keywords("")

        assert result["hard_skills"] == []
        assert result["soft_skills"] == []
        assert result["requirements"] == []

    def test_extract_data_keywords(self):
        """测试: 提取数据相关技能"""
        optimizer = ATSOptimizer()
        jd = """
        数据工程师，熟悉 SQL、Pandas、NumPy。
        有 Spark、Hadoop、Kafka 经验。
        """

        result = optimizer.extract_jd_keywords(jd)

        assert "sql" in result["hard_skills"]
        assert "pandas" in result["hard_skills"]
        assert "numpy" in result["hard_skills"]
        assert "spark" in result["hard_skills"]
        assert "hadoop" in result["hard_skills"]
        assert "kafka" in result["hard_skills"]


class TestAnalyzeMatchScore:
    """匹配度分析测试"""

    def test_full_match(self):
        """测试: 完全匹配"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": ["react", "vue", "typescript"],
            "soft_skills": ["沟通"]
        }
        resume = {
            "skills": ["React", "Vue", "TypeScript"],
            "work_experience": [
                {"description": "使用 React 和 Vue 开发项目，有良好的沟通能力"}
            ]
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        assert result["overall_score"] >= 90
        assert len(result["hard_skill_match"]["matched"]) == 3
        assert len(result["hard_skill_match"]["missing"]) == 0

    def test_no_match(self):
        """测试: 完全不匹配"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": ["java", "spring"],
            "soft_skills": []
        }
        resume = {
            "skills": ["Python", "Django"],
            "work_experience": [{"description": "Python 开发"}]
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        assert result["overall_score"] < 50
        assert len(result["hard_skill_match"]["matched"]) == 0
        assert len(result["hard_skill_match"]["missing"]) == 2

    def test_partial_match(self):
        """测试: 部分匹配"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": ["react", "vue", "angular", "typescript"],
            "soft_skills": ["沟通", "协作"]
        }
        resume = {
            "skills": ["React", "TypeScript"],
            "work_experience": [{"description": "前端开发，沟通能力强"}]
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        assert result["overall_score"] >= 50
        assert result["overall_score"] < 100
        assert len(result["hard_skill_match"]["matched"]) == 2
        assert len(result["hard_skill_match"]["missing"]) == 2

    def test_soft_skill_matching(self):
        """测试: 软技能匹配"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": [],
            "soft_skills": ["沟通", "协作", "领导力"]
        }
        resume = {
            "skills": [],
            "work_experience": [{"description": "具有团队沟通和协作经验"}]
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        assert "沟通" in result["soft_skill_match"]["matched"]
        assert "协作" in result["soft_skill_match"]["matched"]
        assert "领导力" in result["soft_skill_match"]["missing"]

    def test_case_insensitive_resume(self):
        """测试: 简历大小写不敏感"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": ["react"],
            "soft_skills": []
        }
        resume = {
            "skills": ["REACT", "React", "react"],
            "work_experience": []
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        assert len(result["hard_skill_match"]["matched"]) == 1

    def test_empty_resume(self):
        """测试: 空简历处理"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": ["react", "vue"],
            "soft_skills": []
        }
        resume = {"skills": [], "work_experience": []}

        result = optimizer.analyze_match_score(resume, jd_keywords)

        # 空简历时硬技能匹配率为0，软技能默认为1.0，分数=0*70+1.0*30=30
        assert result["overall_score"] == 30
        assert len(result["hard_skill_match"]["matched"]) == 0

    def test_empty_jd_keywords(self):
        """测试: 空 JD 关键词"""
        optimizer = ATSOptimizer()
        jd_keywords = {"hard_skills": [], "soft_skills": []}
        resume = {
            "skills": ["React"],
            "work_experience": [{"description": "前端开发"}]
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        assert result["overall_score"] == 100  # 空要求视为完全匹配

    def test_match_rate_calculation(self):
        """测试: 匹配率计算"""
        optimizer = ATSOptimizer()
        jd_keywords = {
            "hard_skills": ["react", "vue", "angular", "typescript", "javascript"],
            "soft_skills": []
        }
        resume = {
            "skills": ["React", "TypeScript", "JavaScript"],
            "work_experience": []
        }

        result = optimizer.analyze_match_score(resume, jd_keywords)

        # 3/5 硬技能匹配
        assert result["hard_skill_match"]["rate"] == 60.0


class TestExtractResumeText:
    """简历文本提取测试"""

    def test_extract_from_skills(self):
        """测试: 从技能字段提取"""
        optimizer = ATSOptimizer()
        resume = {
            "skills": ["React", "Vue", "TypeScript"],
            "work_experience": [],
            "projects": []
        }

        text = optimizer._extract_resume_text(resume)

        assert "React" in text
        assert "Vue" in text

    def test_extract_from_work_experience(self):
        """测试: 从工作经历提取"""
        optimizer = ATSOptimizer()
        resume = {
            "skills": [],
            "work_experience": [
                {"description": "使用 React 开发前端项目"},
                {"description": "负责 Vue 组件库开发"}
            ],
            "projects": []
        }

        text = optimizer._extract_resume_text(resume)

        assert "React" in text
        assert "Vue" in text

    def test_extract_from_projects(self):
        """测试: 从项目经历提取"""
        optimizer = ATSOptimizer()
        resume = {
            "skills": [],
            "work_experience": [],
            "projects": [
                {"description": "使用 Python 开发数据分析系统"},
                {"description": "机器学习模型训练平台"}
            ]
        }

        text = optimizer._extract_resume_text(resume)

        assert "Python" in text
        assert "机器学习" in text

    def test_extract_from_all_sections(self):
        """测试: 从所有模块提取"""
        optimizer = ATSOptimizer()
        resume = {
            "skills": ["React"],
            "work_experience": [{"description": "Vue 项目"}],
            "projects": [{"description": "Angular 应用"}]
        }

        text = optimizer._extract_resume_text(resume)

        assert "React" in text
        assert "Vue" in text
        assert "Angular" in text

    def test_handle_missing_sections(self):
        """测试: 处理缺失的模块"""
        optimizer = ATSOptimizer()
        resume = {}

        text = optimizer._extract_resume_text(resume)

        assert text == ""


class TestGenerateSuggestions:
    """优化建议生成测试"""

    def test_low_score_suggestions(self):
        """测试: 低分建议"""
        optimizer = ATSOptimizer()
        suggestions = optimizer._generate_suggestions(
            missing_hard=["react", "vue"],
            missing_soft=["沟通"],
            score=50
        )

        assert any("较低" in s or "50" in s for s in suggestions)

    def test_medium_score_suggestions(self):
        """测试: 中等分数建议"""
        optimizer = ATSOptimizer()
        suggestions = optimizer._generate_suggestions(
            missing_hard=["vue"],
            missing_soft=[],
            score=75
        )

        assert any("一般" in s or "75" in s for s in suggestions)

    def test_high_score_suggestions(self):
        """测试: 高分建议"""
        optimizer = ATSOptimizer()
        suggestions = optimizer._generate_suggestions(
            missing_hard=[],
            missing_soft=[],
            score=90
        )

        assert any("良好" in s or "90" in s for s in suggestions)

    def test_missing_hard_skills_count(self):
        """测试: 缺失硬技能计数"""
        optimizer = ATSOptimizer()
        suggestions = optimizer._generate_suggestions(
            missing_hard=["react", "vue", "angular"],
            missing_soft=[],
            score=60
        )

        assert any("3项" in s or "3" in s for s in suggestions)

    def test_missing_soft_skills_list(self):
        """测试: 缺失软技能列表"""
        optimizer = ATSOptimizer()
        suggestions = optimizer._generate_suggestions(
            missing_hard=[],
            missing_soft=["沟通", "协作"],
            score=70
        )

        assert any("沟通" in s and "协作" in s for s in suggestions)


class TestSuggestInjections:
    """关键词注入建议测试"""

    def test_frontend_skill_injection(self):
        """测试: 前端技能注入建议"""
        optimizer = ATSOptimizer()
        resume = {"skills": [], "work_experience": [], "projects": []}
        jd_keywords = {"hard_skills": ["react", "vue", "css", "html"]}

        suggestions = optimizer.suggest_injections(resume, jd_keywords)

        assert len(suggestions) == 4
        assert all(s["section"] == "skills" for s in suggestions)

    def test_backend_skill_injection(self):
        """测试: 后端技能注入建议"""
        optimizer = ATSOptimizer()
        resume = {"skills": [], "work_experience": [], "projects": []}
        jd_keywords = {"hard_skills": ["mysql", "redis", "docker"]}

        suggestions = optimizer.suggest_injections(resume, jd_keywords)

        assert all(s["section"] == "skills" for s in suggestions)

    def test_other_skill_injection(self):
        """测试: 其他技能注入到工作经历"""
        optimizer = ATSOptimizer()
        resume = {"skills": [], "work_experience": [], "projects": []}
        jd_keywords = {"hard_skills": ["python", "fastapi"]}

        suggestions = optimizer.suggest_injections(resume, jd_keywords)

        assert all(s["section"] == "work_experience" for s in suggestions)

    def test_no_suggestion_for_matched_skills(self):
        """测试: 已匹配的技能不生成建议"""
        optimizer = ATSOptimizer()
        resume = {"skills": ["React"], "work_experience": [], "projects": []}
        jd_keywords = {"hard_skills": ["react"]}

        suggestions = optimizer.suggest_injections(resume, jd_keywords)

        assert len(suggestions) == 0


class TestOptimizeForATS:
    """一站式 ATS 优化测试"""

    def test_full_optimization_flow(self):
        """测试: 完整优化流程"""
        optimizer = ATSOptimizer()
        resume = {
            "skills": ["React"],
            "work_experience": [{"description": "前端开发"}],
            "projects": []
        }
        jd = "需要 React、Vue、TypeScript 技能。"

        result = optimizer.optimize_for_ats(resume, jd)

        assert "jd_analysis" in result
        assert "match_score" in result
        assert "optimization_suggestions" in result
        assert "priority_actions" in result

    def test_priority_actions_low_score(self):
        """测试: 低分数优先级行动"""
        optimizer = ATSOptimizer()
        resume = {"skills": [], "work_experience": [], "projects": []}
        jd = "需要 Java、Spring、MySQL、Redis、Python、Docker。"

        result = optimizer.optimize_for_ats(resume, jd)

        actions = result["priority_actions"]
        assert any("高优先级" in action for action in actions)

    def test_priority_actions_medium_score(self):
        """测试: 中等分数优先级行动"""
        optimizer = ATSOptimizer()
        resume = {"skills": ["Java", "Spring"], "work_experience": [], "projects": []}
        jd = "需要 Java、Spring、MySQL、Redis、Docker。"

        result = optimizer.optimize_for_ats(resume, jd)

        actions = result["priority_actions"]
        assert any("中优先级" in action for action in actions)

    def test_priority_actions_high_score(self):
        """测试: 高分数优先级行动"""
        optimizer = ATSOptimizer()
        resume = {
            "skills": ["Java", "Spring", "MySQL"],
            "work_experience": [],
            "projects": []
        }
        # JD 包含一个简历中不存在的技能，这样会有 injection_suggestions
        jd = "需要 Java、Spring、MySQL、Redis、Docker 技能。"

        result = optimizer.optimize_for_ats(resume, jd)

        actions = result["priority_actions"]
        # 高分（>=70）时只有低优先级行动
        assert any("低优先级" in action for action in actions)


class TestQuickATSCheck:
    """快速 ATS 检查测试"""

    def test_quick_check_full_match(self):
        """测试: 快速检查完全匹配"""
        resume = "熟练使用 React、Vue、TypeScript 进行前端开发"
        jd = "需要 React、Vue、TypeScript 技能"

        result = quick_ats_check(resume, jd)

        assert result["score"] == 100
        assert result["matched_skills"] == 3
        assert result["total_skills"] == 3

    def test_quick_check_partial_match(self):
        """测试: 快速检查部分匹配"""
        resume = "熟练使用 React 进行前端开发"
        jd = "需要 React、Vue、TypeScript 技能"

        result = quick_ats_check(resume, jd)

        assert result["score"] > 0
        assert result["score"] < 100
        assert result["matched_skills"] == 1

    def test_quick_check_no_match(self):
        """测试: 快速检查不匹配"""
        resume = "熟练使用 Python、Django 进行后端开发"
        jd = "需要 React、Vue、TypeScript 技能"

        result = quick_ats_check(resume, jd)

        assert result["score"] == 0
        assert result["matched_skills"] == 0

    def test_quick_check_top_missing(self):
        """测试: 快速检查返回缺失技能"""
        resume = "React 开发"
        jd = "需要 React、Vue、TypeScript、JavaScript、HTML、CSS 技能"

        result = quick_ats_check(resume, jd)

        assert len(result["top_missing"]) > 0
        assert "vue" in result["top_missing"]

    def test_quick_check_empty_jd(self):
        """测试: 快速检查空 JD"""
        resume = "React 开发"
        jd = "无需专业技能"

        result = quick_ats_check(resume, jd)

        # 分数应为 0 因为 total_skills = 0
        assert result["score"] == 0


class TestSKILL_KEYWORDS:
    """技能关键词库测试"""

    def test_frontend_keywords_complete(self):
        """测试: 前端关键词库完整"""
        frontend = ATSOptimizer.SKILL_KEYWORDS["frontend"]

        assert "react" in frontend
        assert "vue" in frontend
        assert "angular" in frontend
        assert "typescript" in frontend
        assert "javascript" in frontend

    def test_backend_keywords_complete(self):
        """测试: 后端关键词库完整"""
        backend = ATSOptimizer.SKILL_KEYWORDS["backend"]

        assert "java" in backend
        assert "python" in backend
        assert "go" in backend
        assert "mysql" in backend
        assert "redis" in backend

    def test_data_keywords_complete(self):
        """测试: 数据关键词库完整"""
        data = ATSOptimizer.SKILL_KEYWORDS["data"]

        assert "pandas" in data
        assert "numpy" in data
        assert "spark" in data
        assert "tensorflow" in data

    def test_devops_keywords_complete(self):
        """测试: DevOps 关键词库完整"""
        devops = ATSOptimizer.SKILL_KEYWORDS["devops"]

        assert "linux" in devops
        assert "docker" in devops
        assert "kubernetes" in devops
        assert "aws" in devops

    def test_mobile_keywords_complete(self):
        """测试: 移动端关键词库完整"""
        mobile = ATSOptimizer.SKILL_KEYWORDS["mobile"]

        assert "ios" in mobile
        assert "android" in mobile
        assert "swift" in mobile
        assert "kotlin" in mobile
        assert "flutter" in mobile


class TestRequirementPatterns:
    """要求正则模式测试"""

    def test_years_pattern(self):
        """测试: 工作年限模式"""
        import re
        pattern = ATSOptimizer.REQUIREMENT_PATTERNS[0]

        matches = re.findall(pattern, "需要3年以上工作经验")
        assert "3" in matches

        matches = re.findall(pattern, "5年及以上经验")
        assert "5" in matches

    def test_education_pattern(self):
        """测试: 学历模式"""
        import re
        pattern = ATSOptimizer.REQUIREMENT_PATTERNS[1]

        matches = re.findall(pattern, "本科及以上")
        assert "本科" in matches

        matches = re.findall(pattern, "硕士及以上优先")
        assert "硕士" in matches

        # 模式是 (本科|硕士|博士|专科)(?:及)?以上，所以"硕士"不会单独匹配
        matches = re.findall(pattern, "硕士优先")
        assert "硕士" not in matches  # 没有"以上"，不会匹配

    def test_familiarity_pattern(self):
        """测试: 熟悉/精通模式"""
        import re
        pattern = ATSOptimizer.REQUIREMENT_PATTERNS[2]

        matches = re.findall(pattern, "熟悉React框架开发")
        assert len(matches) > 0

        matches = re.findall(pattern, "精通Python")
        assert len(matches) > 0
