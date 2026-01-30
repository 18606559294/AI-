"""
稳定版验证测试 - 确认Appium能正确控制APP的所有功能
"""

import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设备配置
DEVICE_CONFIG = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'c8025d3c',
    'appPackage': 'com.example.ai_resume_app',
    'appActivity': '.MainActivity',
    'noReset': False,
    'forceAppLaunch': True,
    'newCommandTimeout': 600,
    'autoGrantPermissions': True,
    'uiautomator2ServerInstallTimeout': 120000,
    'uiautomator2ServerLaunchTimeout': 120000,
    'adbExecTimeout': 120000,
    'skipServerInstallation': False,
}

APPIUM_SERVER = 'http://127.0.0.1:4723'
SCREENSHOT_DIR = './screenshots_verify/'

import os
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def save_screenshot(driver, name):
    path = f"{SCREENSHOT_DIR}{name}.png"
    driver.save_screenshot(path)
    print(f"   📸 截图: {name}.png")
    return path

def safe_tap(driver, x, y, name=""):
    """安全的点击操作"""
    try:
        driver.tap([(x, y)])
        time.sleep(1.5)
        print(f"   ✓ 点击 ({x}, {y}) {name}")
        return True
    except Exception as e:
        print(f"   ✗ 点击失败: {e}")
        return False

def safe_swipe(driver, start_x, start_y, end_x, end_y, duration=800):
    """安全的滑动操作"""
    try:
        driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(1)
        print(f"   ✓ 滑动完成")
        return True
    except Exception as e:
        print(f"   ✗ 滑动失败: {e}")
        return False

def main():
    print("=" * 60)
    print("AI简历应用 - 完整功能验证测试")
    print("=" * 60)
    
    print("\n[步骤1] 连接Appium服务器...")
    
    options = UiAutomator2Options()
    options.load_capabilities(DEVICE_CONFIG)
    
    try:
        driver = webdriver.Remote(APPIUM_SERVER, options=options)
        print("   ✅ 连接成功!")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return
    
    driver.implicitly_wait(15)
    
    print("\n[步骤2] 等待应用完全启动...")
    time.sleep(8)
    
    # 获取屏幕信息
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    print(f"   屏幕尺寸: {width}x{height}")
    
    # 计算导航栏位置
    nav_y = height - 80  # 底部导航栏
    home_x = int(width * 0.125)
    resume_x = int(width * 0.375)
    template_x = int(width * 0.625)
    profile_x = int(width * 0.875)
    
    try:
        # ============ 测试登录页面 ============
        print("\n[步骤3] 测试登录页面...")
        save_screenshot(driver, "01_app_started")
        
        # 检查当前页面
        current_activity = driver.current_activity
        print(f"   当前Activity: {current_activity}")
        
        # 点击返回，回到主页（如果在登录页面）
        print("\n[步骤4] 返回主页...")
        driver.back()
        time.sleep(2)
        save_screenshot(driver, "02_after_back")
        
        # ============ 测试底部导航 ============
        print("\n[步骤5] 测试底部导航 - 首页...")
        safe_tap(driver, home_x, nav_y, "首页")
        time.sleep(2)
        save_screenshot(driver, "03_home_tab")
        
        print("\n[步骤6] 测试底部导航 - 简历...")
        safe_tap(driver, resume_x, nav_y, "简历")
        time.sleep(2)
        save_screenshot(driver, "04_resume_tab")
        
        print("\n[步骤7] 测试底部导航 - 模板...")
        safe_tap(driver, template_x, nav_y, "模板")
        time.sleep(2)
        save_screenshot(driver, "05_template_tab")
        
        print("\n[步骤8] 测试底部导航 - 我的...")
        safe_tap(driver, profile_x, nav_y, "我的")
        time.sleep(2)
        save_screenshot(driver, "06_profile_tab")
        
        # ============ 测试个人中心功能 ============
        print("\n[步骤9] 在个人中心点击登录...")
        # 点击登录按钮区域
        safe_tap(driver, width // 2, int(height * 0.45), "登录按钮")
        time.sleep(2)
        save_screenshot(driver, "07_login_clicked")
        
        # ============ 测试登录页面交互 ============
        print("\n[步骤10] 测试登录页面...")
        # 点击邮箱输入框
        safe_tap(driver, width // 2, int(height * 0.35), "邮箱输入框")
        time.sleep(1)
        save_screenshot(driver, "08_email_field")
        
        # 返回
        driver.back()
        time.sleep(1)
        
        # 点击注册链接
        print("\n[步骤11] 点击注册链接...")
        safe_tap(driver, int(width * 0.6), int(height * 0.88), "注册链接")
        time.sleep(2)
        save_screenshot(driver, "09_register_page")
        
        # 返回登录页
        driver.back()
        time.sleep(1)
        
        # 返回个人中心
        driver.back()
        time.sleep(1)
        save_screenshot(driver, "10_back_to_profile")
        
        # ============ 测试简历列表 ============
        print("\n[步骤12] 测试简历列表...")
        safe_tap(driver, resume_x, nav_y, "简历Tab")
        time.sleep(2)
        save_screenshot(driver, "11_resume_list")
        
        # 点击新建简历按钮（右下角FAB）
        print("\n[步骤13] 点击新建简历...")
        safe_tap(driver, int(width * 0.85), int(height * 0.88), "新建简历")
        time.sleep(3)
        save_screenshot(driver, "12_new_resume")
        
        # 返回
        driver.back()
        time.sleep(1)
        
        # ============ 测试模板库 ============
        print("\n[步骤14] 测试模板库...")
        safe_tap(driver, template_x, nav_y, "模板Tab")
        time.sleep(2)
        save_screenshot(driver, "13_template_list")
        
        # 点击一个模板
        print("\n[步骤15] 点击模板卡片...")
        safe_tap(driver, int(width * 0.25), int(height * 0.35), "模板卡片")
        time.sleep(2)
        save_screenshot(driver, "14_template_detail")
        
        # 返回
        driver.back()
        time.sleep(1)
        
        # ============ 测试滑动 ============
        print("\n[步骤16] 测试滚动操作...")
        safe_swipe(driver, width // 2, int(height * 0.7), width // 2, int(height * 0.3))
        time.sleep(1)
        save_screenshot(driver, "15_scrolled_down")
        
        safe_swipe(driver, width // 2, int(height * 0.3), width // 2, int(height * 0.7))
        time.sleep(1)
        save_screenshot(driver, "16_scrolled_up")
        
        # ============ 最终状态 ============
        print("\n[步骤17] 回到首页...")
        safe_tap(driver, home_x, nav_y, "首页")
        time.sleep(2)
        save_screenshot(driver, "17_final_home")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        try:
            save_screenshot(driver, "error_state")
        except:
            pass
    
    finally:
        print("\n[清理] 关闭连接...")
        try:
            driver.quit()
            print("   ✅ 连接已关闭")
        except:
            pass
    
    print(f"\n📁 所有截图保存在: {SCREENSHOT_DIR}")
    print("请检查截图确认测试是否正确执行!")

if __name__ == '__main__':
    main()
