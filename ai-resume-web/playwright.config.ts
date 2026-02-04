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
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 30000, // 操作超时30秒
    navigationTimeout: 120000, // 导航超时120秒
  },

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 180000, // 服务器启动超时3分钟
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
