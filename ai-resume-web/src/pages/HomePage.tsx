import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

export default function HomePage() {
  const { user, logout } = useAuthStore();

  const displayName = user?.nickname ?? user?.email?.split('@')[0] ?? '用户';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航栏 */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-8">
              <h1 className="text-xl font-bold text-primary-600">
                AI 简历
              </h1>
              <nav className="hidden md:flex gap-6">
                <Link to="/resumes" className="text-gray-700 hover:text-primary-600 transition-colors">
                  我的简历
                </Link>
                <Link to="/templates" className="text-gray-700 hover:text-primary-600 transition-colors">
                  模板库
                </Link>
              </nav>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600 hidden sm:block">
                {displayName}
              </span>
              <Link
                to="/settings"
                className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </Link>
              <button
                onClick={logout}
                className="btn btn-secondary text-sm py-2"
              >
                退出
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 主内容区域 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 欢迎横幅 */}
        <div className="bg-gradient-to-r from-primary-500 to-primary-700 rounded-2xl p-8 mb-8 text-white">
          <h2 className="text-2xl font-bold mb-2">
            欢迎回来，{displayName}！
          </h2>
          <p className="text-primary-100 mb-6">
            使用 AI 技术快速创建专业简历，让求职更轻松
          </p>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/resumes/new"
              className="bg-white text-primary-600 px-6 py-2 rounded-lg font-medium hover:bg-primary-50 transition-colors"
            >
              创建新简历
            </Link>
            <Link
              to="/templates"
              className="bg-primary-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors border border-primary-400"
            >
              浏览模板
            </Link>
          </div>
        </div>

        {/* 快捷功能 */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Link
            to="/resumes/new"
            className="card p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary-200 transition-colors">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">创建新简历</h3>
            <p className="text-gray-600 text-sm">
              从零开始或使用 AI 智能生成你的专业简历
            </p>
          </Link>

          <Link
            to="/templates"
            className="card p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-200 transition-colors">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">选择模板</h3>
            <p className="text-gray-600 text-sm">
              浏览精美的简历模板，选择最适合你的设计
            </p>
          </Link>

          <Link
            to="/profile"
            className="card p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">个人中心</h3>
            <p className="text-gray-600 text-sm">
              管理你的账户信息和会员订阅
            </p>
          </Link>
        </div>

        {/* 最近简历 */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">最近编辑</h2>
            <Link to="/resumes" className="text-primary-600 hover:underline text-sm">
              查看全部 →
            </Link>
          </div>
          <div className="card p-8 text-center">
            <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-gray-500 mb-4">还没有简历</p>
            <Link
              to="/resumes/new"
              className="btn btn-primary"
            >
              创建第一份简历
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
