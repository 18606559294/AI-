/**
 * HelpPage 组件测试
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import HelpPage from './HelpPage';

// Mock UIComponents
vi.mock('../components/UIComponents', () => ({
  GradientText: ({ children }: { children: React.ReactNode }) => <span className="gradient-text">{children}</span>,
  Orb: () => null,
}));

// Mock SEO component
vi.mock('../components/SEO', () => ({
  SEO: () => null,
}));

describe('HelpPage', () => {
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <HelmetProvider>
      <MemoryRouter>
        {children}
      </MemoryRouter>
    </HelmetProvider>
  );

  it('渲染帮助中心页面', () => {
    render(<HelpPage />, { wrapper });

    expect(screen.getByText(/帮助中心/)).toBeInTheDocument();
    expect(screen.getByText('常见问题解答和使用指南')).toBeInTheDocument();
  });

  it('显示快速导航卡片', () => {
    render(<HelpPage />, { wrapper });

    expect(screen.getByText('新用户注册')).toBeInTheDocument();
    expect(screen.getByText('模板库')).toBeInTheDocument();
    expect(screen.getByText('联系客服')).toBeInTheDocument();
  });

  it('显示所有 FAQ 问题', () => {
    render(<HelpPage />, { wrapper });

    const expectedQuestions = [
      '如何创建一份新简历？',
      '如何使用 AI 功能生成简历？',
      '支持哪些导出格式？',
      '如何更换简历模板？',
      '忘记密码怎么办？',
      '如何联系客服？'
    ];

    expectedQuestions.forEach(question => {
      expect(screen.getByText(question)).toBeInTheDocument();
    });
  });

  it('显示使用指南', () => {
    render(<HelpPage />, { wrapper });

    expect(screen.getByText('使用指南')).toBeInTheDocument();
    expect(screen.getByText('1. 创建账号')).toBeInTheDocument();
    expect(screen.getByText('2. 创建简历')).toBeInTheDocument();
    expect(screen.getByText('3. AI 优化')).toBeInTheDocument();
    expect(screen.getByText('4. 导出简历')).toBeInTheDocument();
  });

  it('有返回登录链接', () => {
    render(<HelpPage />, { wrapper });

    expect(screen.getByText('返回登录')).toBeInTheDocument();
  });
});
