import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false, // 禁用并行运行以确保服务器稳定
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1, // 增加重试次数
  workers: 1, // 单个worker避免并发问题
  reporter: [['html', { outputFolder: 'playwright-report' }], ['line']],
  timeout: 120000, // 增加单个测试超时时间到120秒
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
    actionTimeout: 30000, // 操作超时30秒
    navigationTimeout: 120000, // 导航超时120秒
    // 模拟真人操作设置
    launchOptions: {
      slowMo: 50, // 轻微延迟模拟真人操作
    },
  },

  webServer: {
    command: 'npx vite preview --port 3000',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 180000, // 服务器启动超时3分钟
  },

  projects: [
    // 桌面端测试 - 主要测试目标
    {
      name: 'chromium-desktop',
      use: { 
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 },
      },
      grep: [/@desktop/, /@critical/],
    },
    // 移动端模拟测试
    {
      name: 'mobile-iphone',
      use: {
        ...devices['iPhone 12'],
      },
      grep: [/@mobile/, /@critical/],
    },
    // Android 设备模拟
    {
      name: 'mobile-android',
      use: {
        ...devices['Pixel 5'],
      },
      grep: [/@mobile/, /@critical/],
    },
  ],
});
