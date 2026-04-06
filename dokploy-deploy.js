const { chromium } = require('playwright');
const fs = require('fs');

async function deployToDokploy() {
    const browser = await chromium.launch({
        headless: false, // 设置为false可以看到浏览器操作
        slowMo: 1000 // 减慢操作速度便于观察
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🚀 开始Dokploy部署流程...');

        // 步骤1: 访问Dokploy登录页面
        console.log('📍 访问Dokploy管理面板...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'networkidle' });
        await page.screenshot({ path: 'dokploy-01-login-page.png' });

        // 等待页面加载
        await page.waitForTimeout(2000);

        // 步骤2: 登录
        console.log('🔐 登录到系统...');

        // 查找并填写邮箱
        const emailSelectors = [
            'input[name="email"]',
            'input[type="email"]',
            'input[placeholder*="邮箱"]',
            'input[placeholder*="email"]',
            '#email'
        ];

        let emailInput = null;
        for (const selector of emailSelectors) {
            try {
                emailInput = await page.$(selector);
                if (emailInput) {
                    console.log(`✅ 找到邮箱输入框: ${selector}`);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        if (!emailInput) {
            console.log('🔍 尝试查找页面上的输入框...');
            const inputs = await page.$$('input');
            console.log(`找到 ${inputs.length} 个输入框`);

            // 截图用于调试
            await page.screenshot({ path: 'dokploy-debug-inputs.png' });
        }

        // 查找并填写密码
        const passwordSelectors = [
            'input[name="password"]',
            'input[type="password"]',
            'input[placeholder*="密码"]',
            'input[placeholder*="password"]',
            '#password'
        ];

        // 查找登录按钮
        const loginButtonSelectors = [
            'button[type="submit"]',
            'button:has-text("登录")',
            'button:has-text("Login")',
            'button:has-text("Sign In")',
            'button:has-text("登入")',
            'button.btn-primary',
            'button.primary'
        ];

        console.log('📝 正在填写登录信息...');

        // 尝试填写表单
        if (emailInput) {
            await emailInput.fill('641600780@qq.com');
            console.log('✅ 邮箱已填写');
        }

        let passwordInput = null;
        for (const selector of passwordSelectors) {
            try {
                passwordInput = await page.$(selector);
                if (passwordInput) {
                    console.log(`✅ 找到密码输入框: ${selector}`);
                    await passwordInput.fill('353980swsgbo');
                    console.log('✅ 密码已填写');
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        await page.screenshot({ path: 'dokploy-02-form-filled.png' });

        // 点击登录按钮
        console.log('🖱️ 点击登录按钮...');
        let loginClicked = false;

        for (const selector of loginButtonSelectors) {
            try {
                const loginButton = await page.$(selector);
                if (loginButton) {
                    await loginButton.click();
                    console.log(`✅ 点击了登录按钮: ${selector}`);
                    loginClicked = true;
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        if (!loginClicked) {
            console.log('⚠️ 未找到登录按钮，尝试按Enter键...');
            await page.keyboard.press('Enter');
        }

        // 等待登录完成
        await page.waitForTimeout(3000);
        await page.screenshot({ path: 'dokploy-03-after-login.png' });

        // 步骤3: 查找ai-resume-platform应用
        console.log('🔍 查找ai-resume-platform应用...');

        // 等待页面加载
        await page.waitForLoadState('networkidle');

        // 尝试多种方式查找应用
        const appSelectors = [
            'a:has-text("ai-resume-platform")',
            'div:has-text("ai-resume-platform")',
            '[data-app="ai-resume-platform"]',
            '*:has-text("ai-resume")',
            '*:has-text("resume")'
        ];

        let appFound = false;
        for (const selector of appSelectors) {
            try {
                const appElement = await page.$(selector);
                if (appElement) {
                    console.log(`✅ 找到应用: ${selector}`);
                    await appElement.click();
                    appFound = true;
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        if (!appFound) {
            console.log('🔍 搜索应用列表...');
            const pageContent = await page.content();
            const hasResume = pageContent.includes('resume') || pageContent.includes('ai-resume');

            if (hasResume) {
                console.log('✅ 页面包含resume相关内容');
            } else {
                console.log('⚠️ 页面未找到resume相关内容');
            }

            await page.screenshot({ path: 'dokploy-04-app-search.png' });
        }

        // 等待应用页面加载
        await page.waitForTimeout(3000);
        await page.screenshot({ path: 'dokploy-05-app-page.png' });

        // 步骤4: 查找并点击部署按钮
        console.log('🚀 准备部署应用...');

        const deploySelectors = [
            'button:has-text("Deploy")',
            'button:has-text("部署")',
            'button:has-text("deploy")',
            'button[data-action="deploy"]',
            'button.btn-deploy',
            'a:has-text("Deploy")',
            'a:has-text("部署")'
        ];

        let deployButton = null;
        for (const selector of deploySelectors) {
            try {
                deployButton = await page.$(selector);
                if (deployButton && await deployButton.isVisible()) {
                    console.log(`✅ 找到部署按钮: ${selector}`);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        if (deployButton) {
            await deployButton.click();
            console.log('✅ 点击了部署按钮');
            await page.screenshot({ path: 'dokploy-06-deploy-started.png' });
        } else {
            console.log('⚠️ 未找到部署按钮，截图当前页面...');
            await page.screenshot({ path: 'dokploy-06-no-deploy-button.png' });
        }

        // 步骤5: 监控部署进度
        console.log('⏳ 监控部署进度...');

        // 等待部署开始
        await page.waitForTimeout(5000);

        // 持续监控部署状态
        const maxWaitTime = 600000; // 最多等待10分钟
        const startTime = Date.now();
        let deployCompleted = false;

        while (Date.now() - startTime < maxWaitTime && !deployCompleted) {
            await page.screenshot({ path: `dokploy-deploy-progress-${Date.now()}.png` });

            // 检查是否有完成状态
            const pageContent = await page.content();
            const hasSuccess = pageContent.includes('success') ||
                             pageContent.includes('完成') ||
                             pageContent.includes('deployed') ||
                             pageContent.includes('running');

            const hasError = pageContent.includes('error') ||
                           pageContent.includes('失败') ||
                           pageContent.includes('failed');

            if (hasSuccess && !hasError) {
                console.log('✅ 部署完成！');
                deployCompleted = true;
                break;
            }

            if (hasError) {
                console.log('❌ 部署出现错误');
                break;
            }

            console.log(`⏳ 部署中... (${Math.round((Date.now() - startTime) / 1000)}秒)`);
            await page.waitForTimeout(10000); // 每10秒检查一次
        }

        // 步骤6: 检查服务状态
        console.log('🔍 检查服务状态...');
        await page.screenshot({ path: 'dokploy-07-final-status.png' });

        // 查找服务状态信息
        const statusSelectors = [
            '.status',
            '[data-status]',
            '.service-status',
            '.health-status'
        ];

        const finalReport = {
            timestamp: new Date().toISOString(),
            success: deployCompleted,
            duration: Date.now() - startTime,
            services: {
                backend: { status: 'unknown', port: 8000 },
                frontend: { status: 'unknown', port: 3000 },
                redis: { status: 'unknown' }
            },
            screenshots: []
        };

        // 收集截图文件列表
        const screenshots = fs.readdirSync('.').filter(f => f.startsWith('dokploy-') && f.endsWith('.png'));
        finalReport.screenshots = screenshots;

        // 保存报告
        fs.writeFileSync('dokploy-deploy-report.json', JSON.stringify(finalReport, null, 2));
        console.log('📊 部署报告已保存到 dokploy-deploy-report.json');

        // 等待一段时间观察最终状态
        await page.waitForTimeout(5000);

    } catch (error) {
        console.error('❌ 部署过程中出现错误:', error);
        await page.screenshot({ path: 'dokploy-error.png' });
    } finally {
        console.log('🏁 完成部署流程，保持浏览器开启30秒...');
        await page.waitForTimeout(30000);
        await browser.close();
    }
}

// 运行部署流程
deployToDokploy().catch(console.error);