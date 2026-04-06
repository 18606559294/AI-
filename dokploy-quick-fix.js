const { chromium } = require('playwright');
const fs = require('fs');

async function quickFixDeployment() {
    const browser = await chromium.launch({
        headless: false,
        slowMo: 1500  // 减慢操作速度，便于观察
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        console.log('🔧 开始Dokploy快速修复流程...');

        // 登录
        console.log('🔐 登录Dokploy面板...');
        await page.goto('http://113.45.64.145:3000', { waitUntil: 'networkidle' });
        await page.fill('input[name="email"]', '641600780@qq.com');
        await page.fill('input[name="password"]', '353980swsgbo');
        await page.click('button[type="submit"]');
        await page.waitForTimeout(3000);

        // 导航到应用页面
        console.log('🎯 导航到ai-resume-platform应用...');
        await page.click('a:has-text("ai-resume-platform")');
        await page.waitForTimeout(5000);

        // 截图初始状态
        await page.screenshot({ path: 'dokploy-fix-01-initial.png' });

        // 修复步骤1: 停止问题服务
        console.log('🛑 步骤1: 停止问题服务...');

        const fixLog = {
            timestamp: new Date().toISOString(),
            steps: [],
            services: {
                redis: { action: 'restart', status: 'pending' },
                backend: { action: 'restart', status: 'pending' },
                mysql: { action: 'check', status: 'pending' }
            },
            errors: []
        };

        try {
            // 查找停止按钮或重启按钮
            const stopButtons = await page.$$('button:has-text("Stop"), button:has-text("停止"), [aria-label*="stop"], [aria-label*="停止"]');
            console.log(`找到 ${stopButtons.length} 个停止按钮`);

            if (stopButtons.length > 0) {
                // 优先停止Backend服务
                for (const button of stopButtons) {
                    try {
                        const buttonText = await button.textContent();
                        if (buttonText.includes('Backend') || buttonText.includes('backend')) {
                            console.log(`点击停止按钮: ${buttonText}`);
                            await button.click();
                            await page.waitForTimeout(3000);
                            fixLog.steps.push({
                                action: 'stop',
                                service: 'Backend',
                                status: 'completed'
                            });
                            break;
                        }
                    } catch (e) {
                        fixLog.errors.push(`停止Backend失败: ${e.message}`);
                    }
                }

                // 等待服务停止
                await page.waitForTimeout(5000);
                await page.screenshot({ path: 'dokploy-fix-02-after-stop.png' });
            }

        } catch (error) {
            console.log('⚠️ 停止服务时出错:', error.message);
            fixLog.errors.push(`停止服务错误: ${error.message}`);
        }

        // 修复步骤2: 重启Redis
        console.log('🔄 步骤2: 重启Redis服务...');

        try {
            // 查找Redis相关的重启按钮
            const redisButtons = await page.$$('button:has-text("Redis"), [class*="redis"] button, [data-service="redis"] button');

            for (const button of redisButtons) {
                try {
                    const buttonText = await button.textContent();
                    if (buttonText.includes('Restart') || buttonText.includes('重启') || buttonText.includes('Start') || buttonText.includes('启动')) {
                        console.log(`点击Redis重启按钮: ${buttonText}`);
                        await button.click();
                        await page.waitForTimeout(5000);

                        fixLog.services.redis.status = 'restarting';
                        fixLog.steps.push({
                            action: 'restart',
                            service: 'Redis',
                            status: 'in_progress'
                        });

                        // 等待Redis启动
                        console.log('⏳ 等待Redis启动...');
                        await page.waitForTimeout(15000);

                        // 检查Redis状态
                        const redisStatus = await page.$eval('[class*="redis"] [class*="status"], [data-service="redis"] [class*="status"]',
                            el => el.textContent).catch(() => 'unknown');

                        fixLog.services.redis.status = redisStatus;
                        console.log(`Redis状态: ${redisStatus}`);

                        if (redisStatus.includes('running') || redisStatus.includes('healthy') || redisStatus.includes('运行中') || redisStatus.includes('健康')) {
                            fixLog.services.redis.status = 'healthy';
                            console.log('✅ Redis启动成功');
                        }

                        break;
                    }
                } catch (e) {
                    console.log('Redis重启按钮点击失败:', e.message);
                }
            }

            await page.screenshot({ path: 'dokploy-fix-03-after-redis.png' });

        } catch (error) {
            console.log('⚠️ 重启Redis时出错:', error.message);
            fixLog.errors.push(`重启Redis错误: ${error.message}`);
            fixLog.services.redis.status = 'failed';
        }

        // 修复步骤3: 重启Backend
        console.log('🔄 步骤3: 重启Backend服务...');

        try {
            // 查找Backend相关的重启按钮
            const backendButtons = await page.$$('button:has-text("Backend"), [class*="backend"] button, [data-service="backend"] button');

            for (const button of backendButtons) {
                try {
                    const buttonText = await button.textContent();
                    if (buttonText.includes('Restart') || buttonText.includes('重启') || buttonText.includes('Start') || buttonText.includes('启动')) {
                        console.log(`点击Backend重启按钮: ${buttonText}`);
                        await button.click();
                        await page.waitForTimeout(5000);

                        fixLog.services.backend.status = 'restarting';
                        fixLog.steps.push({
                            action: 'restart',
                            service: 'Backend',
                            status: 'in_progress'
                        });

                        // 等待Backend启动
                        console.log('⏳ 等待Backend启动...');
                        await page.waitForTimeout(30000); // Backend需要更多时间启动

                        // 检查Backend状态
                        const backendStatus = await page.$eval('[class*="backend"] [class*="status"], [data-service="backend"] [class*="status"]',
                            el => el.textContent).catch(() => 'unknown');

                        fixLog.services.backend.status = backendStatus;
                        console.log(`Backend状态: ${backendStatus}`);

                        if (backendStatus.includes('running') || backendStatus.includes('healthy') || backendStatus.includes('运行中') || backendStatus.includes('健康')) {
                            fixLog.services.backend.status = 'healthy';
                            console.log('✅ Backend启动成功');
                        }

                        break;
                    }
                } catch (e) {
                    console.log('Backend重启按钮点击失败:', e.message);
                }
            }

            await page.screenshot({ path: 'dokploy-fix-04-after-backend.png' });

        } catch (error) {
            console.log('⚠️ 重启Backend时出错:', error.message);
            fixLog.errors.push(`重启Backend错误: ${error.message}`);
            fixLog.services.backend.status = 'failed';
        }

        // 修复步骤4: 检查服务日志
        console.log('📋 步骤4: 检查服务日志...');

        try {
            // 查找日志标签页
            const logsTab = await page.$('a:has-text("Logs"), button:has-text("Logs"), [role="tab"]:has-text("Logs"), a:has-text("日志")');
            if (logsTab) {
                console.log('打开日志标签页...');
                await logsTab.click();
                await page.waitForTimeout(5000);
                await page.screenshot({ path: 'dokploy-fix-05-logs.png', fullPage: true });

                // 提取日志内容
                const logContent = await page.evaluate(() => {
                    const logs = [];
                    const logElements = document.querySelectorAll('pre, code, [class*="log"], [class*="terminal"]');
                    logElements.forEach(el => {
                        const text = el.textContent;
                        if (text && text.trim().length > 0) {
                            logs.push(text.substring(0, 500));
                        }
                    });
                    return logs;
                });

                fixLog.logs = logContent;
                console.log(`提取了 ${logContent.length} 条日志`);
            }

        } catch (error) {
            console.log('⚠️ 检查日志时出错:', error.message);
            fixLog.errors.push(`日志检查错误: ${error.message}`);
        }

        // 最终验证
        console.log('🔍 步骤5: 最终验证...');

        try {
            // 等待所有服务稳定
            await page.waitForTimeout(20000);

            // 检查最终状态
            const finalStatus = await page.evaluate(() => {
                const status = {};

                // 查找所有服务的状态指示器
                const serviceElements = document.querySelectorAll('[class*="service"], [class*="container"], [data-service]');
                serviceElements.forEach(el => {
                    const serviceName = el.querySelector('[class*="name"], [class*="title"]')?.textContent;
                    const serviceStatus = el.querySelector('[class*="status"]')?.textContent;
                    if (serviceName && serviceStatus) {
                        status[serviceName.trim()] = serviceStatus.trim();
                    }
                });

                return status;
            });

            fixLog.finalStatus = finalStatus;
            console.log('最终状态:', finalStatus);

            await page.screenshot({ path: 'dokploy-fix-06-final.png' });

        } catch (error) {
            console.log('⚠️ 最终验证时出错:', error.message);
            fixLog.errors.push(`最终验证错误: ${error.message}`);
        }

        // 生成修复报告
        console.log('📋 生成修复报告...');

        const reportPath = 'dokploy-fix-report.json';
        fs.writeFileSync(reportPath, JSON.stringify(fixLog, null, 2));

        const readableReport = `
# Dokploy快速修复报告

## 修复时间
${fixLog.timestamp}

## 执行的步骤
${fixLog.steps.map((step, i) => `
${i + 1}. **${step.action}** ${step.service}: ${step.status}
`).join('')}

## 服务状态

### Redis服务
- 操作: ${fixLog.services.redis.action}
- 状态: ${fixLog.services.redis.status}

### Backend服务
- 操作: ${fixLog.services.backend.action}
- 状态: ${fixLog.services.backend.status}

### MySQL服务
- 操作: ${fixLog.services.mysql.action}
- 状态: ${fixLog.services.mysql.status}

## 最终状态
\`\`\`json
${JSON.stringify(fixLog.finalStatus, null, 2)}
\`\`\`

## 错误记录
${fixLog.errors.length > 0 ?
  fixLog.errors.map(err => `- ❌ ${err}`).join('\n') :
  '✅ 无错误'}

## 截图文件
1. 初始状态: dokploy-fix-01-initial.png
2. 停止服务后: dokploy-fix-02-after-stop.png
3. Redis重启后: dokploy-fix-03-after-redis.png
4. Backend重启后: dokploy-fix-04-after-backend.png
5. 服务日志: dokploy-fix-05-logs.png
6. 最终状态: dokploy-fix-06-final.png

## 建议后续操作
${fixLog.services.backend.status === 'healthy' && fixLog.services.redis.status === 'healthy' ?
  '✅ **修复成功！** 所有服务已恢复正常运行。' :
  '⚠️ **需要手动介入** - 部分服务仍存在问题，建议：' +
  (fixLog.services.backend.status !== 'healthy' ? '\n- 检查Backend服务日志' : '') +
  (fixLog.services.redis.status !== 'healthy' ? '\n- 检查Redis服务配置' : '') +
  '\n- 验证环境变量配置' +
  '\n- 检查Docker容器状态'}
`;

        fs.writeFileSync('dokploy-fix-report.md', readableReport);

        console.log('✅ 快速修复流程完成！');
        console.log('📊 报告已保存:');
        console.log(`   - JSON: ${reportPath}`);
        console.log(`   - Markdown: dokploy-fix-report.md`);
        console.log(`   - 截图: dokploy-fix-*.png`);

        // 显示修复摘要
        console.log('\n📋 修复摘要:');
        console.log(`Redis服务: ${fixLog.services.redis.status}`);
        console.log(`Backend服务: ${fixLog.services.backend.status}`);

        if (fixLog.errors.length > 0) {
            console.log('\n⚠️ 遇到的错误:');
            fixLog.errors.forEach(err => {
                console.log(`  - ${err}`);
            });
        }

        console.log('\n保持浏览器开启120秒供详细检查...');
        await page.waitForTimeout(120000);

    } catch (error) {
        console.error('❌ 修复过程中出现错误:', error);
        await page.screenshot({ path: 'dokploy-fix-error.png' });
    } finally {
        await browser.close();
    }
}

// 运行快速修复
console.log('🚀 启动Dokploy快速修复流程...');
quickFixDeployment().catch(console.error);