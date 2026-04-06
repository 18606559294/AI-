const { chromium } = require('playwright');

async function triggerRedeploy() {
    const browser = await chromium.launch({
        headless: false,  // 显示浏览器窗口以便观察
        slowMo: 1000     // 慢速操作以便观察
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🌐 正在访问Dokploy面板...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'networkidle' });

        // 等待页面加载
        await page.waitForTimeout(2000);

        // 检查是否需要登录
        const loginForm = await page.locator('input[type="email"], input[type="text"]').first();
        if (await loginForm.isVisible()) {
            console.log('📝 需要登录，正在输入凭据...');

            // 输入邮箱
            await page.locator('input[type="email"], input[type="text"]').first().fill('641600780@qq.com');
            await page.waitForTimeout(500);

            // 输入密码
            await page.locator('input[type="password"]').fill('353980swsgbo');
            await page.waitForTimeout(500);

            // 点击登录按钮
            const loginButton = await page.locator('button[type="submit"], button:has-text("登录"), button:has-text("Login"), button:has-text("Sign In")').first();
            await loginButton.click();
            console.log('✅ 已点击登录按钮');

            // 等待登录完成
            await page.waitForTimeout(3000);
        } else {
            console.log('✅ 已经登录');
        }

        // 等待主界面加载
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);

        console.log('🔍 正在查找AI智能体简历项目...');

        // 等待项目列表加载
        await page.waitForTimeout(2000);

        // 查找包含"AI智能体简历"的项目卡片
        const projectSelectors = [
            'div:has-text("AI智能体简历")',
            'text=AI智能体简历',
            '[class*="project"]:has-text("AI智能体简历")',
            'a:has-text("AI智能体简历")'
        ];

        let projectFound = false;
        for (const selector of projectSelectors) {
            try {
                console.log(`🔍 尝试选择器: ${selector}`);
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 3000 })) {
                    console.log(`✅ 找到项目: ${selector}`);
                    await element.click();
                    projectFound = true;
                    break;
                }
            } catch (e) {
                console.log(`⚠️ 选择器 ${selector} 未找到元素`);
                continue;
            }
        }

        if (!projectFound) {
            // 尝试查找所有包含文本的元素
            console.log('🔍 尝试查找所有包含"AI智能体简历"的元素...');
            const allElements = await page.locator('*').all();
            console.log(`📋 找到 ${allElements.length} 个元素，正在检查...`);

            for (let i = 0; i < Math.min(allElements.length, 1000); i++) {
                try {
                    const element = allElements[i];
                    const text = await element.textContent();
                    if (text && text.includes('AI智能体简历') && text.length < 200) {
                        console.log(`✅ 找到相关元素: ${text.substring(0, 100)}`);

                        // 尝试点击该元素或其父元素
                        try {
                            await element.click();
                            projectFound = true;
                            break;
                        } catch (clickError) {
                            // 如果无法直接点击，尝试点击父元素
                            const parent = await element.evaluateHandle(el => el.parentElement);
                            if (parent) {
                                await parent.asElement().click();
                                projectFound = true;
                                break;
                            }
                        }
                    }
                } catch (e) {
                    continue;
                }
            }
        }

        if (!projectFound) {
            console.log('❌ 未找到AI智能体简历项目，正在截图保存...');
            await page.screenshot({ path: 'dokploy-projects.png' });

            // 打印页面结构信息
            const pageContent = await page.content();
            console.log('📄 页面HTML片段:', pageContent.substring(0, 1000));

            throw new Error('无法找到AI智能体简历项目');
        }

        // 等待项目详情页加载
        await page.waitForTimeout(3000);

        console.log('🔄 正在查找重新部署按钮...');

        // 查找重新部署相关的按钮
        const redeploySelectors = [
            'button:has-text("Redeploy")',
            'button:has-text("重新部署")',
            'button:has-text("Deploy")',
            'button:has-text("部署")',
            '[data-testid="redeploy"]',
            '[data-testid="deploy"]',
            'button[class*="redeploy"]',
            'button[class*="deploy"]'
        ];

        let redeployButton = null;
        for (const selector of redeploySelectors) {
            try {
                const button = await page.locator(selector).first();
                if (await button.isVisible({ timeout: 2000 })) {
                    redeployButton = button;
                    console.log(`✅ 找到重新部署按钮: ${selector}`);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        if (!redeployButton) {
            // 查找所有按钮
            const allButtons = await page.locator('button').all();
            console.log(`🔍 找到 ${allButtons.length} 个按钮，正在检查...`);

            for (const button of allButtons) {
                const text = await button.textContent();
                if (text && (text.toLowerCase().includes('redeploy') ||
                           text.toLowerCase().includes('deploy') ||
                           text.includes('重新部署') ||
                           text.includes('部署'))) {
                    redeployButton = page.locator('button').filter({ hasText: text }).first();
                    console.log(`✅ 找到重新部署按钮: ${text.trim()}`);
                    break;
                }
            }
        }

        if (!redeployButton) {
            console.log('❌ 未找到重新部署按钮，正在截图保存...');
            await page.screenshot({ path: 'dokploy-project-detail.png' });
            throw new Error('无法找到重新部署按钮');
        }

        // 点击重新部署按钮
        console.log('🚀 正在点击重新部署按钮...');
        await redeployButton.click();
        await page.waitForTimeout(2000);

        // 检查是否有确认对话框
        const confirmButton = await page.locator('button:has-text("确认"), button:has-text("Confirm"), button:has-text("是"), button:has-text("Yes")').first();
        if (await confirmButton.isVisible({ timeout: 2000 })) {
            console.log('⚠️ 检测到确认对话框，正在确认...');
            await confirmButton.click();
            await page.waitForTimeout(2000);
        }

        console.log('✅ 重新部署已触发！');

        // 等待部署开始
        await page.waitForTimeout(5000);

        // 截图保存当前状态
        await page.screenshot({ path: 'dokploy-redeploy-started.png' });
        console.log('📸 已保存部署状态截图');

        // 等待一段时间观察部署进度
        console.log('⏳ 正在观察部署进度（30秒）...');
        await page.waitForTimeout(30000);

        // 再次截图
        await page.screenshot({ path: 'dokploy-deploy-progress.png' });
        console.log('📸 已保存部署进度截图');

        // 查找部署日志或状态信息
        console.log('📊 正在检查部署状态...');

        const statusSelectors = [
            '.status',
            '[data-testid="status"]',
            '.deployment-status',
            '.logs',
            '[data-testid="logs"]',
            'text=Status',
            'text=状态',
            'text=Logs',
            'text=日志'
        ];

        for (const selector of statusSelectors) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 2000 })) {
                    const text = await element.textContent();
                    console.log(`📋 部署状态信息: ${text.substring(0, 200)}`);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        console.log('✅ 部署触发完成，请手动监控部署进度');
        console.log('🌐 Dokploy面板: http://113.45.64.145:3000');

        // 保持浏览器打开一段时间以便观察
        await page.waitForTimeout(10000);

    } catch (error) {
        console.error('❌ 发生错误:', error.message);

        // 错误时截图
        await page.screenshot({ path: 'dokploy-error.png' });
        console.log('📸 已保存错误截图');

        throw error;
    } finally {
        // 关闭浏览器
        await browser.close();
        console.log('👋 浏览器已关闭');
    }
}

// 运行自动化脚本
triggerRedeploy().catch(console.error);