"""
AI简历应用 - 真实功能测试（不使用返回键）
"""

import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import os

# 设备配置
DEVICE_CONFIG = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'EYFBB22923201473',
    'appPackage': 'com.example.ai_resume_app',
    'appActivity': '.MainActivity',
    'noReset': False,
    'forceAppLaunch': True,
    'newCommandTimeout': 600,
    'autoGrantPermissions': True,
    'uiautomator2ServerInstallTimeout': 120000,
}

APPIUM_SERVER = 'http://127.0.0.1:4723'
SCREENSHOT_DIR = './screenshots_real/'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

test_count = 0

def save_screenshot(driver, name):
    global test_count
    test_count += 1
    path = f"{SCREENSHOT_DIR}{test_count:02d}_{name}.png"
    driver.save_screenshot(path)
    print(f"   📸 {test_count:02d}_{name}.png")
    return path

def tap(driver, x, y, desc=""):
    """点击操作"""
    try:
        driver.tap([(x, y)])
        time.sleep(1.5)
        print(f"   ✅ 点击 ({x}, {y}) {desc}")
        return True
    except Exception as e:
        print(f"   ❌ 点击失败: {e}")
        return False

def swipe_up(driver, width, height):
    """向上滑动"""
    try:
        driver.swipe(width // 2, int(height * 0.7), width // 2, int(height * 0.3), 800)
        time.sleep(1)
        print(f"   ✅ 向上滑动")
        return True
    except:
        return False

def swipe_down(driver, width, height):
    """向下滑动"""
    try:
        driver.swipe(width // 2, int(height * 0.3), width // 2, int(height * 0.7), 800)
        time.sleep(1)
        print(f"   ✅ 向下滑动")
        return True
    except:
        return False

def main():
    print("=" * 60)
    print("AI简历应用 - 完整功能测试")
    print("=" * 60)
    
    print("\n[1] 连接设备...")
    options = UiAutomator2Options()
    options.load_capabilities(DEVICE_CONFIG)
    
    try:
        driver = webdriver.Remote(APPIUM_SERVER, options=options)
        print("   ✅ 连接成功!")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return
    
    driver.implicitly_wait(10)
    
    print("\n[2] 等待应用启动...")
    time.sleep(8)
    
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    print(f"   屏幕尺寸: {width}x{height}")
    
    # 底部导航栏位置 (4个Tab)
    nav_y = height - 80
    tab_home = int(width * 0.125)
    tab_resume = int(width * 0.375)
    tab_template = int(width * 0.625)
    tab_profile = int(width * 0.875)
    
    try:
        # ===== 首页测试 =====
        print("\n[3] 测试首页...")
        save_screenshot(driver, "home_start")
        
        # 向下滑动查看更多内容
        print("   滚动首页内容...")
        swipe_up(driver, width, height)
        save_screenshot(driver, "home_scroll1")
        
        swipe_up(driver, width, height)
        save_screenshot(driver, "home_scroll2")
        
        swipe_down(driver, width, height)
        save_screenshot(driver, "home_scroll_back")
        
        # 点击首页的"创建简历"卡片
        print("\n[4] 点击创建简历卡片...")
        tap(driver, int(width * 0.25), int(height * 0.38), "创建简历")
        time.sleep(2)
        save_screenshot(driver, "create_resume_click")
        
        # 点击首页Tab返回
        tap(driver, tab_home, nav_y, "首页Tab")
        save_screenshot(driver, "back_home_1")
        
        # 点击"AI一键生成"卡片
        print("\n[5] 点击AI一键生成...")
        tap(driver, int(width * 0.75), int(height * 0.38), "AI一键生成")
        time.sleep(2)
        save_screenshot(driver, "ai_generate_click")
        
        # 点击首页Tab返回
        tap(driver, tab_home, nav_y, "首页Tab")
        save_screenshot(driver, "back_home_2")
        
        # 点击"选择模板"卡片
        print("\n[6] 点击选择模板...")
        tap(driver, int(width * 0.25), int(height * 0.54), "选择模板")
        time.sleep(2)
        save_screenshot(driver, "select_template_click")
        
        # 点击首页Tab返回
        tap(driver, tab_home, nav_y, "首页Tab")
        save_screenshot(driver, "back_home_3")
        
        # 点击"导入简历"卡片
        print("\n[7] 点击导入简历...")
        tap(driver, int(width * 0.75), int(height * 0.54), "导入简历")
        time.sleep(2)
        save_screenshot(driver, "import_resume_click")
        
        # 点击首页Tab返回
        tap(driver, tab_home, nav_y, "首页Tab")
        save_screenshot(driver, "back_home_4")
        
        # ===== 我的简历测试 =====
        print("\n[8] 测试我的简历页面...")
        tap(driver, tab_resume, nav_y, "我的简历Tab")
        time.sleep(2)
        save_screenshot(driver, "resume_list")
        
        # 点击新建简历FAB按钮
        print("   点击新建简历按钮...")
        tap(driver, int(width * 0.9), int(height * 0.9), "新建简历FAB")
        time.sleep(2)
        save_screenshot(driver, "new_resume_fab")
        
        # 返回简历列表
        tap(driver, tab_resume, nav_y, "我的简历Tab")
        save_screenshot(driver, "resume_list_2")
        
        # ===== 模板库测试 =====
        print("\n[9] 测试模板库页面...")
        tap(driver, tab_template, nav_y, "模板库Tab")
        time.sleep(2)
        save_screenshot(driver, "template_list")
        
        # 滚动模板列表
        swipe_up(driver, width, height)
        save_screenshot(driver, "template_scroll1")
        
        swipe_up(driver, width, height)
        save_screenshot(driver, "template_scroll2")
        
        swipe_down(driver, width, height)
        save_screenshot(driver, "template_scroll_back")
        
        # 点击第一个模板卡片
        print("   点击模板卡片...")
        tap(driver, int(width * 0.3), int(height * 0.35), "模板卡片1")
        time.sleep(2)
        save_screenshot(driver, "template_detail")
        
        # 返回模板列表
        tap(driver, tab_template, nav_y, "模板库Tab")
        save_screenshot(driver, "template_list_back")
        
        # 点击第二个模板
        tap(driver, int(width * 0.7), int(height * 0.35), "模板卡片2")
        time.sleep(2)
        save_screenshot(driver, "template_detail_2")
        
        # 返回模板列表
        tap(driver, tab_template, nav_y, "模板库Tab")
        
        # ===== 我的页面测试 =====
        print("\n[10] 测试我的页面...")
        tap(driver, tab_profile, nav_y, "我的Tab")
        time.sleep(2)
        save_screenshot(driver, "profile_page")
        
        # 点击登录按钮
        print("   点击登录按钮...")
        tap(driver, int(width * 0.5), int(height * 0.6), "登录按钮")
        time.sleep(2)
        save_screenshot(driver, "login_page")
        
        # 在登录页面点击邮箱输入框
        print("   点击邮箱输入框...")
        tap(driver, int(width * 0.5), int(height * 0.35), "邮箱输入框")
        time.sleep(1)
        save_screenshot(driver, "login_email_focus")
        
        # 点击密码输入框
        print("   点击密码输入框...")
        tap(driver, int(width * 0.5), int(height * 0.43), "密码输入框")
        time.sleep(1)
        save_screenshot(driver, "login_password_focus")
        
        # 点击注册链接
        print("   点击注册链接...")
        tap(driver, int(width * 0.6), int(height * 0.87), "注册链接")
        time.sleep(2)
        save_screenshot(driver, "register_page")
        
        # 在注册页面填写信息
        print("   注册页面...")
        tap(driver, int(width * 0.5), int(height * 0.25), "邮箱输入")
        time.sleep(1)
        save_screenshot(driver, "register_email")
        
        tap(driver, int(width * 0.5), int(height * 0.33), "用户名输入")
        time.sleep(1)
        save_screenshot(driver, "register_username")
        
        # 返回首页
        print("\n[11] 返回首页完成测试...")
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        save_screenshot(driver, "final_home")
        
        print("\n" + "=" * 60)
        print(f"✅ 测试完成! 共截取 {test_count} 张截图")
        print(f"📁 截图保存在: {SCREENSHOT_DIR}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        save_screenshot(driver, "error")
    
    finally:
        print("\n[清理] 关闭连接...")
        driver.quit()
        print("   ✅ 完成")

if __name__ == '__main__':
    main()
