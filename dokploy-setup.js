const { chromium } = require('playwright');
const fs = require('fs');

// 配置信息
const CONFIG = {
  url: 'http://113.45.64.145:3000',
  email: '641600780@qq.com',
  password: '353980swsgbo',
  project: {
    name: 'ai-resume-platform',
    description: 'AI Resume Platform - 智能简历生成系统'
  },
  application: {
    name: 'ai-resume-platform',
    gitRepo: 'git@github.com:18606559294/AI-.git',
    branch: 'main',
    composeFile: 'docker-compose.prod.yml'
  }
};

// 日志函数
function log(message, level = 'info') {
  const timestamp = new Date().toISOString();
  const prefix = {
    'info': '📋',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'step': '🎯'
  }[level] || '📋';

  console.log(`[${timestamp}] ${prefix} ${message}`);
}

// 截图函数
async function takeScreenshot(page, name) {
  const screenshotPath = `/tmp/dokploy-setup-${name}-${Date.now()}.png`;
  await page.screenshot({ path: screenshotPath, fullPage: true });
  log(`截图已保存: ${screenshotPath}`, 'info');
  return screenshotPath;
}

// 主函数
async function setupDokploy() {
  let browser;
  let context;
  let page;

  try {
    log('开始Dokploy配置流程...', 'step');

    // 启动浏览器
    log('正在启动浏览器...', 'info');
    browser = await chromium.launch({
      headless: false,  // 显示浏览器窗口以便调试
      slowMo: 500      // 减慢操作速度以便观察
    });

    context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      recordVideo: {
        dir: '/tmp/dokploy-videos',
        size: { width: 1920, height: 1080 }
      }
    });

    page = await context.newPage();

    // 步骤1: 访问登录页面
    log('步骤1: 访问Dokploy登录页面', 'step');
    await page.goto(CONFIG.url, { waitUntil: 'networkidle' });
    await takeScreenshot(page, '01-login-page');
    log('页面加载完成', 'success');

    // 等待页面加载
    await page.waitForTimeout(2000);

    // 步骤2: 填写登录信息
    log('步骤2: 填写登录信息', 'step');

    // 查找邮箱输入框
    const emailInput = await page.locator('input[type="email"], input[name="email"], input[placeholder*="邮箱"], input[placeholder*="email"], input[placeholder*="Email"]').first();
    if (await emailInput.isVisible()) {
      await emailInput.fill(CONFIG.email);
      log('邮箱已填写', 'success');
    } else {
      log('未找到邮箱输入框，尝试其他方式', 'warning');
    }

    // 查找密码输入框
    const passwordInput = await page.locator('input[type="password"], input[name="password"], input[placeholder*="密码"], input[placeholder*="password"], input[placeholder*="Password"]').first();
    if (await passwordInput.isVisible()) {
      await passwordInput.fill(CONFIG.password);
      log('密码已填写', 'success');
    } else {
      log('未找到密码输入框', 'warning');
    }

    await takeScreenshot(page, '02-login-filled');

    // 查找并点击登录按钮
    const loginButton = await page.locator('button[type="submit"], button:has-text("登录"), button:has-text("Login"), button:has-text("Sign In"), button:has-text("登入")').first();
    if (await loginButton.isVisible()) {
      await loginButton.click();
      log('登录按钮已点击', 'success');
    } else {
      log('未找到登录按钮', 'error');
    }

    // 等待登录完成
    await page.waitForTimeout(3000);
    await takeScreenshot(page, '03-after-login');

    // 步骤3: 导航到项目页面
    log('步骤3: 查找项目创建入口', 'step');

    // 尝试查找"Create Project"按钮或项目相关链接
    const createProjectSelectors = [
      'a:has-text("Create Project")',
      'a:has-text("新建项目")',
      'a:has-text("创建项目")',
      'button:has-text("Create Project")',
      'button:has-text("新建项目")',
      'button:has-text("创建项目")',
      '[href*="project"]',
      '[href*="projects"]'
    ];

    let projectLinkFound = false;
    for (const selector of createProjectSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible({ timeout: 1000 })) {
          log(`找到项目链接: ${selector}`, 'success');
          await element.click();
          projectLinkFound = true;
          break;
        }
      } catch (e) {
        // 继续尝试下一个选择器
      }
    }

    if (!projectLinkFound) {
      log('未找到项目创建链接，分析页面结构...', 'warning');
      const pageContent = await page.content();
      log(`页面URL: ${page.url()}`, 'info');

      // 查找所有按钮和链接
      const buttons = await page.locator('button, a').allTextContents();
      log(`页面上的按钮和链接: ${buttons.slice(0, 20).join(', ')}`, 'info');
    }

    await page.waitForTimeout(2000);
    await takeScreenshot(page, '04-projects-page');

    // 步骤4: 创建项目
    log('步骤4: 创建项目', 'step');

    // 查找项目名称输入框
    const projectNameInput = await page.locator('input[name="name"], input[placeholder*="项目名称"], input[placeholder*="project name"], input[placeholder*="Project Name"]').first();
    if (await projectNameInput.isVisible({ timeout: 2000 })) {
      await projectNameInput.fill(CONFIG.project.name);
      log(`项目名称已填写: ${CONFIG.project.name}`, 'success');
    }

    // 查找项目描述输入框
    const projectDescInput = await page.locator('textarea[name="description"], input[name="description"], input[placeholder*="描述"], input[placeholder*="description"]').first();
    if (await projectDescInput.isVisible({ timeout: 2000 })) {
      await projectDescInput.fill(CONFIG.project.description);
      log(`项目描述已填写: ${CONFIG.project.description}`, 'success');
    }

    await takeScreenshot(page, '05-project-form-filled');

    // 查找并点击创建按钮
    const createButtonSelectors = [
      'button[type="submit"]',
      'button:has-text("创建")',
      'button:has-text("Create")',
      'button:has-text("确认")',
      'button:has-text("Confirm")'
    ];

    for (const selector of createButtonSelectors) {
      try {
        const createButton = await page.locator(selector).first();
        if (await createButton.isVisible({ timeout: 1000 })) {
          await createButton.click();
          log('项目创建按钮已点击', 'success');
          break;
        }
      } catch (e) {
        // 继续尝试
      }
    }

    await page.waitForTimeout(3000);
    await takeScreenshot(page, '06-project-created');

    // 步骤5: 创建应用
    log('步骤5: 创建应用', 'step');

    // 查找应用创建按钮
    const createAppSelectors = [
      'button:has-text("Create Application")',
      'button:has-text("新建应用")',
      'button:has-text("创建应用")',
      'button:has-text("New App")',
      'button:has-text("Add App")',
      'a:has-text("Create Application")'
    ];

    for (const selector of createAppSelectors) {
      try {
        const createAppButton = await page.locator(selector).first();
        if (await createAppButton.isVisible({ timeout: 1000 })) {
          await createAppButton.click();
          log('应用创建按钮已点击', 'success');
          break;
        }
      } catch (e) {
        // 继续尝试
      }
    }

    await page.waitForTimeout(2000);
    await takeScreenshot(page, '07-app-creation-page');

    // 步骤6: 配置Docker Compose应用
    log('步骤6: 配置Docker Compose应用', 'step');

    // 选择应用类型为Docker Compose
    const composeSelectors = [
      'button:has-text("Docker Compose")',
      'label:has-text("Docker Compose")',
      'input[value="docker-compose"]',
      'input[value="compose"]',
      '[data-type="docker-compose"]'
    ];

    for (const selector of composeSelectors) {
      try {
        const composeOption = await page.locator(selector).first();
        if (await composeOption.isVisible({ timeout: 1000 })) {
          await composeOption.click();
          log('已选择Docker Compose类型', 'success');
          break;
        }
      } catch (e) {
        // 继续尝试
      }
    }

    await takeScreenshot(page, '08-compose-type-selected');

    // 填写应用配置
    const appNameInput = await page.locator('input[name="appName"], input[name="application_name"], input[placeholder*="应用名称"]').first();
    if (await appNameInput.isVisible({ timeout: 2000 })) {
      await appNameInput.fill(CONFIG.application.name);
      log(`应用名称已填写: ${CONFIG.application.name}`, 'success');
    }

    const gitRepoInput = await page.locator('input[name="gitRepo"], input[name="repository"], input[placeholder*="Git"], input[placeholder*="github"]').first();
    if (await gitRepoInput.isVisible({ timeout: 2000 })) {
      await gitRepoInput.fill(CONFIG.application.gitRepo);
      log(`Git仓库已填写: ${CONFIG.application.gitRepo}`, 'success');
    }

    const branchInput = await page.locator('input[name="branch"], input[placeholder*="分支"], input[placeholder*="branch"]').first();
    if (await branchInput.isVisible({ timeout: 2000 })) {
      await branchInput.fill(CONFIG.application.branch);
      log(`分支已填写: ${CONFIG.application.branch}`, 'success');
    }

    const composeFileInput = await page.locator('input[name="composeFile"], input[placeholder*="docker-compose"], input[placeholder*="compose"]').first();
    if (await composeFileInput.isVisible({ timeout: 2000 })) {
      await composeFileInput.fill(CONFIG.application.composeFile);
      log(`Docker Compose文件已填写: ${CONFIG.application.composeFile}`, 'success');
    }

    await takeScreenshot(page, '09-app-config-filled');

    // 查找并点击启用自动部署的复选框
    const autoDeployCheckbox = await page.locator('input[type="checkbox"][name*="auto"], input[type="checkbox"][name*="deploy"]').first();
    if (await autoDeployCheckbox.isVisible({ timeout: 2000 })) {
      if (!(await autoDeployCheckbox.isChecked())) {
        await autoDeployCheckbox.check();
        log('已启用自动部署', 'success');
      }
    }

    await takeScreenshot(page, '10-final-config');

    // 查找并点击最终创建按钮
    for (const selector of createButtonSelectors) {
      try {
        const finalCreateButton = await page.locator(selector).first();
        if (await finalCreateButton.isVisible({ timeout: 1000 })) {
          await finalCreateButton.click();
          log('应用创建按钮已点击', 'success');
          break;
        }
      } catch (e) {
        // 继续尝试
      }
    }

    // 等待应用创建完成
    await page.waitForTimeout(5000);
    await takeScreenshot(page, '11-app-created');

    log('Dokploy配置流程完成！', 'success');

  } catch (error) {
    log(`配置过程中发生错误: ${error.message}`, 'error');
    if (page) {
      await takeScreenshot(page, 'error-screenshot');
    }
    throw error;

  } finally {
    // 关闭浏览器
    if (context) {
      const videoPath = await context.video?.path();
      if (videoPath) {
        log(`视频录制已保存: ${videoPath}`, 'success');
      }
    }

    if (browser) {
      await browser.close();
    }
  }
}

// 执行主函数
if (require.main === module) {
  setupDokploy()
    .then(() => {
      log('脚本执行完成', 'success');
      process.exit(0);
    })
    .catch((error) => {
      log(`脚本执行失败: ${error.message}`, 'error');
      console.error(error);
      process.exit(1);
    });
}

module.exports = { setupDokploy };