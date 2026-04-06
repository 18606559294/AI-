const { chromium } = require('playwright');

async function triggerRedeploy() {
    const browser = await chromium.launch({
        headless: false,
        slowMo: 200
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🌐 正在访问Dokploy面板...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);

        // 检查登录状态
        const loginNeeded = await page.locator('input[type="email"], input[type="text"]').count() > 0;
        if (loginNeeded) {
            console.log('📝 正在登录...');

            // 简单的登录流程
            await page.locator('input[type="email"], input[type="text"]').first().fill('641600780@qq.com');
            await page.waitForTimeout(500);
            await page.locator('input[type="password"]').first().fill('353980swsgbo');
            await page.waitForTimeout(500);

            // 查找登录按钮并点击
            const buttons = await page.locator('button').all();
            for (const button of buttons) {
                const text = await button.textContent();
                if (text && (text.includes('登录') || text.toLowerCase().includes('login') || text.toLowerCase().includes('sign'))) {
                    await button.click();
                    break;
                }
            }

            await page.waitForTimeout(5000);
        } else {
            console.log('✅ 已经登录');
        }

        // 等待页面完全加载
        await page.waitForLoadState('networkidle', { timeout: 15000 });
        await page.waitForTimeout(3000);

        console.log('🔍 正在查找AI智能体简历项目...');

        // 截图当前页面状态
        await page.screenshot({ path: 'dokploy-current-page.png' });
        console.log('📸 已保存当前页面截图');

        // 使用JavaScript直接操作DOM来查找和点击项目
        const projectClicked = await page.evaluate(() => {
            return new Promise((resolve) => {
                // 查找所有包含"AI智能体简历"文本的元素
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null
                );

                let node;
                let foundElement = null;

                while (node = walker.nextNode()) {
                    if (node.textContent.includes('AI智能体简历')) {
                        // 找到包含这个文本的父元素
                        let parent = node.parentElement;
                        while (parent && parent !== document.body) {
                            // 检查是否看起来像一个可点击的项目卡片
                            const rect = parent.getBoundingClientRect();
                            const hasClass = parent.className !== '';
                            const hasId = parent.id !== '';

                            // 如果元素有合理的尺寸和类名/ID，很可能就是项目卡片
                            if (rect.width > 100 && rect.height > 30 && (hasClass || hasId)) {
                                foundElement = parent;
                                break;
                            }
                            parent = parent.parentElement;
                        }

                        if (foundElement) break;
                    }
                }

                if (foundElement) {
                    // 点击找到的元素
                    foundElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    setTimeout(() => {
                        foundElement.click();
                        resolve(true);
                    }, 500);
                } else {
                    resolve(false);
                }
            });
        });

        if (projectClicked) {
            console.log('✅ 成功点击AI智能体简历项目');
        } else {
            // 备用方法：尝试直接查找并点击
            console.log('⚠️ 第一种方法失败，尝试备用方法...');

            try {
                // 尝试查找包含项目名称的元素
                const allTextElements = await page.locator('*').all();
                console.log(`🔍 正在检查 ${allTextElements.length} 个元素...`);

                for (const element of allTextElements.slice(0, 500)) { // 限制检查数量
                    try {
                        const text = await element.textContent();
                        if (text === 'AI智能体简历' ||
                            (text.includes('AI智能体简历') && text.length < 50)) {

                            // 检查元素是否可见和可点击
                            if (await element.isVisible()) {
                                console.log('✅ 找到项目元素，正在点击...');
                                await element.click();
                                console.log('✅ 成功点击项目');
                                break;
                            }
                        }
                    } catch (e) {
                        continue;
                    }
                }
            } catch (error) {
                console.log('⚠️ 备用方法也失败:', error.message);
            }
        }

        // 等待页面导航或变化
        console.log('⏳ 等待项目详情页加载...');
        await page.waitForTimeout(8000);

        // 检查URL是否变化
        const currentUrl = page.url();
        console.log('🌐 当前URL:', currentUrl);

        // 截图项目页面
        await page.screenshot({ path: 'dokploy-project-page.png' });
        console.log('📸 已保存项目页面截图');

        console.log('🔄 正在查找重新部署相关功能...');

        // 使用JavaScript查找并点击部署相关的按钮
        const deployActionTaken = await page.evaluate(() => {
            return new Promise((resolve) => {
                // 查找所有按钮和可点击元素
                const clickableElements = document.querySelectorAll('button, [role="button"], .btn, [class*="button"], [onclick]');

                for (const element of clickableElements) {
                    const text = element.textContent?.toLowerCase() || '';
                    const className = element.className?.toLowerCase() || '';

                    // 查找包含部署相关关键词的元素
                    if (text.includes('redeploy') || text.includes('deploy') ||
                        text.includes('重新部署') || text.includes('部署') ||
                        className.includes('deploy') || className.includes('redeploy')) {

                        console.log('找到部署相关元素:', text.trim(), className);

                        // 点击找到的元素
                        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => {
                            element.click();
                            resolve(true);
                        }, 500);
                        return;
                    }
                }

                resolve(false);
            });
        });

        if (deployActionTaken) {
            console.log('✅ 成功触发部署操作');
        } else {
            console.log('⚠️ 未找到明显的部署按钮，尝试查找菜单...');

            // 查找可能的菜单按钮（三个点、更多选项等）
            const menuButton = await page.locator('button').filter(async button => {
                const text = await button.textContent();
                return text && (text.includes('...') || text.includes('⋮') || text.includes('⋯') ||
                               text.includes('more') || text.includes('更多'));
            }).first();

            if (await menuButton.isVisible({ timeout: 3000 })) {
                console.log('✅ 找到菜单按钮，正在点击...');
                await menuButton.click();
                await page.waitForTimeout(2000);

                // 查找菜单中的部署选项
                const deployMenuItem = await page.locator('[role="menuitem"], .menu-item, [class*="menu"]').filter(async item => {
                    const text = await item.textContent();
                    return text && (text.toLowerCase().includes('deploy') || text.includes('部署'));
                }).first();

                if (await deployMenuItem.isVisible({ timeout: 3000 })) {
                    await deployMenuItem.click();
                    console.log('✅ 已点击菜单中的部署选项');
                } else {
                    // 尝试查找所有可能包含部署文本的元素
                    const allElements = await page.locator('*').all();
                    for (const element of allElements.slice(0, 200)) {
                        try {
                            const text = await element.textContent();
                            if (text && (text.toLowerCase().includes('deploy') || text.includes('部署'))) {
                                if (await element.isVisible()) {
                                    await element.click();
                                    console.log('✅ 已点击部署相关元素');
                                    break;
                                }
                            }
                        } catch (e) {
                            continue;
                        }
                    }
                }
            }
        }

        // 等待部署响应
        await page.waitForTimeout(3000);

        // 检查是否有确认对话框
        const hasDialog = await page.evaluate(() => {
            const dialogs = document.querySelectorAll('[role="dialog"], .modal, .dialog, [class*="confirm"], [class*="popup"]');
            return dialogs.length > 0;
        });

        if (hasDialog) {
            console.log('⚠️ 检测到对话框，正在查找确认按钮...');

            const confirmClicked = await page.evaluate(() => {
                const buttons = document.querySelectorAll('button');
                for (const button of buttons) {
                    const text = button.textContent?.toLowerCase() || '';
                    if (text.includes('confirm') || text.includes('yes') ||
                        text.includes('确认') || text.includes('是') ||
                        text.includes('continue') || text.includes('继续')) {
                        button.click();
                        return true;
                    }
                }
                return false;
            });

            if (confirmClicked) {
                console.log('✅ 已确认操作');
            }
        }

        console.log('🚀 部署操作已执行！');

        // 监控部署进度
        console.log('⏳ 开始监控部署进度（2分钟）...');

        for (let i = 0; i < 12; i++) {
            await page.waitForTimeout(10000);

            // 获取页面状态信息
            const statusInfo = await page.evaluate(() => {
                // 查找可能包含状态信息的元素
                const statusElements = document.querySelectorAll('[class*="status"], [class*="log"], [class*="progress"], [class*="deploy"]');
                const results = [];

                statusElements.forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 0 && text.length < 500) {
                        results.push(text);
                    }
                });

                return results.slice(0, 10);
            });

            if (statusInfo.length > 0) {
                console.log(`📊 部署状态 (${(i + 1) * 10}秒):`, statusInfo.slice(0, 3));
            }

            // 定期截图
            if (i % 3 === 0) {
                await page.screenshot({ path: `dokploy-monitor-${i + 1}.png` });
                console.log('📸 已保存监控截图');
            }
        }

        // 最终状态
        await page.screenshot({ path: 'dokploy-final-result.png', fullPage: true });
        console.log('📸 已保存最终状态截图');

        console.log('✅ 自动化操作完成');
        console.log('🌐 请访问Dokploy面板查看详细状态: http://113.45.64.145:3000');

        // 保持浏览器打开
        console.log('⏰ 浏览器将保持打开30秒以便手动检查...');
        await page.waitForTimeout(30000);

    } catch (error) {
        console.error('❌ 发生错误:', error.message);

        // 错误时截图
        await page.screenshot({ path: 'dokploy-error-screenshot.png', fullPage: true });
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