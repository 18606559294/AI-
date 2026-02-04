import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, isLoading, error, clearError } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    try {
      await login(email, password);
      navigate('/');
    } catch {
      // Error handled by store
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            AI 简历智能生成平台
          </h1>
          <p className="text-gray-600">登录以开始创建你的专业简历</p>
        </div>

        <div className="card p-8">
          <h2 className="text-xl font-semibold text-center mb-6">登录</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                邮箱
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="请输入邮箱"
                required
                data-testid="email-input"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                密码
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="请输入密码"
                required
                data-testid="password-input"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn btn-primary w-full py-3"
              data-testid="login-button"
            >
              {isLoading ? '登录中...' : '登录'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            还没有账号？{' '}
            <Link to="/register" className="text-primary-600 hover:underline font-medium" data-testid="register-link">
              立即注册
            </Link>
          </div>
        </div>

        <div className="mt-6 text-center text-xs text-gray-500">
          <a href="/terms" className="hover:underline" data-testid="terms-link">用户协议</a>
          {' · '}
          <a href="/privacy" className="hover:underline" data-testid="privacy-link">隐私政策</a>
        </div>
      </div>
    </div>
  );
}
