const { chromium } = require('playwright');
const fs = require('fs');

async function monitorDeployment() {
    const browser = await chromium.launch({
        headless: false,
        slowMo: 500
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🔍 开始监控Dokploy部署状态...');

        // 访问应用页面
        console.log('📍 访问ai-resume-platform应用页面...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'networkidle' });

        // 快速登录
        console.log('🔐 快速登录...');
        await page.fill('input[name="email"]', '641600780@qq.com');
        await page.fill('input[name="password"]', '353980swsgbo');
        await page.click('button[type="submit"]');
        await page.waitForTimeout(3000);

        // 点击应用
        console.log('🎯 进入ai-resume-platform应用...');
        await page.click('a:has-text("ai-resume-platform")');
        await page.waitForTimeout(5000);

        // 获取详细的应用状态
        console.log('📊 检查应用状态...');

        const deploymentInfo = {
            timestamp: new Date().toISOString(),
            appName: 'ai-resume-platform',
            deployment: {
                status: 'unknown',
                lastDeployment: null,
                logs: []
            },
            services: {
                backend: { name: 'Backend', status: 'unknown', port: 8000, url: null },
                frontend: { name: 'Frontend', status: 'unknown', port: 3000, url: null },
                redis: { name: 'Redis', status: 'unknown', port: 6379, url: null }
            },
            domains: [],
            healthChecks: []
        };

        // 截图当前状态
        await page.screenshot({ path: 'dokploy-monitor-current.png', fullPage: true });

        // 尝试获取部署状态信息
        try {
            // 查找状态指示器
            const statusElements = await page.$$('[class*="status"], [class*="Status"], [data-status]');
            console.log(`找到 ${statusElements.length} 个状态元素`);

            for (const element of statusElements) {
                try {
                    const text = await element.textContent();
                    const className = await element.getAttribute('class');
                    console.log(`状态: ${text.trim()} (${className})`);
                } catch (e) {
                    // 忽略错误
                }
            }

            // 查找容器或服务信息
            const serviceElements = await page.$$('[class*="container"], [class*="service"], [class*="app"]');
            console.log(`找到 ${serviceElements.length} 个服务相关元素`);

        } catch (error) {
            console.log('⚠️ 无法解析详细状态:', error.message);
        }

        // 查找日志或终端输出
        console.log('📝 查找部署日志...');

        const logSelectors = [
            'pre',
            'code',
            '[class*="log"]',
            '[class*="terminal"]',
            '[class*="console"]',
            '[id*="log"]'
        ];

        for (const selector of logSelectors) {
            try {
                const logs = await page.$$(selector);
                if (logs.length > 0) {
                    console.log(`找到 ${logs.length} 个日志元素 (${selector})`);

                    for (let i = 0; i < Math.min(logs.length, 3); i++) {
                        const logText = await logs[i].textContent();
                        if (logText && logText.trim().length > 0) {
                            deploymentInfo.deployment.logs.push({
                                source: selector,
                                content: logText.trim().substring(0, 500)
                            });
                        }
                    }
                }
            } catch (e) {
                // 继续尝试其他选择器
            }
        }

        // 查找域名或访问地址
        console.log('🌐 查找访问地址...');

        try {
            const pageContent = await page.content();

            // 查找可能的域名配置
            const domainPatterns = [
                /domain[:\s]*([a-zA-Z0-9.-]+)/gi,
                /url[:\s]*([a-zA-Z0-9.-]+)/gi,
                /http[s]?:\/\/[a-zA-Z0-9.-]+/gi
            ];

            for (const pattern of domainPatterns) {
                const matches = pageContent.match(pattern);
                if (matches) {
                    deploymentInfo.domains.push(...matches);
                }
            }

            // 如果没有找到域名，使用IP地址
            if (deploymentInfo.domains.length === 0) {
                deploymentInfo.domains.push('http://113.45.64.145:3000');
            }

        } catch (error) {
            console.log('⚠️ 无法解析域名信息');
        }

        // 尝试检查服务健康状态
        console.log('🏥 检查服务健康状态...');

        const healthChecks = [
            { name: 'Backend', url: 'http://113.45.64.145:8000', path: '/health' },
            { name: 'Frontend', url: 'http://113.45.64.145:3000', path: '/' },
            { name: 'Redis', url: 'http://113.45.64.145:6379', path: '' }
        ];

        // 在新页面中检查服务健康状态
        for (const service of healthChecks) {
            try {
                const healthPage = await context.newPage();
                const serviceUrl = service.url + service.path;

                console.log(`检查 ${service.name}: ${serviceUrl}`);

                try {
                    await healthPage.goto(serviceUrl, { timeout: 10000, waitUntil: 'domcontentloaded' });

                    const status = healthPage.status();
                    const title = await healthPage.title();

                    deploymentInfo.healthChecks.push({
                        service: service.name,
                        url: serviceUrl,
                        status: status === 200 ? 'healthy' : 'unhealthy',
                        httpStatus: status,
                        title: title
                    });

                    if (status === 200) {
                        if (service.name === 'Backend') {
                            deploymentInfo.services.backend.status = 'healthy';
                            deploymentInfo.services.backend.url = serviceUrl;
                        } else if (service.name === 'Frontend') {
                            deploymentInfo.services.frontend.status = 'healthy';
                            deploymentInfo.services.frontend.url = serviceUrl;
                        } else if (service.name === 'Redis') {
                            deploymentInfo.services.redis.status = 'healthy';
                        }
                    }

                } catch (healthError) {
                    deploymentInfo.healthChecks.push({
                        service: service.name,
                        url: serviceUrl,
                        status: 'unreachable',
                        error: healthError.message
                    });
                }

                await healthPage.close();
            } catch (error) {
                console.log(`❌ 无法检查 ${service.name}:`, error.message);
            }
        }

        // 生成详细的部署报告
        console.log('📋 生成部署报告...');

        const reportPath = 'dokploy-deployment-report.json';
        fs.writeFileSync(reportPath, JSON.stringify(deploymentInfo, null, 2));

        // 生成可读的报告
        const readableReport = `
# Dokploy部署报告

## 基本信息
- 应用名称: ${deploymentInfo.appName}
- 检查时间: ${deploymentInfo.timestamp}
- 报告文件: ${reportPath}

## 服务状态

### Backend服务
- 端口: ${deploymentInfo.services.backend.port}
- 状态: ${deploymentInfo.services.backend.status}
- 访问地址: ${deploymentInfo.services.backend.url || '未配置'}

### Frontend服务
- 端口: ${deploymentInfo.services.frontend.port}
- 状态: ${deploymentInfo.services.frontend.status}
- 访问地址: ${deploymentInfo.services.frontend.url || '未配置'}

### Redis服务
- 状态: ${deploymentInfo.services.redis.status}

## 健康检查结果
${deploymentInfo.healthChecks.map(check => `
### ${check.service}
- URL: ${check.url}
- 状态: ${check.status}
- HTTP状态: ${check.httpStatus || 'N/A'}
${check.error ? `- 错误: ${check.error}` : ''}
`).join('\n')}

## 访问地址
${deploymentInfo.domains.map(domain => `- ${domain}`).join('\n')}

## 部署日志
${deploymentInfo.deployment.logs.map(log => `
### 来自 ${log.source}:
\`\`\`
${log.content.substring(0, 200)}${log.content.length > 200 ? '...' : ''}
\`\`\`
`).join('\n---\n')}

## 截图文件
- 当前状态: dokploy-monitor-current.png
- 完整页面: dokploy-monitor-current-full.png
`;

        fs.writeFileSync('dokploy-deployment-report.md', readableReport);

        console.log('✅ 部署监控完成！');
        console.log('📊 详细报告已保存:');
        console.log(`   - JSON格式: ${reportPath}`);
        console.log(`   - Markdown格式: dokploy-deployment-report.md`);
        console.log(`   - 截图: dokploy-monitor-current.png`);

        // 显示摘要
        console.log('\n📋 部署摘要:');
        console.log(`Backend服务: ${deploymentInfo.services.backend.status} (端口8000)`);
        console.log(`Frontend服务: ${deploymentInfo.services.frontend.status} (端口3000)`);
        console.log(`Redis服务: ${deploymentInfo.services.redis.status}`);

        console.log('\n🌐 访问地址:');
        deploymentInfo.domains.forEach(domain => {
            console.log(`  - ${domain}`);
        });

        // 等待用户查看
        console.log('\n保持浏览器开启30秒供查看...');
        await page.waitForTimeout(30000);

    } catch (error) {
        console.error('❌ 监控过程中出现错误:', error);
        await page.screenshot({ path: 'dokploy-monitor-error.png' });
    } finally {
        await browser.close();
    }
}

// 运行监控流程
monitorDeployment().catch(console.error);