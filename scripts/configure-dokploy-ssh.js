#!/usr/bin/env node

/**
 * Dokploy SSH配置自动化脚本
 * 通过浏览器自动化登录Dokploy面板并添加SSH密钥
 */

const { chromium } = require('playbook');

// 配置信息
const DOKPLOY_URL = 'http://113.45.64.145:3000';
const EMAIL = '641600780@qq.com';
const PASSWORD = '353980swsgbo';
const SSH_PUBLIC_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPhpLCnOdDAksakqgydJAqd3vL0rHvJ7I2N/SE6wHgu5 AI_Agent_Key';

async function configureDokploySSH() {
    console.log('🚀 启动Dokploy SSH配置流程...');

    const browser = await chromium.launch({
        headless: false, // 显示浏览器窗口
        slowMo: 1000 // 慢速执行，便于观察
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    try {
        // 步骤1: 访问Dokploy登录页面
        console.log('📍 访问Dokploy登录页面...');
        await page.goto(DOKPLOY_URL);
        await page.waitForLoadState('networkidle');

        // 步骤2: 登录
        console.log('🔐 登录Dokploy账户...');
        await page.fill('input[type="email"], input[name="email"]', EMAIL);
        await page.fill('input[type="password"], input[name="password"]', PASSWORD);
        await page.click('button[type="submit"]');

        // 等待登录完成
        await page.waitForURL(/\/dashboard|\/projects/, { timeout: 10000 });
        console.log('✅ 登录成功');

        // 步骤3: 导航到SSH Keys设置
        console.log('⚙️ 导航到SSH Keys设置...');
        await page.click('a[href="/settings"], button:has-text("Settings")');
        await page.waitForLoadState('networkidle');

        await page.click('a[href="/settings/ssh-keys"], button:has-text("SSH Keys")');
        await page.waitForLoadState('networkidle');

        // 步骤4: 添加SSH密钥
        console.log('➕ 添加新的SSH密钥...');
        const addButton = await page.$('button:has-text("Add"), button:has-text("添加"), button:has-text("New")');
        if (addButton) {
            await addButton.click();
            await page.waitForTimeout(1000);

            // 填写SSH密钥信息
            await page.fill('input[name="name"], input[placeholder*="name"]', 'AI_Agent_Deployment_Key');
            await page.fill('textarea[name="key"], textarea[placeholder*="key"]', SSH_PUBLIC_KEY);

            // 提交表单
            await page.click('button[type="submit"]:has-text("Add"), button:has-text("Save"), button:has-text("创建")');
            console.log('✅ SSH密钥添加成功');
        } else {
            console.log('⚠️ 未找到添加按钮，可能需要手动操作');
        }

        // 步骤5: 验证SSH密钥是否添加成功
        console.log('🔍 验证SSH密钥...');
        await page.waitForTimeout(2000);
        const keyExists = await page.textContent('body').then(text =>
            text.includes('AI_Agent_Deployment_Key') || text.includes(SSH_PUBLIC_KEY.substring(0, 20))
        );

        if (keyExists) {
            console.log('✅ SSH密钥验证成功');
        } else {
            console.log('⚠️ 无法确认SSH密钥是否添加成功');
        }

        // 保持浏览器打开一段时间供确认
        console.log('⏳ 保持浏览器打开30秒供确认...');
        await page.waitForTimeout(30000);

    } catch (error) {
        console.error('❌ 配置过程出错:', error.message);
    } finally {
        await browser.close();
        console.log('🏁 配置流程完成');
    }
}

// 执行配置
configureDokploySSH().catch(console.error);