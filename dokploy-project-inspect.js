const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const screenshotDir = path.join(__dirname, 'dokploy-project-inspect');
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
    slowMo: 800
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    // 登录
    log('登录到Dokploy');
    await page.goto('http://113.45.64.145:3000', { waitUntil: 'networkidle' });
    await sleep(2000);

    const inputs = await page.locator('input').all();
    for (const input of inputs) {
      const type = await input.getAttribute('type');
      const placeholder = await input.getAttribute('placeholder');
      const name = await input.getAttribute('name');

      if (type === 'email' || placeholder?.toLowerCase().includes('email') || name?.toLowerCase().includes('email')) {
        await input.fill('641600780@qq.com');
      } else if (type === 'password' || name?.toLowerCase().includes('password')) {
        await input.fill('353980swsgbo');
      }
    }

    const buttons = await page.locator('button').all();
    for (const button of buttons) {
      const text = await button.textContent();
      if (text?.toLowerCase().includes('log') || text?.toLowerCase().includes('sign') || text?.includes('登录')) {
        await button.click();
        break;
      }
    }

    await page.waitForLoadState('networkidle');
    await sleep(3000);

    // 导航到项目页面
    log('导航到项目页面');
    await page.goto('http://113.45.64.145:3000/dashboard/projects', { waitUntil: 'networkidle' });
    await sleep(2000);

    await page.screenshot({ path: path.join(screenshotDir, '01-projects-page.png'), fullPage: true });

    // 检查ai-resume-platform项目
    log('点击ai-resume-platform项目');
    const aiResumeLink = page.locator('a:has-text("ai-resume-platform")').first();
    if (await aiResumeLink.isVisible()) {
      await aiResumeLink.click();
      await page.waitForLoadState('networkidle');
      await sleep(2000);

      await page.screenshot({ path: path.join(screenshotDir, '02-ai-resume-platform-project.png'), fullPage: true });

      // 获取页面内容
      const projectContent = await page.textContent('body');
      fs.writeFileSync(
        path.join(screenshotDir, 'ai-resume-project-content.txt'),
        projectContent
      );

      // 查找服务、部署、应用等相关信息
      log('查找服务相关信息...');
      const serviceKeywords = ['service', 'application', 'deployment', 'container', 'compose', 'stack'];
      const foundInfo = [];

      for (const keyword of serviceKeywords) {
        try {
          const elements = await page.locator(`*:has-text("${keyword}")`).all();
          for (const element of elements) {
            try {
              const text = await element.textContent();
              if (text && text.toLowerCase().includes(keyword) && text.trim().length < 300) {
                const tagName = await element.evaluate(el => el.tagName);
                const className = await element.evaluate(el => el.className);
                foundInfo.push({ keyword, text: text.trim(), tagName, className });
              }
            } catch (e) {
              // 忽略
            }
          }
        } catch (e) {
          // 忽略
        }
      }

      fs.writeFileSync(
        path.join(screenshotDir, 'ai-resume-project-info.json'),
        JSON.stringify(foundInfo, null, 2)
      );

      // 查找创建服务/应用的按钮
      log('查找创建服务的选项...');
      const createButtonSelectors = [
        'button:has-text("Create")',
        'button:has-text("New")',
        'button:has-text("Add")',
        'button:has-text("创建")',
        'button:has-text("新建")',
        'button:has-text("添加")',
        'a:has-text("Create")',
        'a:has-text("New")',
        '*:has-text("Create Service")',
        '*:has-text("New Application")',
        '*:has-text("Add Service")'
      ];

      for (const selector of createButtonSelectors) {
        try {
          const button = page.locator(selector).first();
          if (await button.isVisible({ timeout: 2000 })) {
            const buttonText = await button.textContent();
            log(`找到创建按钮: "${buttonText?.trim()}" - ${selector}`);
          }
        } catch (e) {
          // 忽略
        }
      }

      // 查找标签页或导航选项
      log('查找页面标签...');
      const tabs = await page.locator('[role="tab"], .tab, [class*="tab"]').all();
      log(`找到 ${tabs.length} 个可能的标签`);

      for (let i = 0; i < Math.min(tabs.length, 10); i++) {
        try {
          const tabText = await tabs[i].textContent();
          log(`标签 ${i + 1}: "${tabText?.trim()}"`);
        } catch (e) {
          // 忽略
        }
      }

      // 检查旧项目
      log('返回项目列表检查旧项目');
      await page.goto('http://113.45.64.145:3000/dashboard/projects', { waitUntil: 'networkidle' });
      await sleep(2000);

      const oldProjectLink = page.locator('a:has-text("AI智能体简历")').first();
      if (await oldProjectLink.isVisible()) {
        await oldProjectLink.click();
        await page.waitForLoadState('networkidle');
        await sleep(2000);

        await page.screenshot({ path: path.join(screenshotDir, '03-old-project.png'), fullPage: true });

        // 查找服务信息
        log('检查旧项目的服务...');
        const serviceElements = await page.locator('*:has-text("service")').all();
        log(`旧项目找到 ${serviceElements.length} 个包含'service'的元素`);

        // 查找具体的服务
        const serviceNames = [];
        for (const element of serviceElements) {
          try {
            const text = await element.textContent();
            if (text && text.trim().length < 100 && text.trim()) {
              serviceNames.push(text.trim());
            }
          } catch (e) {
            // 忽略
          }
        }

        fs.writeFileSync(
          path.join(screenshotDir, 'old-project-services.json'),
          JSON.stringify(serviceNames, null, 2)
        );
      }

    }

    log('=== 检查完成 ===');
    log('浏览器保持打开，您可以手动操作');
    log(`结果保存在: ${screenshotDir}`);

    // 保持浏览器打开
    await new Promise(() => {});

  } catch (error) {
    log(`错误: ${error.message}`);
    console.error(error);
    await page.screenshot({ path: path.join(screenshotDir, 'error.png'), fullPage: true });
  }
}

main().catch(console.error);