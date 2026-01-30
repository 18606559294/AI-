"""
简单验证测试 - 确认Appium能正确启动和控制APP
"""

import time
from appium import webdriver
from appium.options.android import UiAutomator2Options

# 设备配置
DEVICE_CONFIG = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'c8025d3c',
    'appPackage': 'com.example.ai_resume_app',
    'appActivity': '.MainActivity',
    'noReset': False,
    'forceAppLaunch': True,
    'shouldTerminateApp': True,
    'newCommandTimeout': 300,
    'autoGrantPermissions': True,
}

APPIUM_SERVER = 'http://127.0.0.1:4723'

def main():
    print("=" * 60)
    print("Appium 验证测试 - AI简历应用")
    print("=" * 60)
    
    print("\n1. 正在连接Appium服务器...")
    
    options = UiAutomator2Options()
    options.load_capabilities(DEVICE_CONFIG)
    
    try:
        driver = webdriver.Remote(APPIUM_SERVER, options=options)
        print("   ✅ 连接成功!")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return
    
    driver.implicitly_wait(10)
    
    print("\n2. 等待应用启动...")
    time.sleep(5)
    
    print("\n3. 检查应用状态...")
    try:
        # 获取当前Activity
        current_activity = driver.current_activity
        print(f"   当前Activity: {current_activity}")
        
        # 获取当前包名
        current_package = driver.current_package
        print(f"   当前包名: {current_package}")
        
        # 获取屏幕尺寸
        size = driver.get_window_size()
        print(f"   屏幕尺寸: {size['width']}x{size['height']}")
        
        # 检查页面源
        page_source = driver.page_source
        print(f"   页面源长度: {len(page_source)} 字符")
        
    except Exception as e:
        print(f"   ❌ 获取状态失败: {e}")
    
    print("\n4. 执行简单交互测试...")
    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 截图
        driver.save_screenshot('verify_screenshot_1.png')
        print("   📸 截图1已保存: verify_screenshot_1.png")
        
        # 点击屏幕中央
        print("   点击屏幕中央...")
        driver.tap([(width // 2, height // 2)])
        time.sleep(2)
        
        driver.save_screenshot('verify_screenshot_2.png')
        print("   📸 截图2已保存: verify_screenshot_2.png")
        
        # 执行滑动
        print("   执行向上滑动...")
        driver.swipe(width // 2, int(height * 0.7), width // 2, int(height * 0.3), 800)
        time.sleep(2)
        
        driver.save_screenshot('verify_screenshot_3.png')
        print("   📸 截图3已保存: verify_screenshot_3.png")
        
        # 点击底部导航
        print("   点击底部导航栏...")
        nav_y = height - 50
        
        # 点击简历Tab
        driver.tap([(int(width * 0.4), nav_y)])
        time.sleep(2)
        driver.save_screenshot('verify_screenshot_4_resume.png')
        print("   📸 截图4已保存: verify_screenshot_4_resume.png")
        
        # 点击模板Tab
        driver.tap([(int(width * 0.6), nav_y)])
        time.sleep(2)
        driver.save_screenshot('verify_screenshot_5_template.png')
        print("   📸 截图5已保存: verify_screenshot_5_template.png")
        
        # 点击我的Tab
        driver.tap([(int(width * 0.8), nav_y)])
        time.sleep(2)
        driver.save_screenshot('verify_screenshot_6_profile.png')
        print("   📸 截图6已保存: verify_screenshot_6_profile.png")
        
        print("   ✅ 交互测试完成!")
        
    except Exception as e:
        print(f"   ❌ 交互测试失败: {e}")
    
    print("\n5. 关闭连接...")
    driver.quit()
    print("   ✅ 测试完成!")
    
    print("\n" + "=" * 60)
    print("请检查手机屏幕，确认APP是否有响应")
    print("截图已保存到当前目录")
    print("=" * 60)

if __name__ == '__main__':
    main()
