const { chromium } = require('playwright');

async function triggerRedeploy() {
    const browser = await chromium.launch({
        headless: false,
        slowMo: 500
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🌐 正在访问Dokploy面板...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'domcontentloaded' });

        // 等待页面加载
        await page.waitForTimeout(3000);

        // 检查是否需要登录
        const loginNeeded = await page.locator('input[type="email"], input[type="text"]').count() > 0;
        if (loginNeeded) {
            console.log('📝 需要登录，正在输入凭据...');

            // 输入邮箱
            const emailInput = await page.locator('input[type="email"], input[type="text"]').first();
            await emailInput.fill('641600780@qq.com');
            await page.waitForTimeout(500);

            // 输入密码
            const passwordInput = await page.locator('input[type="password"]').first();
            await passwordInput.fill('353980swsgbo');
            await page.waitForTimeout(500);

            // 查找并点击登录按钮
            const loginButton = await page.locator('button').filter(async button => {
                const text = await button.textContent();
                return text && (text.includes('登录') || text.includes('Login') || text.includes('Sign In') || text.toLowerCase().includes('sign'));
            }).first();

            await loginButton.click();
            console.log('✅ 已点击登录按钮');

            // 等待登录完成
            await page.waitForTimeout(5000);
        } else {
            console.log('✅ 已经登录');
        }

        // 等待主界面完全加载
        await page.waitForLoadState('networkidle', { timeout: 10000 });
        await page.waitForTimeout(3000);

        console.log('🔍 正在查找AI智能体简历项目...');

        // 使用JavaScript来查找和点击项目
        const projectClicked = await page.evaluate(async () => {
            // 等待一小段时间确保DOM完全加载
            await new Promise(resolve => setTimeout(resolve, 1000));

            // 查找所有可能包含项目名称的元素
            const allElements = document.querySelectorAll('*');

            for (const element of allElements) {
                const text = element.textContent || '';
                const trimmedText = text.trim();

                // 查找包含"AI智能体简历"的元素
                if (trimmedText === 'AI智能体简历' ||
                    (trimmedText.includes('AI智能体简历') && trimmedText.length < 100)) {

                    // 尝试找到可点击的父元素
                    let clickableElement = element;

                    // 向上查找可点击的元素
                    while (clickableElement) {
                        const tagName = clickableElement.tagName.toLowerCase();
                        const hasClickHandler = clickableElement.onclick !== null;
                        const isClickable = tagName === 'a' || tagName === 'button' ||
                                          clickableElement.classList.contains('clickable') ||
                                          clickableElement.classList.contains('cursor-pointer') ||
                                          hasClickHandler;

                        if (isClickable) {
                            console.log('找到可点击元素:', clickableElement.tagName, clickableElement.className);
                            clickableElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            clickableElement.click();
                            return true;
                        }

                        clickableElement = clickableElement.parentElement;
                        if (clickableElement === document.body) break;
                    }
                }
            }

            return false;
        });

        if (projectClicked) {
            console.log('✅ 成功点击AI智能体简历项目');
        } else {
            // 如果JavaScript点击失败，尝试其他方法
            console.log('⚠️ JavaScript点击失败，尝试其他方法...');

            // 尝试直接查找并点击
            const projectCard = await page.locator('div').filter({ hasText: 'AI智能体简历' }).first();
            if (await projectCard.isVisible()) {
                await projectCard.click();
                console.log('✅ 通过locator点击成功');
            } else {
                throw new Error('无法找到或点击AI智能体简历项目');
            }
        }

        // 等待项目详情页加载
        console.log('⏳ 等待项目详情页加载...');
        await page.waitForTimeout(5000);

        // 截图项目详情页
        await page.screenshot({ path: 'dokploy-project-detail.png' });
        console.log('📸 已保存项目详情页截图');

        console.log('🔄 正在查找重新部署按钮...');

        // 查找并点击重新部署按钮
        const redeployClicked = await page.evaluate(async () => {
            await new Promise(resolve => setTimeout(resolve, 1000));

            const allButtons = document.querySelectorAll('button, [role="button"], .btn, [class*="button"]');

            for (const button of allButtons) {
                const text = (button.textContent || '').trim().toLowerCase();

                if (text.includes('redeploy') || text.includes('deploy') ||
                    text.includes('重新部署') || text.includes('部署')) {

                    console.log('找到部署按钮:', text);
                    button.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    button.click();
                    return true;
                }
            }

            return false;
        });

        if (!redeployClicked) {
            // 尝试使用Playwright locator
            const redeployButton = await page.locator('button').filter(async button => {
                const text = await button.textContent();
                return text && (text.toLowerCase().includes('redeploy') ||
                              text.toLowerCase().includes('deploy') ||
                              text.includes('重新部署') ||
                              text.includes('部署'));
            }).first();

            if (await redeployButton.isVisible({ timeout: 3000 })) {
                await redeployButton.click();
                console.log('✅ 通过locator点击重新部署按钮');
            } else {
                throw new Error('无法找到重新部署按钮');
            }
        } else {
            console.log('✅ 成功点击重新部署按钮');
        }

        // 等待确认对话框
        await page.waitForTimeout(2000);

        // 检查是否有确认对话框
        const hasConfirmDialog = await page.evaluate(async () => {
            const dialogs = document.querySelectorAll('[role="dialog"], .modal, .dialog, [class*="confirm"]');
            return dialogs.length > 0;
        });

        if (hasConfirmDialog) {
            console.log('⚠️ 检测到确认对话框，正在查找确认按钮...');

            const confirmClicked = await page.evaluate(async () => {
                const confirmButtons = document.querySelectorAll('button, [role="button"]');
                for (const button of confirmButtons) {
                    const text = (button.textContent || '').toLowerCase();
                    if (text.includes('confirm') || text.includes('yes') ||
                        text.includes('确认') || text.includes('是') || text.includes('继续')) {
                        console.log('找到确认按钮:', text);
                        button.click();
                        return true;
                    }
                }
                return false;
            });

            if (confirmClicked) {
                console.log('✅ 已点击确认按钮');
            }
        }

        console.log('🚀 重新部署已触发！');

        // 等待部署开始并监控进度
        console.log('⏳ 正在监控部署进度...');

        for (let i = 0; i < 12; i++) { // 监控2分钟
            await page.waitForTimeout(10000); // 每10秒检查一次

            // 获取部署状态
            const statusInfo = await page.evaluate(async () => {
                const statusElements = document.querySelectorAll('[class*="status"], [class*="deploy"], [class*="log"]');
                const results = [];

                statusElements.forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 0 && text.length < 500) {
                        results.push(text);
                    }
                });

                return results.slice(0, 5); // 返回前5个状态信息
            });

            console.log(`📊 部署状态 (${(i + 1) * 10}秒):`, statusInfo);

            // 定期截图
            if (i % 3 === 0) { // 每30秒截图一次
                await page.screenshot({ path: `dokploy-deploy-progress-${i + 1}.png` });
                console.log('📸 已保存部署进度截图');
            }
        }

        // 最终截图
        await page.screenshot({ path: 'dokploy-final-status.png' });
        console.log('📸 已保存最终状态截图');

        console.log('✅ 部署监控完成');
        console.log('🌐 请访问Dokploy面板查看详细状态: http://113.45.64.145:3000');

        // 保持浏览器打开以便手动检查
        console.log('⏰ 浏览器将保持打开30秒以便手动检查...');
        await page.waitForTimeout(30000);

    } catch (error) {
        console.error('❌ 发生错误:', error.message);
        console.error('错误堆栈:', error.stack);

        // 错误时截图
        await page.screenshot({ path: 'dokploy-error.png', fullPage: true });
        console.log('📸 已保存错误截图');

        throw error;
    } finally {
        await browser.close();
        console.log('👋 浏览器已关闭');
    }
}

// 运行自动化脚本
triggerRedeploy().catch(error => {
    console.error('脚本执行失败:', error);
    process.exit(1);
});