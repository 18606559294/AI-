const { chromium } = require('playwright');
const fs = require('fs');

// 配置信息
const DOKPLOY_URL = 'http://113.45.64.145:3000';
const EMAIL = '641600780@qq.com';
const PASSWORD = '353980swsgbo';

// 创建输出目录
const outputDir = '/tmp/dokploy-screenshots';
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function takeScreenshot(page, name) {
    const path = `${outputDir}/${name}.png`;
    await page.screenshot({ path, fullPage: true });
    console.log(`📸 截图保存: ${path}`);
    return path;
}

async function checkDokploy() {
    console.log('🚀 启动Dokploy面板检查...');

    // 启动浏览器
    const browser = await chromium.launch({
        headless: false,  // 显示浏览器窗口以便观察
        slowMo: 1000     // 放慢操作以便观察
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });

    const page = await context.newPage();

    try {
        // 步骤1: 访问Dokploy登录页面
        console.log('📍 步骤1: 访问Dokploy登录页面');
        await page.goto(DOKPLOY_URL);
        await sleep(3000);
        await takeScreenshot(page, '01-login-page');

        // 步骤2: 填写登录信息
        console.log('📍 步骤2: 填写登录信息');

        // 查找登录表单元素
        const emailInput = await page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]').first();
        const passwordInput = await page.locator('input[type="password"], input[name="password"]').first();
        const loginButton = await page.locator('button[type="submit"], button:has-text("登录") i, button:has-text("Login") i, button:has-text("Sign") i').first();

        if (await emailInput.isVisible()) {
            await emailInput.fill(EMAIL);
            console.log('✅ 邮箱已填写');
        } else {
            console.log('❌ 未找到邮箱输入框');
            await takeScreenshot(page, '02-email-input-not-found');
            throw new Error('未找到邮箱输入框');
        }

        if (await passwordInput.isVisible()) {
            await passwordInput.fill(PASSWORD);
            console.log('✅ 密码已填写');
        } else {
            console.log('❌ 未找到密码输入框');
            await takeScreenshot(page, '03-password-input-not-found');
            throw new Error('未找到密码输入框');
        }

        await takeScreenshot(page, '04-login-form-filled');

        // 步骤3: 点击登录按钮
        console.log('📍 步骤3: 点击登录按钮');
        await loginButton.click();
        await sleep(5000); // 等待登录处理
        await takeScreenshot(page, '05-after-login');

        // 步骤4: 查找AI智能体简历项目
        console.log('📍 步骤4: 查找AI智能体简历项目');

        // 尝试多种方式查找项目
        let projectFound = false;
        let projectElement = null;

        // 方法1: 通过文本查找
        const projectSelectors = [
            'text=AI智能体简历',
            'text=ai-resume',
            'text=AI简历',
            '[data-project-name*="ai"]',
            '[data-project-name*="resume"]',
            'a:has-text("AI")',
            'div:has-text("AI智能体简历")'
        ];

        for (const selector of projectSelectors) {
            try {
                projectElement = page.locator(selector).first();
                if (await projectElement.isVisible({ timeout: 2000 })) {
                    console.log(`✅ 找到项目，使用选择器: ${selector}`);
                    projectFound = true;
                    break;
                }
            } catch (e) {
                // 继续尝试下一个选择器
                continue;
            }
        }

        if (!projectFound) {
            // 方法2: 列出所有项目
            console.log('🔍 正在扫描页面上的所有项目...');
            const allProjects = await page.locator('a, div[class*="project"], div[class*="card"]').all();
            console.log(`找到 ${allProjects.length} 个可能的元素`);

            for (let i = 0; i < Math.min(allProjects.length, 20); i++) {
                try {
                    const text = await allProjects[i].textContent();
                    if (text && (text.includes('AI') || text.includes('简历') || text.includes('resume'))) {
                        console.log(`📌 可能的项目: ${text.trim()}`);
                        projectElement = allProjects[i];
                        projectFound = true;
                        break;
                    }
                } catch (e) {
                    continue;
                }
            }
        }

        await takeScreenshot(page, '06-project-list');

        if (projectFound && projectElement) {
            console.log('✅ 找到AI智能体简历项目');
            await projectElement.click();
            await sleep(3000);
            await takeScreenshot(page, '07-project-details');
        } else {
            console.log('❌ 未找到AI智能体简历项目');
            console.log('📋 页面当前内容:');
            const pageContent = await page.content();
            console.log(pageContent.substring(0, 1000));
            await takeScreenshot(page, '07-project-not-found');
            return;
        }

        // 步骤5: 检查现有服务
        console.log('📍 步骤5: 检查现有服务');

        const serviceSelectors = [
            'text=服务',
            'text=Services',
            '[data-service]',
            'div[class*="service"]',
            'div[class*="container"]'
        ];

        let servicesFound = false;
        const serviceInfo = [];

        for (const selector of serviceSelectors) {
            try {
                const services = page.locator(selector).all();
                const count = await (await services).length;
                if (count > 0) {
                    console.log(`✅ 找到 ${count} 个服务相关元素 (选择器: ${selector})`);

                    // 获取服务详情
                    for (let i = 0; i < Math.min(count, 10); i++) {
                        try {
                            const service = (await services)[i];
                            const text = await service.textContent();
                            if (text && text.trim().length > 0) {
                                serviceInfo.push({
                                    index: i,
                                    selector: selector,
                                    text: text.trim().substring(0, 200)
                                });
                            }
                        } catch (e) {
                            continue;
                        }
                    }

                    servicesFound = true;
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        console.log('📊 服务信息汇总:');
        serviceInfo.forEach(info => {
            console.log(`  - 服务 ${info.index}: ${info.text}`);
        });

        // 步骤6: 尝试查找添加服务按钮
        console.log('📍 步骤6: 查找添加服务或管理服务的选项');

        const actionButtons = [
            'button:has-text("添加")',
            'button:has-text("Add")',
            'button:has-text("新建")',
            'button:has-text("Create")',
            'button:has-text("部署")',
            'button:has-text("Deploy")',
            '[aria-label*="add"]',
            '[aria-label*="create"]'
        ];

        const availableActions = [];

        for (const selector of actionButtons) {
            try {
                const button = page.locator(selector).first();
                if (await button.isVisible({ timeout: 1000 })) {
                    const buttonText = await button.textContent();
                    availableActions.push({
                        selector: selector,
                        text: buttonText.trim()
                    });
                    console.log(`✅ 找到操作按钮: ${buttonText.trim()}`);
                }
            } catch (e) {
                continue;
            }
        }

        // 步骤7: 检查服务状态和配置
        console.log('📍 步骤7: 检查服务状态和配置');

        // 查找状态指示器
        const statusIndicators = [
            'text=运行中',
            'text=Running',
            'text=已停止',
            'text=Stopped',
            'text=在线',
            'text=Online',
            '[class*="status"]',
            '[class*="state"]'
        ];

        const serviceStatus = [];

        for (const selector of statusIndicators) {
            try {
                const status = page.locator(selector).all();
                const count = await (await status).length;
                if (count > 0) {
                    for (let i = 0; i < Math.min(count, 5); i++) {
                        try {
                            const statusText = await (await status)[i].textContent();
                            if (statusText && statusText.trim().length > 0) {
                                serviceStatus.push({
                                    selector: selector,
                                    text: statusText.trim()
                                });
                            }
                        } catch (e) {
                            continue;
                        }
                    }
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        console.log('📊 服务状态信息:');
        serviceStatus.forEach(status => {
            console.log(`  - ${status.text}`);
        });

        // 最终截图
        await takeScreenshot(page, '08-final-state');

        // 生成检查报告
        const report = {
            timestamp: new Date().toISOString(),
            dokployUrl: DOKPLOY_URL,
            loginSuccess: true,
            projectFound: projectFound,
            projectName: 'AI智能体简历',
            servicesFound: servicesFound,
            serviceCount: serviceInfo.length,
            services: serviceInfo,
            availableActions: availableActions,
            serviceStatus: serviceStatus,
            screenshots: fs.readdirSync(outputDir).map(file => `${outputDir}/${file}`)
        };

        const reportPath = '/home/hongfu/ai-resume/dokploy-check-report.json';
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        console.log(`📋 检查报告已保存: ${reportPath}`);

        // 保持浏览器打开一段时间以便观察
        console.log('⏳ 保持浏览器打开30秒以便观察...');
        await sleep(30000);

    } catch (error) {
        console.error('❌ 发生错误:', error.message);
        await takeScreenshot(page, 'error-screenshot');
        throw error;
    } finally {
        await browser.close();
        console.log('🏁 检查完成');
    }
}

// 运行检查
checkDokploy().catch(console.error);