"""
经历深度挖掘框架
从平淡的工作描述中发现亮点，生成有价值的简历内容
"""
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ExperienceDimensions:
    """经历五维度分析结果"""
    # 技术维度
    tech_stack: List[str]                    # 技术栈
    architecture_contribution: str           # 架构贡献
    technical_challenges: List[str]          # 解决的技术难题
    
    # 业务维度
    business_context: str                    # 业务背景
    metrics: Dict[str, Any]                  # 量化指标 {before, after, unit}
    business_impact: str                     # 业务影响
    
    # 协作维度
    team_size: int                           # 团队规模
    cross_functional: bool                   # 是否跨职能协作
    stakeholder_management: List[str]        # 利益相关方管理
    
    # 创新维度
    innovations: List[str]                   # 创新点
    lessons_learned: List[str]               # 踩坑经验
    
    # 成长维度
    skills_gained: List[str]                 # 获得的技能
    leadership_growth: str                   # 领导力成长


class ExperienceMiner:
    """
    经历挖掘器
    
    使用 LLM 深度分析工作经历，提取多维度信息。
    适用于：
    1. 用户输入简单时，自动挖掘深度信息
    2. 发现用户自己都没意识到的亮点
    3. 生成量化建议
    """
    
    def __init__(self, ai_provider):
        """
        初始化
        
        Args:
            ai_provider: AI 提供商实例（如 OpenAIProviderV2）
        """
        self.ai = ai_provider
    
    async def mine_experience(
        self,
        title: str,
        company: str,
        description: str,
        period: str = "",
        context: Optional[Dict[str, Any]] = None
    ) -> ExperienceDimensions:
        """
        深度挖掘一段工作经历
        
        Args:
            title: 职位名称
            company: 公司名称
            description: 工作描述（可能很简略）
            period: 时间段
            context: 额外上下文（如行业、公司规模等）
        
        Returns:
            ExperienceDimensions 五维度分析结果
        """
        prompt = self._build_mining_prompt(
            title, company, description, period, context
        )
        
        try:
            response = await self.ai.optimize_content(
                original=prompt,
                optimization_type="polish",
                context="深度挖掘"
            )
            
            # 解析返回的 JSON
            result = json.loads(response)
            return self._parse_dimensions(result)
            
        except Exception as e:
            print(f"[WARN] Experience mining failed: {e}")
            # 返回默认结果
            return self._default_dimensions()
    
    def _build_mining_prompt(
        self,
        title: str,
        company: str,
        description: str,
        period: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """构建挖掘 Prompt"""
        ctx_str = json.dumps(context, ensure_ascii=False) if context else "{}"
        
        return f"""请深度分析以下工作经历，从五个维度提取信息：

【基本信息】
职位: {title}
公司: {company}
时间: {period}
描述: {description}
上下文: {ctx_str}

请按以下 JSON 格式返回分析结果：
{{
  "tech": {{
    "stack": ["技术1", "技术2"],
    "architecture": "架构贡献描述",
    "challenges": ["难题1", "难题2"]
  }},
  "business": {{
    "context": "业务背景",
    "metrics": {{"before": "之前", "after": "之后", "unit": "单位"}},
    "impact": "业务影响"
  }},
  "collaboration": {{
    "team_size": 5,
    "cross_functional": true,
    "stakeholders": ["产品经理", "设计师"]
  }},
  "innovation": {{
    "innovations": ["创新点1"],
    "lessons": ["经验教训1"]
  }},
  "growth": {{
    "skills": ["技能1", "技能2"],
    "leadership": "领导力成长描述"
  }}
}}

要求：
1. 如果信息无法推断，请合理推测（基于行业常识）
2. metrics 尽可能给出具体数字
3. 挖掘用户描述中未明说的亮点"""

    def _parse_dimensions(self, data: Dict[str, Any]) -> ExperienceDimensions:
        """解析维度数据"""
        tech = data.get("tech", {})
        business = data.get("business", {})
        collab = data.get("collaboration", {})
        innov = data.get("innovation", {})
        growth = data.get("growth", {})
        
        return ExperienceDimensions(
            tech_stack=tech.get("stack", []),
            architecture_contribution=tech.get("architecture", ""),
            technical_challenges=tech.get("challenges", []),
            
            business_context=business.get("context", ""),
            metrics=business.get("metrics", {}),
            business_impact=business.get("impact", ""),
            
            team_size=collab.get("team_size", 0),
            cross_functional=collab.get("cross_functional", False),
            stakeholder_management=collab.get("stakeholders", []),
            
            innovations=innov.get("innovations", []),
            lessons_learned=innov.get("lessons", []),
            
            skills_gained=growth.get("skills", []),
            leadership_growth=growth.get("leadership", "")
        )
    
    def _default_dimensions(self) -> ExperienceDimensions:
        """默认维度数据"""
        return ExperienceDimensions(
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
    
    def generate_star_description(
        self,
        dims: ExperienceDimensions,
        highlight: str = "balanced"  # "tech", "business", "leadership", "balanced"
    ) -> str:
        """
        基于维度生成 STAR 法则描述
        
        Args:
            dims: 维度分析结果
            highlight: 突出方向
        
        Returns:
            STAR 法则描述
        """
        parts = []
        
        # Situation
        if dims.business_context:
            parts.append(f"在{dims.business_context}的背景下")
        
        # Task
        parts.append(f"负责{dims.architecture_contribution or '核心功能开发'}")
        
        # Action
        actions = []
        if dims.tech_stack:
            actions.append(f"使用{', '.join(dims.tech_stack[:3])}等技术栈")
        if dims.team_size > 0:
            actions.append(f"协调{dims.team_size}人团队")
        if dims.cross_functional:
            actions.append(f"与{dims.stakeholder_management[0] if dims.stakeholder_management else '多方'}协作")
        
        if actions:
            parts.append("，".join(actions))
        
        # Result
        if dims.metrics:
            before = dims.metrics.get("before", "")
            after = dims.metrics.get("after", "")
            unit = dims.metrics.get("unit", "")
            if before and after:
                parts.append(f"实现从{before}到{after}的{unit}提升")
            elif after:
                parts.append(f"达成{after}{unit}")
        
        return "。".join([p for p in parts if p])
    
    def suggest_quantification(
        self,
        dims: ExperienceDimensions
    ) -> List[str]:
        """
        生成量化建议
        
        当用户描述缺乏数字时，建议可以量化的方向
        
        Returns:
            建议列表
        """
        suggestions = []
        
        if not dims.metrics:
            suggestions.append("建议添加：性能提升百分比、用户增长数、收入贡献等")
        
        if dims.team_size == 0:
            suggestions.append("建议说明：团队规模、汇报层级")
        
        if not dims.technical_challenges:
            suggestions.append("建议补充：技术难点、架构决策")
        
        return suggestions


# 便捷函数
async def mine_work_experience(
    ai_provider,
    title: str,
    company: str,
    description: str,
    **kwargs
) -> Dict[str, Any]:
    """
    快速挖掘工作经历
    
    Returns:
        包含 dimensions 和 star_description 的字典
    """
    miner = ExperienceMiner(ai_provider)
    dims = await miner.mine_experience(title, company, description, **kwargs)
    
    return {
        "dimensions": asdict(dims),
        "star_description": miner.generate_star_description(dims),
        "suggestions": miner.suggest_quantification(dims)
    }
