"""
ATS 关键词优化器
自动提取 JD 关键词，优化简历匹配度
"""
import json
import re
from typing import Dict, Any, List, Set, Tuple
from collections import Counter


class ATSOptimizer:
    """
    ATS (Applicant Tracking System) 优化器
    
    功能：
    1. 从 JD 提取关键词
    2. 分析简历与 JD 的匹配度
    3. 建议缺失的关键词
    4. 自动优化简历内容
    """
    
    # 通用技能关键词库（按领域分类）
    SKILL_KEYWORDS = {
        "frontend": [
            "react", "vue", "angular", "typescript", "javascript", "html", "css",
            "webpack", "vite", "tailwind", "bootstrap", "sass", "less",
            "redux", "mobx", "pinia", "next.js", "nuxt", "spa", "ssr",
            "dom", "bom", "ajax", "fetch", "axios", "rest", "graphql"
        ],
        "backend": [
            "java", "python", "go", "nodejs", "c++", "c#", "rust", "php",
            "spring", "springboot", "django", "flask", "fastapi", "express",
            "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
            "kafka", "rabbitmq", "docker", "kubernetes", "microservices"
        ],
        "data": [
            "sql", "pandas", "numpy", "spark", "hadoop", "hive", "flink",
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "data analysis", "data mining", "etl", "data warehouse"
        ],
        "devops": [
            "linux", "shell", "bash", "git", "jenkins", "gitlab ci", "github actions",
            "docker", "kubernetes", "k8s", "helm", "terraform", "ansible",
            "aws", "azure", "gcp", "aliyun", "tencent cloud",
            "prometheus", "grafana", "elk", "observability"
        ],
        "mobile": [
            "ios", "android", "swift", "kotlin", "objective-c",
            "flutter", "react native", "uniapp", "cordova", "ionic",
            "mvvm", "mvc", "mvp", "jetpack", "arkts", "harmonyos"
        ]
    }
    
    # 软技能关键词
    SOFT_SKILLS = [
        "沟通", "协作", "团队合作", "领导力", "问题解决", "分析能力",
        "communication", "collaboration", "teamwork", "leadership",
        "problem solving", "analytical", "adaptability", "creativity"
    ]
    
    # 学历/经验要求关键词
    REQUIREMENT_PATTERNS = [
        r'(\d+)\+?\s*年(?:及)?以上?(?:工作)?经验',
        r'(本科|硕士|博士|专科)(?:及)?以上',
        r'(?:熟悉|精通|掌握|了解)\s*([^，。；]+)',
        r'有\s*(.+?)\s*经验',
    ]
    
    def __init__(self):
        self.jd_keywords: Set[str] = set()
        self.jd_requirements: List[str] = []
    
    def extract_jd_keywords(self, job_description: str) -> Dict[str, Any]:
        """
        从职位描述中提取关键词
        
        Args:
            job_description: 职位描述文本
        
        Returns:
            包含以下字段的字典：
            - hard_skills: 硬技能关键词
            - soft_skills: 软技能关键词
            - requirements: 硬性要求
            - nice_to_have: 加分项
        """
        text = job_description.lower()
        
        result = {
            "hard_skills": [],
            "soft_skills": [],
            "requirements": [],
            "nice_to_have": [],
            "raw_keywords": []
        }
        
        # 提取技能关键词
        all_skills = []
        for category, keywords in self.SKILL_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    all_skills.append(keyword)
        
        result["hard_skills"] = list(set(all_skills))
        
        # 提取软技能
        for skill in self.SOFT_SKILLS:
            if skill.lower() in text:
                result["soft_skills"].append(skill)
        
        # 使用正则提取要求
        for pattern in self.REQUIREMENT_PATTERNS:
            matches = re.findall(pattern, job_description)
            result["requirements"].extend(matches)
        
        # 简单关键词提取（分词后长度>2的英文单词或中文词组）
        words = re.findall(r'[a-zA-Z]+', text)
        word_freq = Counter(words)
        
        # 选取高频技术词汇
        common_tech = [
            word for word, count in word_freq.most_common(20)
            if len(word) > 2 and word not in ['and', 'the', 'for', 'with', 'you', 'will']
        ]
        result["raw_keywords"] = common_tech
        
        self.jd_keywords = set(result["hard_skills"] + result["soft_skills"])
        self.jd_requirements = result["requirements"]
        
        return result
    
    def analyze_match_score(
        self,
        resume_content: Dict[str, Any],
        jd_keywords: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        分析简历与 JD 的匹配度
        
        Args:
            resume_content: 简历内容
            jd_keywords: JD 关键词提取结果
        
        Returns:
            匹配度分析结果
        """
        # 提取简历中的关键词
        resume_text = self._extract_resume_text(resume_content)
        resume_text_lower = resume_text.lower()
        
        hard_skills = jd_keywords.get("hard_skills", [])
        soft_skills = jd_keywords.get("soft_skills", [])
        
        # 计算匹配度
        matched_hard = [
            skill for skill in hard_skills
            if skill.lower() in resume_text_lower
        ]
        matched_soft = [
            skill for skill in soft_skills
            if skill.lower() in resume_text_lower
        ]
        
        hard_match_rate = len(matched_hard) / len(hard_skills) if hard_skills else 1.0
        soft_match_rate = len(matched_soft) / len(soft_skills) if soft_skills else 1.0
        
        # 整体匹配分数（硬技能权重更高）
        overall_score = int(hard_match_rate * 70 + soft_match_rate * 30)
        
        # 缺失关键词
        missing_hard = list(set(hard_skills) - set(matched_hard))
        missing_soft = list(set(soft_skills) - set(matched_soft))
        
        return {
            "overall_score": overall_score,
            "hard_skill_match": {
                "matched": matched_hard,
                "missing": missing_hard,
                "rate": round(hard_match_rate * 100, 1)
            },
            "soft_skill_match": {
                "matched": matched_soft,
                "missing": missing_soft,
                "rate": round(soft_match_rate * 100, 1)
            },
            "suggestions": self._generate_suggestions(
                missing_hard, missing_soft, overall_score
            )
        }
    
    def _extract_resume_text(self, resume_content: Dict[str, Any]) -> str:
        """从简历内容中提取文本"""
        text_parts = []
        
        # 技能
        skills = resume_content.get("skills", [])
        if isinstance(skills, list):
            text_parts.extend(skills)
        
        # 工作经历
        for exp in resume_content.get("work_experience", []):
            desc = exp.get("description", "")
            if desc:
                text_parts.append(desc)
        
        # 项目经历
        for proj in resume_content.get("projects", []):
            desc = proj.get("description", "")
            if desc:
                text_parts.append(desc)
        
        return " ".join(text_parts)
    
    def _generate_suggestions(
        self,
        missing_hard: List[str],
        missing_soft: List[str],
        score: int
    ) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        if score < 60:
            suggestions.append(f"⚠️ 匹配度较低（{score}分），建议重点补充以下技能：" + ", ".join(missing_hard[:5]))
        elif score < 80:
            suggestions.append(f"📌 匹配度一般（{score}分），可考虑添加：" + ", ".join(missing_hard[:3]))
        else:
            suggestions.append(f"✅ 匹配度良好（{score}分），技能覆盖较全面")
        
        if missing_hard:
            suggestions.append(f"缺失硬技能（{len(missing_hard)}项）：" + ", ".join(missing_hard[:10]))
        
        if missing_soft:
            suggestions.append(f"缺失软技能：" + ", ".join(missing_soft[:5]))
        
        return suggestions
    
    def suggest_injections(
        self,
        resume_content: Dict[str, Any],
        jd_keywords: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        建议关键词注入位置
        
        Returns:
            建议列表，每项包含：
            - section: 模块名称
            - keyword: 关键词
            - suggestion: 注入建议
        """
        suggestions = []
        
        hard_skills = jd_keywords.get("hard_skills", [])
        resume_text = self._extract_resume_text(resume_content).lower()
        
        for keyword in hard_skills:
            if keyword.lower() not in resume_text:
                # 判断应该注入到哪个模块
                if any(kw in keyword.lower() for kw in ["react", "vue", "angular", "css", "html"]):
                    section = "skills"
                    suggestion = f"在技能列表中添加：{keyword}"
                elif any(kw in keyword.lower() for kw in ["mysql", "redis", "docker", "linux"]):
                    section = "skills"
                    suggestion = f"在技能列表中添加：{keyword}"
                else:
                    section = "work_experience"
                    suggestion = f"在工作经历描述中自然融入：{keyword}"
                
                suggestions.append({
                    "section": section,
                    "keyword": keyword,
                    "suggestion": suggestion
                })
        
        return suggestions
    
    def optimize_for_ats(
        self,
        resume_content: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """
        一站式 ATS 优化
        
        Args:
            resume_content: 简历内容
            job_description: 职位描述
        
        Returns:
            完整的优化报告
        """
        # 提取 JD 关键词
        jd_keywords = self.extract_jd_keywords(job_description)
        
        # 分析匹配度
        match_analysis = self.analyze_match_score(resume_content, jd_keywords)
        
        # 生成注入建议
        injection_suggestions = self.suggest_injections(resume_content, jd_keywords)
        
        return {
            "jd_analysis": jd_keywords,
            "match_score": match_analysis,
            "optimization_suggestions": injection_suggestions,
            "priority_actions": self._get_priority_actions(match_analysis, injection_suggestions)
        }
    
    def _get_priority_actions(
        self,
        match_analysis: Dict[str, Any],
        suggestions: List[Dict[str, Any]]
    ) -> List[str]:
        """获取优先级行动项"""
        actions = []
        score = match_analysis["overall_score"]
        
        if score < 50:
            actions.append("🔴 高优先级：匹配度低于50%，建议重新定位目标岗位或大幅调整简历")
        
        if score < 70:
            actions.append("🟡 中优先级：补充核心技能关键词（前5项）")
        
        if suggestions:
            actions.append(f"🟢 低优先级：优化 {len(suggestions)} 个关键词的自然融入")
        
        return actions


# 便捷函数
def quick_ats_check(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    快速 ATS 检查
    
    Args:
        resume_text: 简历文本
        job_description: 职位描述
    
    Returns:
        简洁的检查结果
    """
    optimizer = ATSOptimizer()
    
    jd_keywords = optimizer.extract_jd_keywords(job_description)
    
    # 简单匹配计算
    resume_lower = resume_text.lower()
    matched = sum(1 for skill in jd_keywords["hard_skills"] if skill.lower() in resume_lower)
    total = len(jd_keywords["hard_skills"])
    
    return {
        "score": int(matched / total * 100) if total else 0,
        "matched_skills": matched,
        "total_skills": total,
        "top_missing": [
            skill for skill in jd_keywords["hard_skills"][:10]
            if skill.lower() not in resume_lower
        ]
    }
