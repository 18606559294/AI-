const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false, // 显示浏览器窗口以便调试
    slowMo: 1000 // 减慢操作以便观察
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    console.log('正在导航到Dokploy登录页面...');
    await page.goto('http://113.45.64.145:3000', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // 等待页面加载
    await page.waitForTimeout(2000);

    // 查找登录表单
    console.log('正在查找登录表单...');

    // 尝试不同的登录表单选择器
    const emailSelectors = [
      'input[name="email"]',
      'input[type="email"]',
      'input[placeholder*="email" i]',
      '#email',
      '[data-testid="email"]'
    ];

    const passwordSelectors = [
      'input[name="password"]',
      'input[type="password"]',
      '#password',
      '[data-testid="password"]'
    ];

    const submitSelectors = [
      'button[type="submit"]',
      'button:has-text("登录")',
      'button:has-text("Login")',
      'button:has-text("Sign")',
      '[data-testid="submit"]'
    ];

    let emailInput = null;
    let passwordInput = null;
    let submitButton = null;

    // 查找邮箱输入框
    for (const selector of emailSelectors) {
      try {
        emailInput = await page.$(selector);
        if (emailInput) {
          console.log(`找到邮箱输入框: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    // 查找密码输入框
    for (const selector of passwordSelectors) {
      try {
        passwordInput = await page.$(selector);
        if (passwordInput) {
          console.log(`找到密码输入框: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!emailInput || !passwordInput) {
      console.log('无法找到登录表单，截取当前页面...');
      await page.screenshot({ path: 'dokploy-login-page.png' });
      console.log('页面标题:', await page.title());
      console.log('页面URL:', page.url());

      // 尝试打印页面内容以便调试
      const pageContent = await page.content();
      console.log('页面HTML片段:', pageContent.substring(0, 500));
    } else {
      // 输入登录凭据
      console.log('正在输入登录凭据...');
      await emailInput.fill('641600780@qq.com');
      await passwordInput.fill('353980swsgbo');

      // 查找并点击提交按钮
      for (const selector of submitSelectors) {
        try {
          submitButton = await page.$(selector);
          if (submitButton) {
            console.log(`找到提交按钮: ${selector}`);
            break;
          }
        } catch (e) {
          continue;
        }
      }

      if (submitButton) {
        console.log('正在提交登录表单...');
        await submitButton.click();

        // 等待导航完成
        await page.waitForLoadState('networkidle', { timeout: 30000 });
        console.log('登录完成，当前URL:', page.url());
      } else {
        console.log('无法找到提交按钮');
      }
    }

    // 截取登录后的页面
    await page.screenshot({ path: 'dokploy-after-login.png' });
    console.log('已保存登录后截图: dokploy-after-login.png');

    // 等待一段时间让用户手动登录（如果自动登录失败）
    console.log('等待15秒以便手动登录（如果需要）...');
    await page.waitForTimeout(15000);

    // 查找"AI智能体简历"项目
    console.log('正在查找"AI智能体简历"项目...');

    const projectSelectors = [
      'text=AI智能体简历',
      'text=AI Agent Resume',
      '[data-project-name*="AI"]',
      'a:has-text("AI智能体简历")'
    ];

    let projectLink = null;
    for (const selector of projectSelectors) {
      try {
        projectLink = await page.$(selector);
        if (projectLink) {
          console.log(`找到项目链接: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (projectLink) {
      console.log('点击项目链接...');
      await projectLink.click();
      await page.waitForLoadState('networkidle', { timeout: 30000 });
    } else {
      console.log('无法找到项目链接，截取当前页面...');
      await page.screenshot({ path: 'dokploy-project-list.png' });
    }

    // 截取项目页面
    await page.screenshot({ path: 'dokploy-project-page.png' });

    // 查找Backend服务
    console.log('正在查找Backend服务...');

    const backendSelectors = [
      'text=Backend',
      'text=backend',
      '[data-service-name*="Backend"]',
      'a:has-text("Backend")',
      'div:has-text("Backend")'
    ];

    let backendLink = null;
    for (const selector of backendSelectors) {
      try {
        const elements = await page.$$(selector);
        if (elements.length > 0) {
          console.log(`找到${elements.length}个Backend相关元素: ${selector}`);
          backendLink = elements[0];
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (backendLink) {
      console.log('点击Backend服务...');
      await backendLink.click();
      await page.waitForLoadState('networkidle', { timeout: 30000 });
    }

    // 截取Backend服务页面
    await page.screenshot({ path: 'dokploy-backend-service.png' });

    // 查找日志相关按钮/标签
    console.log('正在查找日志功能...');

    const logsSelectors = [
      'text=Logs',
      'text=日志',
      'text=Console',
      'text=console',
      '[data-tab="logs"]',
      'button:has-text("Logs")',
      'button:has-text("日志")'
    ];

    let logsButton = null;
    for (const selector of logsSelectors) {
      try {
        const elements = await page.$$(selector);
        if (elements.length > 0) {
          console.log(`找到日志相关元素: ${selector}`);
          logsButton = elements[0];
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (logsButton) {
      console.log('点击日志按钮...');
      await logsButton.click();
      await page.waitForTimeout(3000); // 等待日志加载
    }

    // 截取日志页面
    await page.screenshot({ path: 'dokploy-backend-logs.png' });
    console.log('已保存日志截图: dokploy-backend-logs.png');

    // 尝试获取日志文本内容
    console.log('正在提取日志内容...');

    const logsContainerSelectors = [
      'pre',
      'code',
      '[data-logs]',
      '.logs',
      '.console',
      '#logs',
      '.log-output'
    ];

    for (const selector of logsContainerSelectors) {
      try {
        const logsElement = await page.$(selector);
        if (logsElement) {
          const logsText = await logsElement.textContent();
          if (logsText && logsText.trim().length > 0) {
            console.log('=== Backend服务日志内容 ===');
            console.log(logsText);

            // 保存日志到文件
            const fs = require('fs');
            fs.writeFileSync('backend-service-logs.txt', logsText);
            console.log('日志已保存到: backend-service-logs.txt');
            break;
          }
        }
      } catch (e) {
        continue;
      }
    }

    // 查找Terminal/Exec功能
    console.log('正在查找Terminal功能...');

    const terminalSelectors = [
      'text=Terminal',
      'text=Console',
      'text=Exec',
      'text=SSH',
      'button:has-text("Terminal")',
      '[data-terminal]'
    ];

    for (const selector of terminalSelectors) {
      try {
        const terminalElement = await page.$(selector);
        if (terminalElement) {
          console.log(`找到Terminal功能: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    // 查找环境变量部分
    console.log('正在查找环境变量配置...');

    const envSelectors = [
      'text=Environment',
      'text=环境变量',
      'text=Variables',
      '.env',
      '[data-env]'
    ];

    for (const selector of envSelectors) {
      try {
        const envElement = await page.$(selector);
        if (envElement) {
          console.log(`找到环境变量部分: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    console.log('日志获取完成，保持浏览器打开以便进一步检查...');
    console.log('按Ctrl+C退出脚本');

    // 保持浏览器打开
    await new Promise(() => {});

  } catch (error) {
    console.error('发生错误:', error);
    await page.screenshot({ path: 'dokploy-error.png' });
  } finally {
    // await browser.close();
  }
})();