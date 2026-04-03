/**
 * PrivacyPage 组件测试
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import PrivacyPage from './PrivacyPage';

describe('PrivacyPage', () => {
  it('渲染隐私政策页面', () => {
    render(
      <MemoryRouter>
        <PrivacyPage />
      </MemoryRouter>
    );

    expect(screen.getByText('隐私政策')).toBeInTheDocument();
  });

  it('显示最后更新日期', () => {
    render(
      <MemoryRouter>
        <PrivacyPage />
      </MemoryRouter>
    );

    expect(screen.getByText(/最后更新日期：/)).toBeInTheDocument();
    expect(screen.getByText(/2024年1月1日/)).toBeInTheDocument();
  });

  it('包含所有主要章节', () => {
    const { container } = render(
      <MemoryRouter>
        <PrivacyPage />
      </MemoryRouter>
    );

    // 检查页面主要内容是否存在
    const pageTitle = screen.getByText('隐私政策');
    expect(pageTitle).toBeInTheDocument();

    // 检查是否有section标题（隐私政策页面有多个section）
    const headings = container.querySelectorAll('h2');
    expect(headings.length).toBeGreaterThan(0);
  });

  it('显示联系邮箱', () => {
    render(
      <MemoryRouter>
        <PrivacyPage />
      </MemoryRouter>
    );

    expect(screen.getByText(/privacy@/)).toBeInTheDocument();
  });

  it('有返回登录链接', () => {
    render(
      <MemoryRouter>
        <PrivacyPage />
      </MemoryRouter>
    );

    expect(screen.getByText('返回登录')).toBeInTheDocument();
  });

  it('包含AI服务说明', () => {
    render(
      <MemoryRouter>
        <PrivacyPage />
      </MemoryRouter>
    );

    // 检查是否有 AI 相关内容
    const aiContent = screen.queryAllByText(/AI服务/);
    expect(aiContent.length).toBeGreaterThan(0);
  });
});
