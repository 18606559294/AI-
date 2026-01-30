// Appium跨平台测试示例
// 使用JavaScript编写，也支持Java、Python等语言

const wd = require('webdriverio');

const opts = {
    hostname: 'localhost',
    port: 4723,
    path: '/wd/hub',
    capabilities: {
        platformName: 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'Android Emulator',
        'appium:app': '/path/to/your/app/build/app/outputs/flutter-apk/app-debug.apk',
        'appium:appPackage': 'com.example.ai_resume_app',
        'appium:appActivity': '.MainActivity',
        'appium:noReset': true,
        'appium:unicodeKeyboard': true,
        'appium:resetKeyboard': true,
    }
};

async function main() {
    const client = await wd.remote(opts);

    try {
        // 测试应用启动
        console.log('测试应用启动...');
        await client.pause(3000);

        // 示例：查找并点击按钮
        /*
        const button = await client.$('id=com.example.ai_resume_app:id/button_id');
        await button.click();
        */

        // 示例：输入文本
        /*
        const inputField = await client.$('id=com.example.ai_resume_app:id/input_field');
        await inputField.setValue('测试内容');
        */

        // 示例：滑动操作
        /*
        await client.touchAction([
            { action: 'press', x: 500, y: 1500 },
            { action: 'moveTo', x: 500, y: 500 },
            'release'
        ]);
        */

        // 示例：验证文本
        /*
        const resultText = await client.$('id=com.example.ai_resume_app:id/result_text');
        const text = await resultText.getText();
        console.log('结果文本:', text);
        */

        console.log('测试完成！');
    } catch (error) {
        console.error('测试失败:', error);
    } finally {
        await client.deleteSession();
    }
}

main();

/*
// 安装Appium和依赖
// npm install webdriverio appium

// 运行测试
// node appium_test_example.js

// 支持的更多操作：
// 1. 截图：await client.saveScreenshot('screenshot.png');
// 2. 获取页面源：const source = await client.getPageSource();
// 3. 等待元素：await client.$('selector').waitForExist(5000);
// 4. 滚动：await client.touchPerform([...]);
// 5. 长按：await client.touchAction([{ action: 'longPress', x: 500, y: 500 }, 'release']);
// 6. 多点触控：await client.multiTouchPerform([...]);
*/