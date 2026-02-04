import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { appWindow } from '@tauri-apps/api/window';
import { useEffect } from 'react';
import App from './App';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// Wrapper to handle Tauri window state
function AppWrapper() {
  const location = useLocation();

  useEffect(() => {
    // Set window title based on route
    const titles: Record<string, string> = {
      '/': 'AI 简历 - 首页',
      '/login': 'AI 简历 - 登录',
      '/register': 'AI 简历 - 注册',
      '/resumes': 'AI 简历 - 我的简历',
      '/templates': 'AI 简历 - 模板库',
      '/profile': 'AI 简历 - 个人中心',
      '/settings': 'AI 简历 - 设置',
    };

    const title = titles[location.pathname] || 'AI 简历智能生成平台';
    document.title = title;

    // Update Tauri window title
    appWindow.setTitle(title).catch(console.error);
  }, [location]);

  return <App />;
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppWrapper />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
);
