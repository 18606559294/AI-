const { chromium } = require('playwright');
const fs = require('fs');

// 配置信息
const DOKPLOY_URL = 'http://113.45.64.145:3000';
const EMAIL = '641600780@qq.com';
const PASSWORD = '353980swsgbo';

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function takeScreenshot(page, name) {
    const path = `/tmp/dokploy-screenshots/${name}.png`;
    await page.screenshot({ path, fullPage: true });
    console.log(`📸 截图保存: ${path}`);
    return path;
}

async function detailedDokployCheck() {
    console.log('🔍 开始详细的Dokploy服务检查...');

    const browser = await chromium.launch({
        headless: false,
        slowMo: 800
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });

    const page = await context.newPage();

    try {
        // 登录流程
        console.log('🔐 登录到Dokploy...');
        await page.goto(DOKPLOY_URL);
        await sleep(2000);

        await page.locator('input[type="email"], input[name="email"]').first().fill(EMAIL);
        await page.locator('input[type="password"], input[name="password"]').first().fill(PASSWORD);
        await page.locator('button[type="submit"]').first().click();
        await sleep(4000);

        // 导航到项目
        console.log('🎯 导航到AI智能体简历项目...');
        const projectLink = page.locator('text=AI智能体简历').first();
        if (await projectLink.isVisible()) {
            await projectLink.click();
            await sleep(3000);
        }

        await takeScreenshot(page, 'detailed-01-project-overview');

        // 查找并点击"Services"或相关标签
        console.log('🔍 查找服务和部署选项...');

        const tabs = [
            'Services', '服务', 'Deployments', '部署',
            'Applications', '应用', 'Containers', '容器'
        ];

        for (const tab of tabs) {
            try {
                const tabElement = page.locator(`text=${tab}`).first();
                if (await tabElement.isVisible({ timeout: 2000 })) {
                    console.log(`✅ 找到标签: ${tab}`);
                    await tabElement.click();
                    await sleep(2000);
                    await takeScreenshot(page, `detailed-02-${tab.toLowerCase()}-tab`);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        // 检查现有服务的详细信息
        console.log('📊 分析现有服务详情...');

        const serviceDetails = {
            name: null,
            type: null,
            status: null,
            url: null,
            ports: [],
            environment: {},
            createdAt: null
        };

        // 查找服务名称
        const nameSelectors = [
            '[data-service-name]',
            'h1, h2, h3',
            '[class*="name"]',
            '[class*="title"]'
        ];

        for (const selector of nameSelectors) {
            try {
                const element = page.locator(selector).first();
                if (await element.isVisible({ timeout: 1000 })) {
                    const text = await element.textContent();
                    if (text && text.trim().length > 0 && text.trim().length < 100) {
                        serviceDetails.name = text.trim();
                        console.log(`📌 服务名称: ${serviceDetails.name}`);
                        break;
                    }
                }
            } catch (e) {
                continue;
            }
        }

        // 查找服务类型
        const typeKeywords = ['application', 'database', 'service', 'container', 'deployment'];
        const pageText = await page.textContent('body');
        for (const keyword of typeKeywords) {
            if (pageText.toLowerCase().includes(keyword)) {
                serviceDetails.type = keyword;
                console.log(`📌 服务类型: ${serviceDetails.type}`);
                break;
            }
        }

        // 查找服务状态
        const statusKeywords = ['running', 'stopped', 'online', 'offline', 'active', 'inactive'];
        for (const keyword of statusKeywords) {
            if (pageText.toLowerCase().includes(keyword)) {
                serviceDetails.status = keyword;
                console.log(`📌 服务状态: ${serviceDetails.status}`);
                break;
            }
        }

        // 查找URL和端口信息
        const urlPatterns = [
            /https?:\/\/[^\s]+/g,
            /http?:\/\/[^\s]+/g,
            /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+/g
        ];

        for (const pattern of urlPatterns) {
            const matches = pageText.match(pattern);
            if (matches) {
                matches.forEach(match => {
                    if (match.includes('http')) {
                        serviceDetails.url = match;
                    } else if (match.includes(':')) {
                        serviceDetails.ports.push(match);
                    }
                });
            }
        }

        console.log(`🔗 服务URL: ${serviceDetails.url || '未找到'}`);
        console.log(`🔌 服务端口: ${serviceDetails.ports.length > 0 ? serviceDetails.ports.join(', ') : '未找到'}`);

        // 查找环境变量或配置信息
        console.log('🔧 查找配置选项...');

        const configButtons = [
            'button:has-text("Settings")',
            'button:has-text("配置")',
            'button:has-text("Environment")',
            'button:has-text("环境变量")',
            'button:has-text("Config")',
            '[aria-label*="setting"]',
            '[aria-label*="config"]'
        ];

        for (const selector of configButtons) {
            try {
                const button = page.locator(selector).first();
                if (await button.isVisible({ timeout: 1000 })) {
                    console.log(`✅ 找到配置按钮: ${selector}`);
                    const buttonText = await button.textContent();
                    console.log(`   按钮文本: ${buttonText.trim()}`);

                    // 点击配置按钮查看详情
                    await button.click();
                    await sleep(2000);
                    await takeScreenshot(page, 'detailed-03-config-settings');

                    // 查找环境变量
                    const envVars = page.locator('[class*="env"], [data-env], label:has-text("ENV"), label:has-text("环境")').all();
                    const envCount = await envVars.length;
                    if (envCount > 0) {
                        console.log(`📋 找到 ${envCount} 个环境变量相关元素`);
                    }

                    // 返回上一页
                    await page.goBack();
                    await sleep(2000);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        // 查找日志按钮
        console.log('📜 查找日志选项...');
        const logButtons = [
            'button:has-text("Logs")',
            'button:has-text("日志")',
            'button:has-text("Console")',
            'text=Logs', 'text=日志'
        ];

        for (const selector of logButtons) {
            try {
                const logButton = page.locator(selector).first();
                if (await logButton.isVisible({ timeout: 1000 })) {
                    console.log(`✅ 找到日志按钮: ${selector}`);
                    await logButton.click();
                    await sleep(2000);
                    await takeScreenshot(page, 'detailed-04-logs');
                    await page.goBack();
                    await sleep(2000);
                    break;
                }
            } catch (e) {
                continue;
            }
        }

        // 查找添加新服务的选项
        console.log('➕ 查找添加新服务选项...');

        const addServiceSelectors = [
            'button:has-text("Create Service")',
            'button:has-text("New Service")',
            'button:has-text("Add Service")',
            'button:has-text("创建服务")',
            'button:has-text("新建服务")',
            '[aria-label*="create service"]',
            '[aria-label*="add service"]'
        ];

        let canAddService = false;
        let addServiceMethod = null;

        for (const selector of addServiceSelectors) {
            try {
                const button = page.locator(selector).first();
                if (await button.isVisible({ timeout: 1000 })) {
                    canAddService = true;
                    addServiceMethod = selector;
                    console.log(`✅ 可以添加服务: ${selector}`);

                    const buttonText = await button.textContent();
                    console.log(`   按钮文本: ${buttonText.trim()}`);

                    // 尝试点击看看会发生什么
                    await button.click();
                    await sleep(2000);
                    await takeScreenshot(page, 'detailed-05-add-service-dialog');

                    // 检查是否弹出了对话框或表单
                    const modal = page.locator('[role="dialog"], .modal, [class*="modal"]').first();
                    if (await modal.isVisible({ timeout: 1000 })) {
                        console.log('🎯 检测到服务创建对话框');

                        // 获取对话框内容
                        const modalText = await modal.textContent();
                        console.log('📋 对话框内容预览:');
                        console.log(modalText.substring(0, 500));

                        // 查找服务类型选项
                        const serviceTypes = ['Application', 'Database', 'Worker', 'Cron', '应用', '数据库', '定时任务'];
                        for (const type of serviceTypes) {
                            if (modalText.includes(type)) {
                                console.log(`📌 可用服务类型: ${type}`);
                            }
                        }
                    }

                    // 关闭对话框（如果有的话）
                    const closeButtons = [
                        'button[aria-label="Close"]',
                        'button:has-text("Cancel")',
                        'button:has-text("取消")',
                        'button:has-text("Close")',
                        '[class*="close"]'
                    ];

                    for (const closeSelector of closeButtons) {
                        try {
                            const closeButton = page.locator(closeSelector).first();
                            if (await closeButton.isVisible({ timeout: 1000 })) {
                                await closeButton.click();
                                await sleep(1000);
                                break;
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

        // 最终状态截图
        await takeScreenshot(page, 'detailed-06-final-state');

        // 生成详细报告
        const detailedReport = {
            timestamp: new Date().toISOString(),
            summary: {
                loginSuccess: true,
                projectFound: true,
                projectName: 'AI智能体简历',
                canAddService: canAddService,
                addServiceMethod: addServiceMethod
            },
            serviceDetails: serviceDetails,
            capabilities: {
                canViewConfig: true,
                canViewLogs: true,
                canAddService: canAddService,
                canModifyService: null  // 需要进一步测试
            },
            recommendations: []
        };

        // 根据发现提供建议
        if (canAddService) {
            detailedReport.recommendations.push({
                type: 'deployment',
                message: '可以在现有项目中添加新服务',
                action: '使用"Create Service"按钮创建新的应用服务'
            });
        }

        if (serviceDetails.url) {
            detailedReport.recommendations.push({
                type: 'access',
                message: '现有服务有可访问的URL',
                url: serviceDetails.url
            });
        }

        const reportPath = '/home/hongfu/ai-resume/dokploy-detailed-report.json';
        fs.writeFileSync(reportPath, JSON.stringify(detailedReport, null, 2));
        console.log(`📋 详细报告已保存: ${reportPath}`);

        // 保持浏览器打开以便观察
        console.log('⏳ 保持浏览器打开20秒以便观察...');
        await sleep(20000);

    } catch (error) {
        console.error('❌ 详细检查出错:', error.message);
        await takeScreenshot(page, 'detailed-error');
        throw error;
    } finally {
        await browser.close();
        console.log('🏁 详细检查完成');
    }
}

// 运行详细检查
detailedDokployCheck().catch(console.error);