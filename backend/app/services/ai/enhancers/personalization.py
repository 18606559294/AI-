"""
个性化生成策略
根据用户画像和目标岗位，定制简历内容角度
"""
import json
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass


class UserLevel(str, Enum):
    """用户级别"""
    NEW_GRAD = "new_grad"           # 应届生
    JUNIOR = "junior"               # 初级（1-3年）
    SENIOR = "senior"               # 高级（3-5年）
    STAFF = "staff"                 # 资深（5-8年）
    LEAD = "lead"                   # 负责人（8年+）
    MANAGER = "manager"             # 管理岗


class CareerType(str, Enum):
    """职业发展方向"""
    TECHNICAL = "technical"         # 技术深度
    MANAGEMENT = "management"       # 管理路线
    HYBRID = "hybrid"               # 技术+管理


@dataclass
class UserProfile:
    """用户画像"""
    level: UserLevel
    years_of_experience: int
    career_type: CareerType
    target_company_type: str        # 大厂/外企/创业公司/国企
    target_position: str
    strengths: List[str]            # 核心优势
    skill_focus: List[str]          # 想突出的技能
    avoid_keywords: List[str]       # 想避免的词汇


@dataclass
class ContentStrategy:
    """内容生成策略"""
    angle: str                      # 内容角度
    keywords_emphasis: List[str]    # 重点关键词
    structure: str                  # 结构偏好
    tone: str                       # 语气风格
    highlight_sections: List[str]   # 突出模块


