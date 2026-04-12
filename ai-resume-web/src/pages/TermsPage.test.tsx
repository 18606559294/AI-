/**
 * TermsPage 组件测试
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import TermsPage from './TermsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

describe('TermsPage', () => {
  it('渲染用户协议页面', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <TermsPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('用户协议')).toBeInTheDocument();
  });

  it('显示最后更新日期', () => {
    render(
      <MemoryRouter>
        <TermsPage />
      </MemoryRouter>
    );

    expect(screen.getByText(/最后更新日期：/)).toBeInTheDocument();
    expect(screen.getByText(/2024年1月1日/)).toBeInTheDocument();
  });

  it('包含主要章节标题', () => {
    const { container } = render(
      <MemoryRouter>
        <TermsPage />
      </MemoryRouter>
    );

    // 检查页面主要内容是否存在
    const pageTitle = screen.getByText('用户协议');
    expect(pageTitle).toBeInTheDocument();

    // 检查是否有section标题
    const headings = container.querySelectorAll('h2');
    expect(headings.length).toBeGreaterThan(0);
  });

  it('有返回登录链接', () => {
    render(
      <MemoryRouter>
        <TermsPage />
      </MemoryRouter>
    );

    expect(screen.getByText('登录')).toBeInTheDocument();
  });

  it('显示平台Logo', () => {
    render(
      <MemoryRouter>
        <TermsPage />
      </MemoryRouter>
    );

    expect(screen.getByText('AI 简历')).toBeInTheDocument();
  });
});
