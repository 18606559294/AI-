const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const screenshotDir = path.join(__dirname, 'dokploy-inspect');
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

function log(message) {
  console.log(`[${new Date().toISOString()}] ${message}`);
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const browser = await chromium.launch({
    headless: false,
    slowMo: 500
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    log('访问Dokploy面板');
    await page.goto('http://113.45.64.145:3000', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    await sleep(2000);

    log('填写登录信息');
    // 查找所有输入框
    const inputs = await page.locator('input').all();
    log(`找到 ${inputs.length} 个输入框`);

    for (let i = 0; i < inputs.length; i++) {
      const input = inputs[i];
      const type = await input.getAttribute('type');
      const placeholder = await input.getAttribute('placeholder');
      const name = await input.getAttribute('name');

      log(`输入框 ${i + 1}: type=${type}, placeholder=${placeholder}, name=${name}`);

      if (type === 'email' || placeholder?.toLowerCase().includes('email') || name?.toLowerCase().includes('email')) {
        await input.fill('641600780@qq.com');
        log('✓ 已填写邮箱');
      } else if (type === 'password' || name?.toLowerCase().includes('password')) {
        await input.fill('353980swsgbo');
        log('✓ 已填写密码');
      }
    }

    await page.screenshot({ path: path.join(screenshotDir, '01-form-filled.png') });

    log('查找并点击登录按钮');
    const buttons = await page.locator('button').all();
    log(`找到 ${buttons.length} 个按钮`);

    for (const button of buttons) {
      const text = await button.textContent();
      const type = await button.getAttribute('type');
      log(`按钮文本: "${text?.trim()}", type: ${type}`);

      if (text?.toLowerCase().includes('log') ||
          text?.toLowerCase().includes('sign') ||
          text?.includes('登录') ||
          type === 'submit') {
        await button.click();
        log('✓ 已点击登录按钮');
        break;
      }
    }

    await page.waitForLoadState('networkidle', { timeout: 30000 });
    await sleep(3000);

    await page.screenshot({ path: path.join(screenshotDir, '02-logged-in.png'), fullPage: true });

    // 获取页面HTML结构
    const pageHTML = await page.content();
    fs.writeFileSync(path.join(screenshotDir, 'page-structure.html'), pageHTML);
    log('✓ 页面HTML结构已保存');

    // 查找所有链接和可点击元素
    log('分析页面结构...');
    const links = await page.locator('a').all();
    log(`找到 ${links.length} 个链接`);

    const linkTexts = [];
    for (const link of links) {
      try {
        const text = await link.textContent();
        const href = await link.getAttribute('href');
        if (text && text.trim()) {
          linkTexts.push({ text: text.trim(), href });
        }
      } catch (e) {
        // 忽略错误
      }
    }

    // 保存链接信息
    fs.writeFileSync(
      path.join(screenshotDir, 'links.json'),
      JSON.stringify(linkTexts, null, 2)
    );
    log('✓ 链接信息已保存');

    // 查找包含"ai-resume"、"application"、"service"等关键词的元素
    const keywords = ['ai-resume', 'application', 'service', 'project', 'app', 'redis', 'backend', 'deploy'];
    const foundElements = [];

    for (const keyword of keywords) {
      try {
        const elements = await page.locator(`*:has-text("${keyword}")`).all();
        for (const element of elements) {
          try {
            const text = await element.textContent();
            if (text && text.toLowerCase().includes(keyword) && text.trim().length < 200) {
              const tagName = await element.evaluate(el => el.tagName);
              foundElements.push({ keyword, text: text.trim(), tagName });
            }
          } catch (e) {
            // 忽略错误
          }
        }
      } catch (e) {
        // 忽略错误
      }
    }

    // 保存找到的元素
    fs.writeFileSync(
      path.join(screenshotDir, 'found-elements.json'),
      JSON.stringify(foundElements, null, 2)
    );
    log(`✓ 找到 ${foundElements.length} 个相关元素`);

    // 尝试智能导航
    log('尝试智能导航...');
    const navigationTargets = [
      'ai-resume',
      'application',
      'applications',
      'apps',
      'projects',
      'services',
      'deployments'
    ];

    for (const target of navigationTargets) {
      try {
        log(`尝试查找: ${target}`);
        const element = await page.locator(`*:has-text("${target}")`).first();
        if (await element.isVisible({ timeout: 2000 })) {
          log(`✓ 找到可点击元素: ${target}`);
          await element.click();
          await page.waitForLoadState('networkidle');
          await sleep(2000);

          const screenshotName = `03-navigated-to-${target.replace(/\s+/g, '-')}.png`;
          await page.screenshot({ path: path.join(screenshotDir, screenshotName), fullPage: true });
          log(`✓ 已保存截图: ${screenshotName}`);

          // 如果找到了ai-resume相关内容，停止搜索
          if (target.toLowerCase().includes('ai-resume')) {
            log('✓ 已找到ai-resume相关页面，停止搜索');
            break;
          }

          // 返回上一页
          await page.goBack();
          await page.waitForLoadState('networkidle');
          await sleep(1000);
        }
      } catch (e) {
        log(`无法导航到 ${target}: ${e.message}`);
      }
    }

    // 最终状态
    await page.screenshot({ path: path.join(screenshotDir, '04-final-state.png'), fullPage: true });

    log('=== 检查完成 ===');
    log('浏览器将保持打开状态，您可以手动操作');
    log('按 Ctrl+C 退出');

    // 保持浏览器打开
    await new Promise(() => {});

  } catch (error) {
    log(`错误: ${error.message}`);
    console.error(error);
    await page.screenshot({ path: path.join(screenshotDir, 'error.png'), fullPage: true });
  }
}

main().catch(console.error);