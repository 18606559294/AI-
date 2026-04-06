const { chromium } = require('playwright');

async function triggerRedeploy() {
    const browser = await chromium.launch({
        headless: false,
        slowMo: 300
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
            await page.locator('input[type="email"], input[type="text"]').first().fill('641600780@qq.com');
            await page.waitForTimeout(500);

            // 输入密码
            await page.locator('input[type="password"]').first().fill('353980swsgbo');
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

        // 使用更精确的方法查找项目卡片
        const projectCard = await page.locator('div').filter(async div => {
            const text = await div.textContent();
            const hasProjectName = text && text.includes('AI智能体简历');
            const hasCreatedInfo = text && text.includes('Created');
            const hasServiceInfo = text && text.includes('service');

            // 查找包含项目名称和相关信息的卡片
            return hasProjectName && (hasCreatedInfo || hasServiceInfo);
        }).first();

        if (await projectCard.isVisible({ timeout: 5000 })) {
            console.log('✅ 找到AI智能体简历项目卡片');

            // 获取卡片的位置信息
            const box = await projectCard.boundingBox();
            console.log('📍 项目卡片位置:', box);

            // 点击卡片中心位置
            if (box) {
                const x = box.x + box.width / 2;
                const y = box.y + box.height / 2;
                console.log('🖱️ 将点击位置:', x, y);

                // 使用page.click来点击卡片
                await page.click(`div:has-text('AI智能体简历') >> div:has-text('Created')`, {
                    position: { x: box.width / 2, y: box.height / 2 }
                });
            } else {
                // 如果无法获取位置，直接点击
                await projectCard.click();
            }

            console.log('✅ 已点击项目卡片');
        } else {
            // 尝试备用方法
            console.log('⚠️ 第一种方法失败，尝试备用方法...');

            // 直接查找包含项目文本的元素并点击
            await page.click('text=AI智能体简历', {
                timeout: 5000,
                force: true
            });

            console.log('✅ 已通过文本定位点击项目');
        }

        // 等待项目详情页加载
        console.log('⏳ 等待项目详情页加载...');
        await page.waitForTimeout(5000);

        // 检查URL变化或页面内容变化
        const currentUrl = page.url();
        console.log('🌐 当前URL:', currentUrl);

        // 截图项目详情页
        await page.screenshot({ path: 'dokploy-project-detail.png' });
        console.log('📸 已保存项目详情页截图');

        console.log('🔄 正在查找重新部署按钮...');

        // 在项目详情页中查找部署相关的按钮
        const redeployButton = await page.locator('button').filter(async button => {
            const text = await button.textContent();
            const className = await button.getAttribute('class');

            return text && (
                text.toLowerCase().includes('redeploy') ||
                text.toLowerCase().includes('deploy') ||
                text.includes('重新部署') ||
                text.includes('部署') ||
                text.includes('Redeploy')
            );
        }).first();

        if (await redeployButton.isVisible({ timeout: 5000 })) {
            const buttonText = await redeployButton.textContent();
            console.log(`✅ 找到部署按钮: "${buttonText.trim()}"`);

            await redeployButton.click();
            console.log('✅ 已点击部署按钮');
        } else {
            // 尝试查找其他可能的部署触发方式
            console.log('⚠️ 未找到明显的部署按钮，查找其他部署方式...');

            // 查找可能的菜单或操作区域
            const menuButton = await page.locator('button').filter(async button => {
                const text = await button.textContent();
                return text && (text.includes('...') || text.includes('⋮') || text.includes('more'));
            }).first();

            if (await menuButton.isVisible({ timeout: 3000 })) {
                console.log('✅ 找到菜单按钮，点击展开...');
                await menuButton.click();
                await page.waitForTimeout(1000);

                // 查找菜单中的部署选项
                const deployMenuItem = await page.locator('[role="menuitem"], .menu-item, [class*="menu"]').filter(async item => {
                    const text = await item.textContent();
                    return text && (text.toLowerCase().includes('deploy') || text.includes('部署'));
                }).first();

                if (await deployMenuItem.isVisible({ timeout: 3000 })) {
                    await deployMenuItem.click();
                    console.log('✅ 已点击菜单中的部署选项');
                }
            }
        }

        // 等待确认对话框或其他响应
        await page.waitForTimeout(3000);

        // 检查是否有确认对话框
        const confirmDialog = await page.locator('[role="dialog"], .modal, .dialog').first();
        if (await confirmDialog.isVisible({ timeout: 2000 })) {
            console.log('⚠️ 检测到确认对话框');

            const confirmButton = await page.locator('button').filter(async button => {
                const text = await button.textContent();
                return text && (text.includes('确认') || text.includes('Confirm') || text.includes('是') || text.includes('Yes') || text.includes('继续'));
            }).first();

            if (await confirmButton.isVisible({ timeout: 2000 })) {
                await confirmButton.click();
                console.log('✅ 已确认部署');
            }
        }

        console.log('🚀 部署已触发！开始监控部署进度...');

        // 监控部署进度
        console.log('⏳ 正在监控部署进度（2分钟）...');

        for (let i = 0; i < 12; i++) {
            await page.waitForTimeout(10000); // 每10秒检查一次

            // 获取页面文本内容来分析状态
            const pageText = await page.evaluate(() => document.body.textContent);

            // 查找状态相关的关键词
            const statusKeywords = [
                'deploying', 'deployment', 'building', 'running',
                'success', 'failed', 'error', 'completed',
                '部署中', '部署成功', '部署失败', '构建中', '运行中'
            ];

            const foundStatus = statusKeywords.filter(keyword =>
                pageText.toLowerCase().includes(keyword.toLowerCase())
            );

            if (foundStatus.length > 0) {
                console.log(`📊 部署状态 (${(i + 1) * 10}秒):`, foundStatus.join(', '));
            }

            // 定期截图
            if (i % 3 === 0) {
                await page.screenshot({ path: `dokploy-deploy-progress-${i + 1}.png` });
                console.log('📸 已保存部署进度截图');
            }
        }

        // 最终状态检查
        await page.screenshot({ path: 'dokploy-final-status.png', fullPage: true });
        console.log('📸 已保存最终状态截图');

        console.log('✅ 部署触发和监控完成');
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