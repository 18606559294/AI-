/**
 * AboutPage 组件测试
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AboutPage from './AboutPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

describe('AboutPage', () => {
  it('渲染关于我们页面', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <AboutPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('关于我们')).toBeInTheDocument();
  });

  it('显示产品介绍', () => {
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    expect(screen.getByText('AI 简历智能生成平台')).toBeInTheDocument();
    expect(screen.getByText(/利用前沿 AI 技术/)).toBeInTheDocument();
  });

  it('显示统计数据', () => {
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    expect(screen.getByText('50+')).toBeInTheDocument();
    expect(screen.getByText('专业模板')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('AI 模型')).toBeInTheDocument();
    expect(screen.getByText('100K+')).toBeInTheDocument();
    expect(screen.getByText('服务用户')).toBeInTheDocument();
    expect(screen.getByText('98%')).toBeInTheDocument();
    expect(screen.getByText('满意度')).toBeInTheDocument();
  });

  it('显示核心功能', () => {
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    expect(screen.getByText('核心功能')).toBeInTheDocument();
    expect(screen.getByText('AI 智能生成')).toBeInTheDocument();
    expect(screen.getByText('精美模板')).toBeInTheDocument();
    expect(screen.getByText('多格式导出')).toBeInTheDocument();
    expect(screen.getByText('安全可靠')).toBeInTheDocument();
  });

  it('显示联系信息', () => {
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    expect(screen.getByText('联系我们')).toBeInTheDocument();
    expect(screen.getByText('support@airesume.com')).toBeInTheDocument();
    expect(screen.getByText('https://github.com/airesume')).toBeInTheDocument();
  });

  it('显示版本信息', () => {
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    expect(screen.getByText('版本 1.0.0')).toBeInTheDocument();
    expect(screen.getByText(/© 2026 AI Resume/)).toBeInTheDocument();
  });

  it('导航链接正确', () => {
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    expect(screen.getByText('AI 简历')).toBeInTheDocument();
    expect(screen.getByText('我的简历')).toBeInTheDocument();
    expect(screen.getByText('模板库')).toBeInTheDocument();
  });
});
