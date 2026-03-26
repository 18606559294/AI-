import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ResumePreview from '../ResumePreview';
import type { ResumeContent } from '@ai-resume/shared/types';

const mockContent: ResumeContent = {
  basic_info: {
    name: '测试用户',
    email: 'test@example.com',
    phone: '13800138000',
    location: '北京市',
    title: '软件工程师',
    summary: '一名热爱编程的软件工程师',
    job_intention: '前端开发工程师',
    self_introduction: '我有丰富的开发经验',
  },
  education: [
    {
      school: '北京大学',
      degree: '学士',
      major: '计算机科学与技术',
      start_year: '2018',
      end_year: '2022',
    },
  ],
  work_experience: [
    {
      company: '某科技公司',
      position: '前端工程师',
      start_year: '2022',
      end_year: '至今',
      description: '负责前端开发工作',
    },
  ],
  projects: [
    {
      name: '简历项目',
      role: '核心开发者',
      description: '使用 React 开发的简历系统',
      tech_stack: ['React', 'TypeScript', 'Vite'],
      url: 'https://example.com',
    },
  ],
  skills: [
    { name: 'JavaScript', level: '熟练' },
    { name: 'TypeScript', level: '熟练' },
    { name: 'React', level: '熟练' },
  ],
};

describe('ResumePreview Component', () => {
  it('渲染简历预览（现代模板）', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('测试用户')).toBeInTheDocument();
    expect(screen.getByText('软件工程师')).toBeInTheDocument();
    expect(screen.getByText('test@example.com')).toBeInTheDocument();
  });

  it('渲染简历预览（经典模板）', () => {
    render(<ResumePreview content={mockContent} template="classic" />);
    expect(screen.getByText('测试用户')).toBeInTheDocument();
    expect(screen.getByText('软件工程师')).toBeInTheDocument();
  });

  it('渲染简历预览（简约模板）', () => {
    render(<ResumePreview content={mockContent} template="minimal" />);
    expect(screen.getByText('测试用户')).toBeInTheDocument();
    expect(screen.getByText('软件工程师')).toBeInTheDocument();
  });

  it('渲染教育经历', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('北京大学')).toBeInTheDocument();
    expect(screen.getByText('计算机科学与技术')).toBeInTheDocument();
  });

  it('渲染工作经历', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('某科技公司')).toBeInTheDocument();
    expect(screen.getByText('前端工程师')).toBeInTheDocument();
  });

  it('渲染项目经历', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('简历项目')).toBeInTheDocument();
    expect(screen.getByText('核心开发者')).toBeInTheDocument();
  });

  it('渲染技能列表', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('JavaScript')).toBeInTheDocument();
    expect(screen.getByText('TypeScript')).toBeInTheDocument();
    expect(screen.getByText('React')).toBeInTheDocument();
  });

  it('处理空内容', () => {
    const emptyContent: ResumeContent = {
      basic_info: {},
      education: [],
      work_experience: [],
      projects: [],
      skills: [],
    };

    render(<ResumePreview content={emptyContent} template="modern" />);
    expect(screen.getByText('简历预览')).toBeInTheDocument();
  });

  it('默认使用现代模板', () => {
    const { container } = render(<ResumePreview content={mockContent} />);
    expect(container.querySelector('.modern-template')).toBeInTheDocument();
  });

  it('渲染求职意向', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('前端开发工程师')).toBeInTheDocument();
  });

  it('渲染自我介绍', () => {
    render(<ResumePreview content={mockContent} template="modern" />);
    expect(screen.getByText('我有丰富的开发经验')).toBeInTheDocument();
  });
});
