"""
导出服务 - PDF/Word/图片导出
"""
import io
import os
from typing import Dict, Any, Optional
from datetime import datetime
from jinja2 import Template as JinjaTemplate
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

# PDF 导出需要 WeasyPrint
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False


class ExportService:
    """导出服务类"""
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
    
    async def to_pdf(
        self,
        resume_content: Dict[str, Any],
        style_config: Optional[Dict[str, Any]] = None,
        template_html: Optional[str] = None
    ) -> bytes:
        """导出为PDF"""
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError("PDF导出功能需要安装 WeasyPrint")

        # 生成HTML（内联CSS样式）
        html_content = self._generate_html_with_inline_css(resume_content, style_config, template_html)

        # 转换为PDF（使用WeasyPrint 60.2的正确API）
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()

        return pdf_bytes

    def _generate_html_with_inline_css(
        self,
        resume_content: Dict[str, Any],
        style_config: Optional[Dict[str, Any]] = None,
        template_html: Optional[str] = None
    ) -> str:
        """生成内联CSS的HTML内容"""
        if template_html:
            template = JinjaTemplate(template_html)
            return template.render(resume=resume_content, style=style_config or {})

        # 生成HTML和CSS
        html_body = self._generate_html(resume_content, style_config, template_html)
        css_content = self._generate_css(style_config)

        # 组合完整HTML
        full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_content.get('basic_info', {}).get('name', '简历')}</title>
    <style>
    {css_content}
    </style>
