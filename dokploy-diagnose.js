const { chromium } = require('playwright');
const fs = require('fs');

async function diagnoseDeployment() {
    const browser = await chromium.launch({
        headless: false,
        slowMo: 1000
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🔍 开始Dokploy部署诊断...');

        // 访问并登录
        console.log('📍 访问Dokploy面板...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'networkidle' });

        console.log('🔐 登录中...');
        await page.fill('input[name="email"]', '641600780@qq.com');
        await page.fill('input[name="password"]', '353980swsgbo');
        await page.click('button[type="submit"]');
        await page.waitForTimeout(3000);

        // 导航到应用页面
        console.log('🎯 查找ai-resume-platform应用...');

        // 截图登录后状态
        await page.screenshot({ path: 'dokploy-diagnose-01-dashboard.png' });

        try {
            // 尝试多种可能的选择器来找到应用
            const appSelectors = [
                'a:has-text("ai-resume-platform")',
                'a[href*="ai-resume"]',
                '[class*="app-card"]:has-text("ai-resume")',
                'div:has-text("ai-resume-platform")'
            ];

            let appFound = false;
            for (const selector of appSelectors) {
                try {
                    const element = await page.$(selector);
                    if (element) {
                        console.log(`✅ 找到应用，使用选择器: ${selector}`);
                        await element.click();
                        appFound = true;
                        break;
                    }
                } catch (e) {
                    // 继续尝试下一个选择器
                }
            }

            if (!appFound) {
                console.log('⚠️ 未找到应用链接，尝试手动导航...');
                // 尝试直接访问应用URL
                await page.goto('http://113.45.64.145:3000/dashboard/applications/ai-resume-platform', { waitUntil: 'networkidle' });
            }

            await page.waitForTimeout(5000);
            await page.screenshot({ path: 'dokploy-diagnose-02-app-page.png', fullPage: true });

            // 收集详细的应用信息
            const diagnosis = {
                timestamp: new Date().toISOString(),
                summary: {
                    status: 'unknown',
                    issues: []
                },
                services: {},
                containers: [],
                logs: [],
                errors: []
            };

            // 检查服务状态
            console.log('🔧 检查服务配置...');

            try {
                // 查找服务容器信息
                const serviceInfo = await page.evaluate(() => {
                    const services = [];

                    // 查找所有可能包含服务信息的元素
                    const elements = document.querySelectorAll('*');
                    elements.forEach(el => {
                        const text = el.textContent;
                        if (text && (text.includes('Backend') || text.includes('Frontend') ||
                                    text.includes('Redis') || text.includes('MySQL') ||
                                    text.includes('backend') || text.includes('frontend'))) {
                            const className = el.className;
                            const tagName = el.tagName;
                            if (className && (className.includes('container') || className.includes('service') ||
                                             className.includes('card') || className.includes('status'))) {
                                services.push({
                                    tagName,
                                    className,
                                    text: text.substring(0, 100)
                                });
                            }
                        }
                    });

                    return services;
                });

                diagnosis.containers = serviceInfo;
                console.log(`找到 ${serviceInfo.length} 个服务相关信息`);

            } catch (error) {
                console.log('⚠️ 无法获取服务信息:', error.message);
                diagnosis.errors.push(`服务信息获取失败: ${error.message}`);
            }

            // 查找日志或部署信息
            console.log('📝 查找部署日志...');

            try {
                // 点击日志标签页（如果存在）
                const logTab = await page.$('a:has-text("Logs"), button:has-text("Logs"), [role="tab"]:has-text("Logs")');
                if (logTab) {
                    await logTab.click();
                    await page.waitForTimeout(3000);
                    await page.screenshot({ path: 'dokploy-diagnose-03-logs.png', fullPage: true });
                }

                // 获取日志内容
                const logContent = await page.evaluate(() => {
                    const logs = [];
                    const logElements = document.querySelectorAll('pre, code, [class*="log"], [class*="terminal"], [class*="console"]');
                    logElements.forEach(el => {
                        const text = el.textContent;
                        if (text && text.trim().length > 0) {
                            logs.push({
                                tag: el.tagName,
                                class: el.className,
                                content: text.substring(0, 500)
                            });
                        }
                    });
                    return logs;
                });

                diagnosis.logs = logContent;

            } catch (error) {
                console.log('⚠️ 无法获取日志信息:', error.message);
                diagnosis.errors.push(`日志获取失败: ${error.message}`);
            }

            // 查找容器状态和健康检查
            console.log('🏥 检查容器健康状态...');

            try {
                // 尝试找到容器状态信息
                const containerStatus = await page.evaluate(() => {
                    const statusInfo = [];

                    // 查找状态指示器
                    const statusElements = document.querySelectorAll('[class*="status"], [data-status], [class*="badge"], [class*="indicator"]');
                    statusElements.forEach(el => {
                        const text = el.textContent;
                        const className = el.className;
                        if (text && text.trim().length > 0 && text.length < 50) {
                            statusInfo.push({
                                text: text.trim(),
                                className,
                                backgroundColor: el.style?.backgroundColor,
                                color: el.style?.color
                            });
                        }
                    });

                    return statusInfo;
                });

                console.log('容器状态信息:', containerStatus);

                // 分析状态
                containerStatus.forEach(status => {
                    if (status.text.toLowerCase().includes('error') || status.text.toLowerCase().includes('failed')) {
                        diagnosis.summary.issues.push(`容器错误: ${status.text}`);
                    }
                    if (status.text.toLowerCase().includes('backend')) {
                        diagnosis.services.backend = status.text;
                    }
                    if (status.text.toLowerCase().includes('frontend')) {
                        diagnosis.services.frontend = status.text;
                    }
                    if (status.text.toLowerCase().includes('redis')) {
                        diagnosis.services.redis = status.text;
                    }
                });

            } catch (error) {
                console.log('⚠️ 无法获取容器状态:', error.message);
                diagnosis.errors.push(`容器状态获取失败: ${error.message}`);
            }

            // 直接检查服务端点
            console.log('🔗 直接检查服务端点...');

            const serviceEndpoints = [
                { name: 'Backend', url: 'http://113.45.64.145:8000', expected: 'API Backend' },
                { name: 'Frontend', url: 'http://113.45.64.145:3000', expected: 'AI Resume Platform' },
                { name: 'Backend Health', url: 'http://113.45.64.145:8000/health', expected: 'Health check endpoint' },
                { name: 'Backend API', url: 'http://113.45.64.145:8000/api', expected: 'API endpoint' }
            ];

            for (const endpoint of serviceEndpoints) {
                try {
                    console.log(`检查 ${endpoint.name}: ${endpoint.url}`);

                    const testPage = await context.newPage();
                    const response = await testPage.goto(endpoint.url, {
                        timeout: 15000,
                        waitUntil: 'domcontentloaded'
                    }).catch(() => null);

                    if (response) {
                        const status = response.status();
                        const headers = response.headers();

                        console.log(`  状态: ${status}`);
                        console.log(`  Content-Type: ${headers['content-type'] || 'N/A'}`);

                        diagnosis.services[endpoint.name.toLowerCase().replace(' ', '_')] = {
                            url: endpoint.url,
                            status,
                            contentType: headers['content-type'] || 'N/A',
                            reachable: status < 500
                        };

                        if (status >= 500) {
                            diagnosis.summary.issues.push(`${endpoint.name} 返回 ${status} 错误`);
                        } else if (status >= 400) {
                            diagnosis.summary.issues.push(`${endpoint.name} 返回 ${status} 客户端错误`);
                        } else {
                            console.log(`  ✅ ${endpoint.name} 可访问`);
                        }
                    } else {
                        diagnosis.services[endpoint.name.toLowerCase().replace(' ', '_')] = {
                            url: endpoint.url,
                            status: 'timeout',
                            reachable: false
                        };
                        diagnosis.summary.issues.push(`${endpoint.name} 无法连接 (超时)`);
                        console.log(`  ❌ ${endpoint.name} 超时`);
                    }

                    await testPage.close();

                } catch (error) {
                    diagnosis.services[endpoint.name.toLowerCase().replace(' ', '_')] = {
                        url: endpoint.url,
                        error: error.message,
                        reachable: false
                    };
                    diagnosis.summary.issues.push(`${endpoint.name} 连接失败: ${error.message}`);
                    console.log(`  ❌ ${endpoint.name} 错误:`, error.message);
                }
            }

            // 检查Redis连接（特殊处理）
            console.log('🔴 检查Redis连接...');
            try {
                // Redis不是HTTP服务，需要特殊检查
                const net = require('net');
                const redisCheck = new Promise((resolve, reject) => {
                    const socket = new net.Socket();
                    socket.setTimeout(5000);

                    socket.connect(6379, '113.45.64.145', () => {
                        socket.destroy();
                        resolve(true);
                    });

                    socket.on('timeout', () => {
                        socket.destroy();
                        reject(new Error('Connection timeout'));
                    });

                    socket.on('error', (err) => {
                        socket.destroy();
                        reject(err);
                    });
                });

                await redisCheck;
                diagnosis.services.redis = {
                    host: '113.45.64.145',
                    port: 6379,
                    status: 'reachable',
                    reachable: true
                };
                console.log('  ✅ Redis 可访问');

            } catch (error) {
                diagnosis.services.redis = {
                    host: '113.45.64.145',
                    port: 6379,
                    status: 'unreachable',
                    error: error.message,
                    reachable: false
                };
                diagnosis.summary.issues.push(`Redis 无法连接: ${error.message}`);
                console.log(`  ❌ Redis 错误:`, error.message);
            }

            // 生成诊断报告
            console.log('📋 生成诊断报告...');

            const reportPath = 'dokploy-diagnosis-report.json';
            fs.writeFileSync(reportPath, JSON.stringify(diagnosis, null, 2));

            // 生成可读的报告
            const readableReport = `
# Dokploy部署诊断报告

## 诊断时间
${diagnosis.timestamp}

## 问题摘要
${diagnosis.summary.issues.length > 0 ?
  diagnosis.summary.issues.map(issue => `- ❌ ${issue}`).join('\n') :
  '✅ 未发现明显问题'}

## 服务状态详情

### Backend服务 (端口8000)
${diagnosis.services.backend ?
  `- URL: ${diagnosis.services.backend.url || 'N/A'}
- 状态: ${diagnosis.services.backend.status || diagnosis.services.backend}
- 可访问: ${diagnosis.services.backend.reachable ? '✅' : '❌'}
${diagnosis.services.backend.error ? `- 错误: ${diagnosis.services.backend.error}` : ''}` :
  '- 未找到状态信息'}

### Frontend服务 (端口3000)
${diagnosis.services.frontend ?
  `- URL: ${diagnosis.services.frontend.url || 'N/A'}
- 状态: ${diagnosis.services.frontend.status || diagnosis.services.frontend}
- 可访问: ${diagnosis.services.frontend.reachable ? '✅' : '❌'}
${diagnosis.services.frontend.error ? `- 错误: ${diagnosis.services.frontend.error}` : ''}` :
  '- 未找到状态信息'}

### Redis服务 (端口6379)
${diagnosis.services.redis ?
  `- 主机: ${diagnosis.services.redis.host || '113.45.64.145'}
- 端口: ${diagnosis.services.redis.port || 6379}
- 状态: ${diagnosis.services.redis.status}
- 可访问: ${diagnosis.services.redis.reachable ? '✅' : '❌'}
${diagnosis.services.redis.error ? `- 错误: ${diagnosis.services.redis.error}` : ''}` :
  '- 未找到状态信息'}

## 容器信息
找到 ${diagnosis.containers.length} 个服务相关元素

## 错误列表
${diagnosis.errors.length > 0 ?
  diagnosis.errors.map(err => `- ${err}`).join('\n') :
  '无错误'}

## 截图文件
- 1. Dashboard: dokploy-diagnose-01-dashboard.png
- 2. 应用页面: dokploy-diagnose-02-app-page.png
- 3. 日志页面: dokploy-diagnose-03-logs.png

## 建议
${diagnosis.summary.issues.length > 0 ?
  '⚠️ 发现问题，请查看上述错误信息并采取相应措施。' :
  '✅ 所有服务正常运行'}
`;

            fs.writeFileSync('dokploy-diagnosis-report.md', readableReport);

            console.log('✅ 诊断完成！');
            console.log('📊 报告已保存:');
            console.log(`   - JSON: ${reportPath}`);
            console.log(`   - Markdown: dokploy-diagnosis-report.md`);
            console.log(`   - 截图: dokploy-diagnose-*.png`);

            // 显示问题摘要
            console.log('\n📋 问题摘要:');
            if (diagnosis.summary.issues.length > 0) {
                diagnosis.summary.issues.forEach(issue => {
                    console.log(`  ❌ ${issue}`);
                });
            } else {
                console.log('  ✅ 未发现明显问题');
            }

            // 保持浏览器开启供查看
            console.log('\n保持浏览器开启60秒供详细检查...');
            await page.waitForTimeout(60000);

        } catch (navigationError) {
            console.error('❌ 应用页面导航失败:', navigationError);
            await page.screenshot({ path: 'dokploy-diagnose-navigation-error.png' });
        }

    } catch (error) {
        console.error('❌ 诊断过程中出现错误:', error);
        await page.screenshot({ path: 'dokploy-diagnose-error.png' });
    } finally {
        await browser.close();
    }
}

// 运行诊断
diagnoseDeployment().catch(console.error);