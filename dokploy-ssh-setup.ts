import { chromium, Browser, Page, BrowserContext } from 'playwright';

async function setupDokploySSH() {
  let browser: Browser | null = null;
  let context: BrowserContext | null = null;

  try {
    console.log('启动浏览器...');
    browser = await chromium.launch({
      headless: false,  // 显示浏览器窗口以便观察操作
      slowMo: 500      // 减慢操作速度便于观察
    });

    context = await browser.newContext({
      viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    console.log('访问 Dokploy 管理面板...');
    await page.goto('http://113.45.64.145:3000', {
      waitUntil: 'networkidle',
      timeout: 30000
    });

    // 等待页面加载
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'dokploy-1-landing.png' });

    console.log('查找登录表单...');

    // 尝试多种可能的登录表单选择器
    const emailSelectors = [
      'input[name="email"]',
      'input[type="email"]',
      'input[placeholder*="email"i]',
      '#email',
      '[data-testid="email-input"]'
    ];

    const passwordSelectors = [
      'input[name="password"]',
      'input[type="password"]',
      'input[placeholder*="password"i]',
      '#password',
      '[data-testid="password-input"]'
    ];

    const submitSelectors = [
      'button[type="submit"]',
      'button:has-text("登录")',
      'button:has-text("Login")',
      'button:has-text("Sign in")',
      'input[type="submit"]',
      '[data-testid="submit-button"]'
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

    // 查找提交按钮
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

    if (!emailInput || !passwordInput || !submitButton) {
      console.log('页面内容，用于调试:');
      const pageContent = await page.content();
      console.log('页面标题:', await page.title());

      // 尝试查找所有输入框
      const allInputs = await page.$$eval('input', inputs =>
        inputs.map(input => ({
          type: input.type,
          name: input.name,
          id: input.id,
          placeholder: input.placeholder
        }))
      );
      console.log('找到的输入框:', allInputs);

      // 尝试查找所有按钮
      const allButtons = await page.$$eval('button', buttons =>
        buttons.map(button => button.textContent)
      );
      console.log('找到的按钮:', allButtons);

      throw new Error('无法找到登录表单元素');
    }

    console.log('输入登录凭据...');
    await emailInput.fill('641600780@qq.com');
    await passwordInput.fill('353980swsgbo');

    await page.screenshot({ path: 'dokploy-2-before-login.png' });

    console.log('点击登录按钮...');
    await submitButton.click();

    // 等待登录完成
    console.log('等待登录完成...');
    await page.waitForLoadState('networkidle', { timeout: 30000 });
    await page.screenshot({ path: 'dokploy-3-after-login.png' });

    console.log('查找 Settings 链接...');
    // 根据页面结构，直接导航到 Settings 页面
    const settingsUrl = 'http://113.45.64.145:3000/dashboard/settings';
    console.log('直接导航到 Settings 页面...');
    await page.goto(settingsUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await page.screenshot({ path: 'dokploy-4-settings.png' });

    console.log('Settings 页面加载完成');
    console.log('查找 SSH Keys 页面...');
    const sshKeysSelectors = [
      'a:has-text("SSH Keys")',
      'a:has-text("SSH")',
      'button:has-text("SSH Keys")',
      '[data-testid="ssh-keys-link"]',
      'a[href*="ssh"]'
    ];

    let sshKeysLink = null;
    for (const selector of sshKeysSelectors) {
      try {
        await page.waitForSelector(selector, { timeout: 5000 });
        sshKeysLink = await page.$(selector);
        if (sshKeysLink) {
          console.log(`找到 SSH Keys 链接: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!sshKeysLink) {
      console.log('Settings 页面可用链接:');
      const allLinks = await page.$$eval('a', links =>
        links.map(link => link.textContent).filter(text => text?.trim())
      );
      console.log(allLinks);
      throw new Error('无法找到 SSH Keys 链接');
    }

    console.log('直接导航到 SSH Keys 页面...');
    const sshKeysUrl = 'http://113.45.64.145:3000/dashboard/settings/ssh-keys';
    await page.goto(sshKeysUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await page.screenshot({ path: 'dokploy-5-ssh-keys.png' });

    console.log('查找 Add SSH Key 按钮...');
    const addSSHButtonSelectors = [
      'button:has-text("Add SSH Key")',
      'button:has-text("添加SSH密钥")',
      'button:has-text("Add")',
      '[data-testid="add-ssh-key-button"]',
      'button[aria-label*="Add SSH"]'
    ];

    let addSSHButton = null;
    for (const selector of addSSHButtonSelectors) {
      try {
        await page.waitForSelector(selector, { timeout: 5000 });
        addSSHButton = await page.$(selector);
        if (addSSHButton) {
          console.log(`找到 Add SSH Key 按钮: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!addSSHButton) {
      console.log('SSH Keys 页面按钮:');
      const allButtons = await page.$$eval('button', buttons =>
        buttons.map(button => button.textContent)
      );
      console.log(allButtons);
      throw new Error('无法找到 Add SSH Key 按钮');
    }

    console.log('点击 Add SSH Key...');
    await addSSHButton.click();
    await page.waitForTimeout(1000); // 等待模态框出现
    await page.screenshot({ path: 'dokploy-6-add-ssh-modal.png' });

    console.log('输入SSH公钥...');
    const sshPublicKey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPhpLCnOdDAksakqgydJAqd3vL0rHvJ7I2N/SE6wHgu5 AI_Agent_Key';

    // 查找SSH密钥输入框
    const sshInputSelectors = [
      'textarea[name="sshKey"]',
      'textarea[name="publicKey"]',
      'textarea[placeholder*="SSH"i]',
      'textarea[placeholder*="ssh"i]',
      '[data-testid="ssh-key-input"]',
      'input[name="sshKey"]',
      'input[name="publicKey"]'
    ];

    let sshKeyInput = null;
    for (const selector of sshInputSelectors) {
      try {
        sshKeyInput = await page.$(selector);
        if (sshKeyInput) {
          console.log(`找到SSH密钥输入框: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!sshKeyInput) {
      throw new Error('无法找到SSH密钥输入框');
    }

    await sshKeyInput.fill(sshPublicKey);
    await page.screenshot({ path: 'dokploy-7-ssh-key-entered.png' });

    console.log('查找保存按钮...');
    const saveButtonSelectors = [
      'button:has-text("Save")',
      'button:has-text("保存")',
      'button:has-text("Confirm")',
      'button:has-text("确认")',
      'button[type="submit"]',
      '[data-testid="save-button"]'
    ];

    let saveButton = null;
    for (const selector of saveButtonSelectors) {
      try {
        saveButton = await page.$(selector);
        if (saveButton) {
          console.log(`找到保存按钮: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!saveButton) {
      throw new Error('无法找到保存按钮');
    }

    console.log('点击保存...');
    await saveButton.click();
    await page.waitForTimeout(2000); // 等待保存完成
    await page.screenshot({ path: 'dokploy-8-after-save.png' });

    console.log('✅ SSH密钥添加完成！');
    console.log('请检查最后一张截图确认密钥已成功添加');

    // 保持浏览器打开一段时间供用户检查
    console.log('浏览器将在10秒后关闭...');
    await page.waitForTimeout(10000);

  } catch (error) {
    console.error('❌ 操作失败:', error);

    // 保存错误时的截图
    if (context) {
      const pages = context.pages();
      if (pages.length > 0) {
        await pages[0].screenshot({ path: 'dokploy-error.png' });
        console.log('错误截图已保存为 dokploy-error.png');
      }
    }

    throw error;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 运行脚本
setupDokploySSH().catch(console.error);