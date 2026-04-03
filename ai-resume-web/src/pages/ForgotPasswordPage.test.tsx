/**
 * ForgotPasswordPage 组件测试
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import ForgotPasswordPage from './ForgotPasswordPage';

// Mock UIComponents
vi.mock('../components/UIComponents', () => ({
  Button: ({ children, loading, disabled, ...props }: any) => (
    <button {...props} disabled={disabled || loading} data-testid={props['data-testid']}>
      {children}
    </button>
  ),
  Input: ({ label, ...props }: any) => (
    <div>
      {label && <label>{label}</label>}
      <input {...props} data-testid={props['data-testid']} />
    </div>
  ),
  GradientText: ({ children }: { children: React.ReactNode }) => <span className="gradient-text">{children}</span>,
  Orb: () => null,
}));

// Mock fetch
global.fetch = vi.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
  } as Response)
);

describe('ForgotPasswordPage', () => {
  it('渲染重置密码页面', () => {
    render(
      <MemoryRouter>
        <ForgotPasswordPage />
      </MemoryRouter>
    );

    expect(screen.getByText('重置密码')).toBeInTheDocument();
  });

  it('默认显示邮箱输入步骤', () => {
    render(
      <MemoryRouter>
        <ForgotPasswordPage />
      </MemoryRouter>
    );

    expect(screen.getByText('输入邮箱获取验证码')).toBeInTheDocument();
    expect(screen.getByText('邮箱地址')).toBeInTheDocument();
    expect(screen.getByText('发送验证码')).toBeInTheDocument();
  });

  it('显示返回登录链接', () => {
    render(
      <MemoryRouter>
        <ForgotPasswordPage />
      </MemoryRouter>
    );

    expect(screen.getByText('返回登录')).toBeInTheDocument();
  });

  it('有进度指示器', () => {
    const { container } = render(
      <MemoryRouter>
        <ForgotPasswordPage />
      </MemoryRouter>
    );

    // 应该有3个进度条div
    const progressBars = container.querySelectorAll('.rounded-full');
    expect(progressBars.length).toBe(3);
  });
});