class PersonalizationEngine:
    """
    个性化引擎
    
    根据用户画像和目标岗位，制定差异化生成策略
    """
    
    def __init__(self, ai_provider):
        self.ai = ai_provider
    
    def create_strategy(self, profile: UserProfile) -> ContentStrategy:
        """
        根据用户画像创建生成策略
        
        Args:
            profile: 用户画像
        
        Returns:
            ContentStrategy 生成策略
        """
        # 基于级别和职业类型的策略映射
        strategy_map = {
            (UserLevel.NEW_GRAD, CareerType.TECHNICAL): {
                "angle": "潜力导向",
                "keywords": ["学习能力", "项目经验", "技术热情", "快速上手"],
                "structure": "教育优先，项目突出",
                "tone": "积极进取",
                "sections": ["projects", "education", "skills"]
            },
            (UserLevel.JUNIOR, CareerType.TECHNICAL): {
                "angle": "成长导向",
                "keywords": ["快速学习", "独立负责", "技术深度", "业务理解"],
                "structure": "技能优先，经历详细",
                "tone": "专业可靠",
                "sections": ["work_experience", "skills", "projects"]
            },
            (UserLevel.SENIOR, CareerType.TECHNICAL): {
                "angle": "专家导向",
                "keywords": ["技术领导力", "架构设计", "问题解决", "效率提升"],
                "structure": "成果优先，技术深度",
                "tone": "权威专业",
                "sections": ["work_experience", "technical_projects", "skills"]
            },
            (UserLevel.STAFF, CareerType.TECHNICAL): {
                "angle": "影响力导向",
                "keywords": ["技术影响力", "跨团队协作", "复杂系统", "行业贡献"],
                "structure": "影响优先，架构展示",
                "tone": "谦逊有力",
                "sections": ["work_experience", "open_source", "speaking"]
            },
            (UserLevel.SENIOR, CareerType.MANAGEMENT): {
                "angle": "领导力导向",
                "keywords": ["团队管理", "项目交付", "资源协调", "人才培养"],
                "structure": "管理成果优先",
                "tone": "稳重果断",
                "sections": ["work_experience", "leadership", "achievements"]
            },
            (UserLevel.LEAD, CareerType.MANAGEMENT): {
                "angle": "战略导向",
                "keywords": ["战略规划", "组织建设", "业务增长", "文化建设"],
                "structure": "战略成果优先",
                "tone": "高屋建瓴",
                "sections": ["work_experience", "strategic_projects", "team_growth"]
            }
        }
        
        # 获取基础策略
        key = (profile.level, profile.career_type)
        base_strategy = strategy_map.get(key, {
            "angle": "专业导向",
            "keywords": ["专业能力", "项目经验", "团队协作"],
            "structure": "经历优先",
            "tone": "专业",
            "sections": ["work_experience", "skills"]
        })
        
        # 根据目标公司类型调整
        company_adjustments = self._adjust_for_company(
            profile.target_company_type,
            base_strategy
        )
        
        # 合并用户自定义技能重点
        final_keywords = list(set(
            base_strategy["keywords"] + profile.skill_focus
        ))
        
        return ContentStrategy(
            angle=base_strategy["angle"],
            keywords_emphasis=final_keywords,
            structure=company_adjustments.get("structure", base_strategy["structure"]),
            tone=company_adjustments.get("tone", base_strategy["tone"]),
            highlight_sections=company_adjustments.get("sections", base_strategy["sections"])
        )
    
    def _adjust_for_company(
        self,
        company_type: str,
        base_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """根据目标公司类型调整策略"""
        adjustments = {
            "大厂": {
                "keywords_add": ["规模化", "高并发", "系统设计"],
                "tone": "强调数据和规模"
            },
            "外企": {
                "keywords_add": ["跨文化", "全球化", "合规"],
                "tone": "强调软技能和国际化"
            },
            "创业公司": {
                "keywords_add": ["从0到1", "多面手", "快速迭代"],
                "tone": "强调全能和创业精神"
            },
            "国企": {
                "keywords_add": ["稳定", "规范", "汇报"],
                "tone": "强调合规和稳定性"
            }
        }
        
        adj = adjustments.get(company_type, {})
        
        result = base_strategy.copy()
        if "keywords_add" in adj:
            result["keywords"] = list(set(
                result["keywords"] + adj["keywords_add"]
            ))
        if "tone" in adj:
            result["tone"] = f"{result['tone']}，{adj['tone']}"
        
        return result
    
    async def enhance_with_jd(
        self,
        strategy: ContentStrategy,
        job_description: str
    ) -> ContentStrategy:
        """
        根据 JD 进一步优化策略
        
        Args:
            strategy: 基础策略
            job_description: 职位描述
        
        Returns:
            优化后的策略
        """
        try:
            # 使用 AI 提取 JD 关键词
            prompt = f"""从以下职位描述中提取关键要求：

{job_description}

请返回 JSON 格式：
{{
  "required_skills": ["技能1", "技能2"],
  "preferred_skills": ["加分技能1"],
  "key_responsibilities": ["职责1"],
  "culture_keywords": ["文化关键词1"]
}}"""
            
            response = await self.ai.optimize_content(
                original=prompt,
                optimization_type="polish"
            )
            
            jd_analysis = json.loads(response)
            
            # 合并关键词
            enhanced_keywords = list(set(
                strategy.keywords_emphasis +
                jd_analysis.get("required_skills", []) +
                jd_analysis.get("culture_keywords", [])
            ))
            
            return ContentStrategy(
                angle=strategy.angle,
                keywords_emphasis=enhanced_keywords,
                structure=strategy.structure,
                tone=strategy.tone,
                highlight_sections=strategy.highlight_sections
            )
            
        except Exception as e:
            print(f"[WARN] JD enhancement failed: {e}")
            return strategy
    
    def generate_system_prompt(self, strategy: ContentStrategy) -> str:
        """
        根据策略生成系统 Prompt
        
        Args:
            strategy: 生成策略
        
        Returns:
            系统级 Prompt
        """
        prompts = {
            "潜力导向": """你是一位资深 HR，擅长发现应届生的潜力。
重点突出：学习能力、项目经验、技术热情、快速上手能力。
语气：积极进取，充满朝气。""",
            
            "成长导向": """你是一位技术经理，看重候选人的成长轨迹。
重点突出：技术深度、独立负责能力、业务理解、快速成长。
语气：专业可靠，有发展潜力。""",
            
            "专家导向": """你是一位技术专家，需要展示技术领导力。
重点突出：架构设计、技术难点解决、效率提升、技术影响力。
语气：权威专业，技术深度。""",
            
            "影响力导向": """你是一位资深架构师，强调技术影响力。
重点突出：跨团队协作、复杂系统设计、行业贡献、技术布道。
语气：谦逊有力，技术领袖。""",
            
            "领导力导向": """你是一位技术管理者，展示管理能力。
重点突出：团队管理、项目交付、人才培养、资源协调。
语气：稳重果断，有领导魅力。""",
            
            "战略导向": """你是一位 CTO/VP，体现战略思维。
重点突出：战略规划、组织建设、业务增长、文化建设。
语气：高屋建瓴，战略视野。"""
        }
        
        base_prompt = prompts.get(
            strategy.angle,
            "你是一位专业简历撰写专家。"
        )
        
        # 添加关键词要求
        keywords_str = ", ".join(strategy.keywords_emphasis[:8])
        
        return f"""{base_prompt}

重点关键词：{keywords_str}
结构偏好：{strategy.structure}
语气要求：{strategy.tone}

输出要求：
- 使用中文撰写
- 返回 JSON 格式
- 突出上述关键词
- 符合目标读者期待"""


# 便捷函数
def create_personalization(
    level: str,
    years: int,
    career_type: str,
    target_company: str,
    target_position: str,
    **kwargs
) -> UserProfile:
    """快速创建用户画像"""
    return UserProfile(
        level=UserLevel(level),
        years_of_experience=years,
        career_type=CareerType(career_type),
        target_company_type=target_company,
        target_position=target_position,
        strengths=kwargs.get("strengths", []),
        skill_focus=kwargs.get("skill_focus", []),
        avoid_keywords=kwargs.get("avoid_keywords", [])
    )