</head>
<body>
{html_body}
</body>
</html>
        """
        return full_html
    
    async def to_word(
        self,
        resume_content: Dict[str, Any],
        style_config: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """导出为Word文档"""
        doc = Document()
        
        # 设置文档样式
        self._setup_word_styles(doc, style_config)
        
        # 基本信息
        basic_info = resume_content.get("basic_info", {})
        if basic_info:
            self._add_basic_info_section(doc, basic_info)
        
        # 个人简介
        if basic_info.get("self_introduction"):
            self._add_section(doc, "个人简介", basic_info["self_introduction"])
        
        # 教育经历
        education = resume_content.get("education", [])
        if education:
            self._add_education_section(doc, education)
        
        # 工作经历
        work_experience = resume_content.get("work_experience", [])
        if work_experience:
            self._add_work_section(doc, work_experience)
        
        # 项目经历
        projects = resume_content.get("projects", [])
        if projects:
            self._add_project_section(doc, projects)
        
        # 技能
        skills = resume_content.get("skills", [])
        if skills:
            self._add_skills_section(doc, skills)
        
        # 证书
        certifications = resume_content.get("certifications", [])
        if certifications:
            self._add_certifications_section(doc, certifications)
        
        # 保存到字节流
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer.read()
    
    async def to_html(
        self,
        resume_content: Dict[str, Any],
        style_config: Optional[Dict[str, Any]] = None,
        template_html: Optional[str] = None
    ) -> str:
        """导出为HTML"""
        html_content = self._generate_html(resume_content, style_config, template_html)
        css_content = self._generate_css(style_config)
        
        # 组合完整HTML
        full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_content.get('basic_info', {}).get('name', '简历')}</title>
    <style>
    {css_content}
    </style>
</head>
<body>
{html_content}
</body>
</html>
        """
        return full_html
    
    def _generate_html(
        self,
        resume_content: Dict[str, Any],
        style_config: Optional[Dict[str, Any]] = None,
        template_html: Optional[str] = None
    ) -> str:
        """生成HTML内容"""
        if template_html:
            template = JinjaTemplate(template_html)
            return template.render(resume=resume_content, style=style_config or {})
        
        # 默认HTML模板
        basic_info = resume_content.get("basic_info", {})
        
        html_parts = ['<div class="resume">']
        
        # 头部信息
        html_parts.append('<header class="resume-header">')
        if basic_info.get("name"):
            html_parts.append(f'<h1 class="name">{basic_info["name"]}</h1>')
        if basic_info.get("job_intention"):
            html_parts.append(f'<p class="job-intention">{basic_info["job_intention"]}</p>')
        
        # 联系方式
        contact_info = []
        if basic_info.get("phone"):
            contact_info.append(f'<span>📱 {basic_info["phone"]}</span>')
        if basic_info.get("email"):
            contact_info.append(f'<span>📧 {basic_info["email"]}</span>')
        if basic_info.get("location"):
            contact_info.append(f'<span>📍 {basic_info["location"]}</span>')
        if contact_info:
            html_parts.append(f'<div class="contact-info">{" | ".join(contact_info)}</div>')
        html_parts.append('</header>')
        
        # 个人简介
        if basic_info.get("self_introduction"):
            html_parts.append('<section class="section">')
            html_parts.append('<h2 class="section-title">个人简介</h2>')
            html_parts.append(f'<p>{basic_info["self_introduction"]}</p>')
            html_parts.append('</section>')
        
        # 教育经历
        education = resume_content.get("education", [])
        if education:
            html_parts.append('<section class="section">')
            html_parts.append('<h2 class="section-title">教育经历</h2>')
            for edu in education:
                html_parts.append('<div class="item">')
                html_parts.append(f'<div class="item-header">')
                html_parts.append(f'<strong>{edu.get("school", "")}</strong>')
                html_parts.append(f'<span>{edu.get("major", "")} | {edu.get("degree", "")}</span>')
                html_parts.append('</div>')
                if edu.get("description"):
                    html_parts.append(f'<p>{edu["description"]}</p>')
                html_parts.append('</div>')
            html_parts.append('</section>')
        
        # 工作经历
        work_experience = resume_content.get("work_experience", [])
        if work_experience:
            html_parts.append('<section class="section">')
            html_parts.append('<h2 class="section-title">工作经历</h2>')
            for work in work_experience:
                html_parts.append('<div class="item">')
                html_parts.append(f'<div class="item-header">')
                html_parts.append(f'<strong>{work.get("company", "")}</strong>')
                html_parts.append(f'<span>{work.get("position", "")}</span>')
                html_parts.append('</div>')
                if work.get("description"):
                    html_parts.append(f'<p>{work["description"]}</p>')
                achievements = work.get("achievements", [])
                if achievements:
                    html_parts.append('<ul>')
                    for achievement in achievements:
                        html_parts.append(f'<li>{achievement}</li>')
                    html_parts.append('</ul>')
                html_parts.append('</div>')
            html_parts.append('</section>')
        
        # 项目经历
        projects = resume_content.get("projects", [])
        if projects:
            html_parts.append('<section class="section">')
            html_parts.append('<h2 class="section-title">项目经历</h2>')
            for project in projects:
                html_parts.append('<div class="item">')
                html_parts.append(f'<div class="item-header">')
                html_parts.append(f'<strong>{project.get("name", "")}</strong>')
                if project.get("role"):
                    html_parts.append(f'<span>{project["role"]}</span>')
                html_parts.append('</div>')
                if project.get("description"):
                    html_parts.append(f'<p>{project["description"]}</p>')
                tech_stack = project.get("tech_stack", [])
                if tech_stack:
                    html_parts.append(f'<p class="tech-stack">技术栈: {", ".join(tech_stack)}</p>')
                html_parts.append('</div>')
            html_parts.append('</section>')
        
        # 技能
        skills = resume_content.get("skills", [])
        if skills:
            html_parts.append('<section class="section">')
            html_parts.append('<h2 class="section-title">专业技能</h2>')
            html_parts.append('<div class="skills">')
            for skill in skills:
                html_parts.append(f'<span class="skill-tag">{skill.get("name", "")}</span>')
            html_parts.append('</div>')
            html_parts.append('</section>')
        
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _generate_css(self, style_config: Optional[Dict[str, Any]] = None) -> str:
        """生成CSS样式"""
        config = style_config or {}
        primary_color = config.get("primary_color", "#2B2B2B")
        secondary_color = config.get("secondary_color", "#666666")
        font_family = config.get("font_family", "Microsoft YaHei, sans-serif")
        font_size = config.get("font_size", 12)
        line_height = config.get("line_height", 1.6)
        
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: {font_family};
            font-size: {font_size}pt;
            line-height: {line_height};
            color: {primary_color};
            background: #fff;
        }}
        .resume {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
        }}
        .resume-header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid {primary_color};
        }}
        .name {{
            font-size: 28pt;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .job-intention {{
            font-size: 14pt;
            color: {secondary_color};
            margin-bottom: 10px;
        }}
        .contact-info {{
            font-size: 10pt;
            color: {secondary_color};
        }}
        .contact-info span {{
            margin: 0 10px;
        }}
        .section {{
            margin-bottom: 25px;
        }}
        .section-title {{
            font-size: 14pt;
            font-weight: bold;
            color: {primary_color};
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid #ddd;
        }}
        .item {{
            margin-bottom: 15px;
        }}
        .item-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}
        .item-header strong {{
            color: {primary_color};
        }}
        .item-header span {{
            color: {secondary_color};
        }}
        .item p {{
            color: {secondary_color};
            margin-bottom: 5px;
        }}
        .item ul {{
            margin-left: 20px;
            color: {secondary_color};
        }}
        .item li {{
            margin-bottom: 3px;
        }}
        .skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .skill-tag {{
            background: #f5f5f5;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 10pt;
        }}
        .tech-stack {{
            font-size: 10pt;
            color: {secondary_color};
            font-style: italic;
        }}
        @media print {{
            .resume {{
                padding: 20px;
            }}
        }}
        """
    
    def _setup_word_styles(self, doc: Document, style_config: Optional[Dict[str, Any]] = None):
        """设置Word文档样式"""
        config = style_config or {}
        
        # 设置默认样式
        style = doc.styles['Normal']
        font = style.font
        font.name = config.get("font_family", "微软雅黑")
        font.size = Pt(config.get("font_size", 11))
    
    def _add_basic_info_section(self, doc: Document, basic_info: Dict[str, Any]):
        """添加基本信息部分"""
        # 姓名
        if basic_info.get("name"):
            p = doc.add_paragraph()
            run = p.add_run(basic_info["name"])
            run.bold = True
            run.font.size = Pt(22)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 求职意向
        if basic_info.get("job_intention"):
            p = doc.add_paragraph()
            p.add_run(basic_info["job_intention"])
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 联系方式
        contact_parts = []
        if basic_info.get("phone"):
            contact_parts.append(basic_info["phone"])
        if basic_info.get("email"):
            contact_parts.append(basic_info["email"])
        if basic_info.get("location"):
            contact_parts.append(basic_info["location"])
        
        if contact_parts:
            p = doc.add_paragraph()
            p.add_run(" | ".join(contact_parts))
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph()  # 空行
    
    def _add_section(self, doc: Document, title: str, content: str):
        """添加通用段落"""
        p = doc.add_paragraph()
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(14)
        
        doc.add_paragraph(content)
        doc.add_paragraph()
    
    def _add_education_section(self, doc: Document, education: list):
        """添加教育经历"""
        p = doc.add_paragraph()
        run = p.add_run("教育经历")
        run.bold = True
        run.font.size = Pt(14)
        
        for edu in education:
            p = doc.add_paragraph()
            p.add_run(f"{edu.get('school', '')} - {edu.get('major', '')}").bold = True
            if edu.get("degree"):
                p.add_run(f" ({edu['degree']})")
            if edu.get("description"):
                doc.add_paragraph(edu["description"])
        
        doc.add_paragraph()
    
    def _add_work_section(self, doc: Document, work_experience: list):
        """添加工作经历"""
        p = doc.add_paragraph()
        run = p.add_run("工作经历")
        run.bold = True
        run.font.size = Pt(14)
        
        for work in work_experience:
            p = doc.add_paragraph()
            p.add_run(f"{work.get('company', '')} - {work.get('position', '')}").bold = True
            
            if work.get("description"):
                doc.add_paragraph(work["description"])
            
            for achievement in work.get("achievements", []):
                doc.add_paragraph(f"• {achievement}")
        
        doc.add_paragraph()
    
    def _add_project_section(self, doc: Document, projects: list):
        """添加项目经历"""
        p = doc.add_paragraph()
        run = p.add_run("项目经历")
        run.bold = True
        run.font.size = Pt(14)
        
        for project in projects:
            p = doc.add_paragraph()
            p.add_run(project.get('name', '')).bold = True
            if project.get("role"):
                p.add_run(f" ({project['role']})")
            
            if project.get("description"):
                doc.add_paragraph(project["description"])
            
            if project.get("tech_stack"):
                doc.add_paragraph(f"技术栈: {', '.join(project['tech_stack'])}")
        
        doc.add_paragraph()
    
    def _add_skills_section(self, doc: Document, skills: list):
        """添加技能"""
        p = doc.add_paragraph()
        run = p.add_run("专业技能")
        run.bold = True
        run.font.size = Pt(14)
        
        skill_names = [skill.get("name", "") for skill in skills if skill.get("name")]
        if skill_names:
            doc.add_paragraph(" | ".join(skill_names))
        
        doc.add_paragraph()
    
    def _add_certifications_section(self, doc: Document, certifications: list):
        """添加证书"""
        p = doc.add_paragraph()
        run = p.add_run("证书荣誉")
        run.bold = True
        run.font.size = Pt(14)
        
        for cert in certifications:
            doc.add_paragraph(f"• {cert.get('name', '')}")
        
        doc.add_paragraph()
