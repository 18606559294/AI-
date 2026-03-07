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
    command: 'npx vite preview --port 3000',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 180000, // 服务器启动超时3分钟
  },

  projects: [
    // 桌面端测试
    {
      name: 'chromium-desktop',
      use: { ...devices['Desktop Chrome'] },
    },
    // iPhone 12 Pro 测试 (using chromium for mobile simulation)
    {
      name: 'mobile-iphone',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 390, height: 844 },
        deviceScaleFactor: 3,
        isMobile: true,
        hasTouch: true,
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
      },
    },
    // Pixel 5 测试 (using chromium for mobile simulation)
    {
      name: 'mobile-android',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 393, height: 851 },
        deviceScaleFactor: 2.625,
        isMobile: true,
        hasTouch: true,
        userAgent: 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36',
      },
    },
    // iPad 测试 (using chromium for tablet simulation)
    {
      name: 'tablet-ipad',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1024, height: 1366 },
        deviceScaleFactor: 2,
        isMobile: true,
        hasTouch: true,
        userAgent: 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
      },
    },
  ],
});
