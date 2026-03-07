import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { initApiClient, getApiClient } from '@ai-resume/shared/api';
import { storage } from '@ai-resume/shared';
import App from './App';
import './index.css';

// 初始化API客户端，配置token获取
initApiClient(() => storage.getToken());

// 设置API Base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
getApiClient().setBaseURL(API_BASE_URL);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter basename="/resume">
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
);
