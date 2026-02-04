import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register, isLoading, error, clearError } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
    const [countdown, setCountdown] = useState(0);

  const validatePassword = (): string | null => {
    if (password.length < 6) return '密码长度至少6位';
    if (!/[A-Za-z]/.test(password)) return '密码必须包含字母';
    if (!/\d/.test(password)) return '密码必须包含数字';
    return null;
  };

  const handleSendCode = async () => {
    // TODO: 实现发送验证码
    setCountdown(60);

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    if (password !== confirmPassword) {
      return;
    }

    const passwordError = validatePassword();
    if (passwordError) {
      return;
    }

    try {
      await register(email, password, {
        username: username || undefined,
        verification_code: verificationCode || undefined,
      });
      navigate('/');
    } catch {
      // Error handled by store
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4 py-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            AI 简历智能生成平台
          </h1>
          <p className="text-gray-600">创建账号，开启智能简历之旅</p>
        </div>

        <div className="card p-8">
          <h2 className="text-xl font-semibold text-center mb-6">注册</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                邮箱 *
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="请输入邮箱"
                required
                data-testid="register-email-input"
              />
            </div>

            <div>
              <label htmlFor="code" className="block text-sm font-medium text-gray-700 mb-1">
                验证码
              </label>
              <div className="flex gap-2">
                <input
                  id="code"
                  type="text"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  className="input flex-1"
                  placeholder="请输入验证码"
                  maxLength={6}
                  data-testid="code-input"
                />
                <button
                  type="button"
                  onClick={handleSendCode}
                  disabled={countdown > 0 || !email}
                  className="btn btn-secondary whitespace-nowrap"
                  data-testid="send-code-button"
                >
                  {countdown > 0 ? `${countdown}秒` : '发送验证码'}
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                用户名
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input"
                placeholder="请输入用户名（可选）"
                data-testid="username-input"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                密码 *
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="至少6位，包含字母和数字"
                required
                data-testid="register-password-input"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                确认密码 *
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="input"
                placeholder="请再次输入密码"
                required
                data-testid="confirm-password-input"
              />
              {confirmPassword && password !== confirmPassword && (
                <p className="text-red-500 text-sm mt-1" data-testid="password-mismatch-error">两次输入的密码不一致</p>
              )}
            </div>

            <div className="flex items-start gap-2">
              <input
                id="terms"
                type="checkbox"
                required
                className="mt-1"
                data-testid="terms-checkbox"
              />
              <label htmlFor="terms" className="text-sm text-gray-600">
                我已阅读并同意{' '}
                <Link to="/terms" className="text-primary-600 hover:underline">
                  《用户协议》
                </Link>
                {' 和 '}
                <Link to="/privacy" className="text-primary-600 hover:underline">
                  《隐私政策》
                </Link>
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading || password !== confirmPassword}
              className="btn btn-primary w-full py-3"
              data-testid="register-button"
            >
              {isLoading ? '注册中...' : '注册'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            已有账号？{' '}
            <Link to="/login" className="text-primary-600 hover:underline font-medium" data-testid="login-link">
              立即登录
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
