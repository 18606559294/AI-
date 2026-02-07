import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false, // 禁用并行运行以确保服务器稳定
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1, // 增加重试次数
  workers: 1, // 单个worker避免并发问题
  reporter: 'html',
  timeout: 120000, // 增加单个测试超时时间到120秒
  use: {
    baseURL: 'http://localhost:3000/resume/',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 30000, // 操作超时30秒
    navigationTimeout: 120000, // 导航超时120秒
  },

  webServer: {
    command: 'node node_modules/vite/bin/vite.js',
    url: 'http://localhost:3000/resume/',
    reuseExistingServer: !process.env.CI,
    timeout: 180000, // 服务器启动超时3分钟
  },

  projects: [
    // 桌面端测试
    {
      name: 'chromium-desktop',
      use: { ...devices['Desktop Chrome'] },
    },
    // iPhone 12 Pro 测试
    {
      name: 'mobile-iphone',
      use: {
        ...devices['iPhone 12 Pro'],
      },
    },
    // Pixel 5 测试
    {
      name: 'mobile-android',
      use: {
        ...devices['Pixel 5'],
      },
    },
    // iPad 测试
    {
      name: 'tablet-ipad',
      use: {
        ...devices['iPad Pro'],
      },
    },
  ],
});
