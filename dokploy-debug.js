const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 创建screenshots目录
const screenshotDir = path.join(__dirname, 'dokploy-screenshots');
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

// 日志函数
function log(message) {
  console.log(`[${new Date().toISOString()}] ${message}`);
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const browser = await chromium.launch({
    headless: false, // 显示浏览器窗口以便观察
    slowMo: 1000 // 慢速操作以便观察
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    log('步骤1: 导航到Dokploy登录页面');
    await page.goto('http://113.45.64.145:3000', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // 截图：登录页面
    await page.screenshot({
      path: path.join(screenshotDir, '01-login-page.png'),
      fullPage: true
    });
    log('登录页面截图已保存');

    log('步骤2: 输入登录凭据');
    // 等待登录表单加载
    await page.waitForLoadState('networkidle');
    await sleep(2000);

    // 查找并填写邮箱
    const emailInput = await page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]').first();
    if (await emailInput.isVisible()) {
      await emailInput.fill('641600780@qq.com');
      log('邮箱已输入');
    } else {
      log('未找到邮箱输入框，尝试其他选择器');
      // 尝试其他可能的选择器
      const inputs = await page.locator('input').all();
      for (const input of inputs) {
        const placeholder = await input.getAttribute('placeholder');
        const type = await input.getAttribute('type');
        const name = await input.getAttribute('name');

        if (placeholder && placeholder.toLowerCase().includes('email') ||
            type === 'email' ||
            name && name.toLowerCase().includes('email')) {
          await input.fill('641600780@qq.com');
          log('邮箱已输入（使用备用选择器）');
          break;
        }
      }
    }

    await sleep(1000);

    // 查找并填写密码
    const passwordInput = await page.locator('input[type="password"], input[name="password"], input[placeholder*="password" i]').first();
    if (await passwordInput.isVisible()) {
      await passwordInput.fill('353980swsgbo');
      log('密码已输入');
    } else {
      log('未找到密码输入框，尝试其他选择器');
      const passwordInputs = await page.locator('input[type="password"]').all();
      if (passwordInputs.length > 0) {
        await passwordInputs[0].fill('353980swsgbo');
        log('密码已输入（使用备用选择器）');
      }
    }

    // 截图：表单已填写
    await page.screenshot({
      path: path.join(screenshotDir, '02-login-form-filled.png'),
      fullPage: true
    });

    log('步骤3: 点击登录按钮');
    const loginButton = await page.locator('button[type="submit"], button:has-text("登录"), button:has-text("Log in"), button:has-text("Sign in"), button:has-text("登入")').first();

    if (await loginButton.isVisible()) {
      await loginButton.click();
      log('登录按钮已点击');
    } else {
      log('尝试按回车键登录');
      await page.keyboard.press('Enter');
    }

    // 等待导航完成
    await page.waitForLoadState('networkidle', { timeout: 30000 });
    await sleep(3000);

    // 截图：登录后的页面
    await page.screenshot({
      path: path.join(screenshotDir, '03-after-login.png'),
      fullPage: true
    });
    log('登录后页面截图已保存');

    log('步骤4: 查找ai-resume-platform应用');
    // 尝试多种方式查找应用
    const appSelectors = [
      'text=ai-resume-platform',
      '[data-app-name="ai-resume-platform"]',
      'a:has-text("ai-resume")',
      'div:has-text("ai-resume-platform")',
      '*:text("ai-resume-platform")'
    ];

    let appFound = false;
    for (const selector of appSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible({ timeout: 5000 })) {
          log(`找到应用: ${selector}`);
          await element.click();
          appFound = true;
          break;
        }
      } catch (e) {
        // 继续尝试下一个选择器
      }
    }

    if (!appFound) {
      log('未找到ai-resume-platform应用，尝试导航到可能的应用列表页');
      // 尝试查找"Applications"、"Apps"或"项目"等链接
      const navSelectors = [
        'text=Applications',
        'text=Apps',
        'text=项目',
        'text=Applications',
        'a:has-text("Application")',
        'nav a:has-text("App")'
      ];

      for (const selector of navSelectors) {
        try {
          const navElement = await page.locator(selector).first();
          if (await navElement.isVisible({ timeout: 3000 })) {
            log(`点击导航: ${selector}`);
            await navElement.click();
            await page.waitForLoadState('networkidle');
            await sleep(2000);
            break;
          }
        } catch (e) {
          // 继续
        }
      }
    }

    // 截图：应用页面
    await page.screenshot({
      path: path.join(screenshotDir, '04-app-page.png'),
      fullPage: true
    });
    log('应用页面截图已保存');

    log('步骤5: 查找并检查服务列表');
    // 查找服务/容器列表
    await sleep(2000);

    // 尝试找到服务列表或容器列表
    const serviceSelectors = [
      'text=Services',
      'text=Containers',
      'text=服务',
      'text=Deployments',
      '[data-testid="service-list"]',
      '.service-list',
      '.container-list'
    ];

    // 获取页面文本内容以了解结构
    const pageContent = await page.textContent('body');
    log('页面内容片段: ' + pageContent.substring(0, 500));

    // 查找所有可能的服务卡片或行
    log('查找服务元素...');

    // 尝试找到包含"redis"、"backend"等关键词的元素
    const keywords = ['redis', 'backend', 'frontend', 'postgres', 'database'];
    const foundServices = [];

    for (const keyword of keywords) {
      try {
        const elements = await page.locator(`*:has-text("${keyword}")`).all();
        for (const element of elements) {
          const text = await element.textContent();
          if (text && text.toLowerCase().includes(keyword)) {
            foundServices.push({ keyword, element, text: text.trim() });
          }
        }
      } catch (e) {
        // 继续
      }
    }

    log(`找到包含关键词的元素: ${foundServices.length}个`);

    // 检查每个服务
    for (const service of foundServices) {
      log(`处理服务: ${service.keyword}`);
      try {
        // 点击服务
        await service.element.click();
        await page.waitForLoadState('networkidle');
        await sleep(2000);

        // 截图：服务详情页
        const serviceName = service.keyword.replace(/[^a-z0-9]/gi, '_');
        await page.screenshot({
          path: path.join(screenshotDir, `05-service-${serviceName}-details.png`),
          fullPage: true
        });

        // 查找Logs标签或按钮
        const logsSelectors = [
          'text=Logs',
          'text=日志',
          'button:has-text("Logs")',
          'tab:has-text("Logs")',
          '[data-testid="logs-tab"]',
          'a:has-text("Logs")'
        ];

        let logsClicked = false;
        for (const selector of logsSelectors) {
          try {
            const logsButton = await page.locator(selector).first();
            if (await logsButton.isVisible({ timeout: 3000 })) {
              log(`点击Logs标签: ${selector}`);
              await logsButton.click();
              await page.waitForLoadState('networkidle');
              await sleep(3000); // 等待日志加载
              logsClicked = true;

              // 截图：日志页面
              await page.screenshot({
                path: path.join(screenshotDir, `06-service-${serviceName}-logs.png`),
                fullPage: true
              });

              // 尝试获取日志文本内容
              try {
                const logsContent = await page.textContent('body');
                const logsPath = path.join(screenshotDir, `service-${serviceName}-logs.txt`);
                fs.writeFileSync(logsPath, logsContent);
                log(`日志内容已保存到: ${logsPath}`);
              } catch (e) {
                log('无法保存日志文本内容');
              }

              break;
            }
          } catch (e) {
            // 继续尝试下一个选择器
          }
        }

        if (!logsClicked) {
          log('未找到Logs标签，可能已在详情页显示');
        }

        // 查找终端或控制台
        const terminalSelectors = [
          'text=Terminal',
          'text=Console',
          'text=终端',
          'button:has-text("Terminal")',
          'button:has-text("Console")'
        ];

        for (const selector of terminalSelectors) {
          try {
            const terminalButton = await page.locator(selector).first();
            if (await terminalButton.isVisible({ timeout: 3000 })) {
              log(`点击终端标签: ${selector}`);
              await terminalButton.click();
              await page.waitForLoadState('networkidle');
              await sleep(2000);

              // 截图：终端页面
              await page.screenshot({
                path: path.join(screenshotDir, `07-service-${serviceName}-terminal.png`),
                fullPage: true
              });
              break;
            }
          } catch (e) {
            // 继续
          }
        }

        // 尝试查找重启按钮
        const restartSelectors = [
          'button:has-text("重启")',
          'button:has-text("Restart")',
          'button:has-text("Redeploy")',
          'button:has-text("重新部署")',
          '[data-testid="restart-button"]',
          'button[aria-label*="restart"]'
        ];

        for (const selector of restartSelectors) {
          try {
            const restartButton = await page.locator(selector).first();
            if (await restartButton.isVisible({ timeout: 3000 })) {
              log(`找到重启按钮: ${selector}`);
              // 只记录，不实际点击，避免意外操作
              log(`服务 ${service.keyword} 有重启选项可用`);
              break;
            }
          } catch (e) {
            // 继续
          }
        }

        // 返回服务列表页
        const backSelectors = [
          'button[aria-label="back"]',
          'text=Back',
          'text=返回',
          'a:has-text("Back")'
        ];

        for (const selector of backSelectors) {
          try {
            const backButton = await page.locator(selector).first();
            if (await backButton.isVisible({ timeout: 3000 })) {
              await backButton.click();
              await page.waitForLoadState('networkidle');
              await sleep(1000);
              break;
            }
          } catch (e) {
            // 继续
          }
        }

      } catch (e) {
        log(`处理服务 ${service.keyword} 时出错: ${e.message}`);
      }
    }

    // 最终截图
    await page.screenshot({
      path: path.join(screenshotDir, '08-final-state.png'),
      fullPage: true
    });

    log('流程完成，保持浏览器打开以便手动检查...');
    log(`所有截图已保存到: ${screenshotDir}`);

    // 保持浏览器打开，让用户可以手动操作
    log('按Ctrl+C退出浏览器...');

  } catch (error) {
    log(`发生错误: ${error.message}`);
    await page.screenshot({
      path: path.join(screenshotDir, 'error-screenshot.png'),
      fullPage: true
    });
  }

  // 等待用户手动关闭
  await new Promise(() => {}); // 无限等待
}

main().catch(console.error);