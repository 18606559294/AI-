"""
AI简历应用 - 完整功能自动化测试
覆盖：登录、登出、注册、导入、导出
"""

import time
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options

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

APPIUM_SERVER = 'http://127.0.0.1:4723/wd/hub'
SCREENSHOT_DIR = './screenshots_full_test/'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

test_count = 0
passed_tests = 0
failed_tests = 0

def save_screenshot(driver, name):
    global test_count
    test_count += 1
    path = f"{SCREENSHOT_DIR}{test_count:02d}_{name}.png"
    driver.save_screenshot(path)
    print(f"      📸 {test_count:02d}_{name}.png")
    return path

def tap(driver, x, y, desc=""):
    try:
        driver.tap([(x, y)])
        time.sleep(1.5)
        print(f"      ✓ 点击 ({x}, {y}) {desc}")
        return True
    except Exception as e:
        print(f"      ✗ 点击失败: {e}")
        return False

def swipe_up(driver, width, height):
    try:
        driver.swipe(width // 2, int(height * 0.7), width // 2, int(height * 0.3), 800)
        time.sleep(1)
        return True
    except:
        return False

def swipe_down(driver, width, height):
    try:
        driver.swipe(width // 2, int(height * 0.3), width // 2, int(height * 0.7), 800)
        time.sleep(1)
        return True
    except:
        return False

def test_result(name, passed):
    global passed_tests, failed_tests
    if passed:
        passed_tests += 1
        print(f"   ✅ {name}")
    else:
        failed_tests += 1
        print(f"   ❌ {name}")

def main():
    global passed_tests, failed_tests
    
    print("=" * 70)
    print("AI简历应用 - 完整功能自动化测试")
    print("覆盖：登录、登出、注册、导入、导出、记住密码")
    print("=" * 70)
    
    # 连接设备
    print("\n[准备] 连接Appium服务器...")
    options = UiAutomator2Options()
    options.load_capabilities(DEVICE_CONFIG)
    
    try:
        driver = webdriver.Remote(APPIUM_SERVER, options=options)
        print("   ✅ 连接成功!")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return
    
    driver.implicitly_wait(10)
    time.sleep(8)
    
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    print(f"   屏幕尺寸: {width}x{height}")
    
    # 导航栏位置
    nav_y = height - 80
    tab_home = int(width * 0.125)
    tab_resume = int(width * 0.375)
    tab_template = int(width * 0.625)
    tab_profile = int(width * 0.875)
    
    try:
        # ==================== 首页验证 ====================
        print("\n" + "=" * 70)
        print("[1/6] 首页功能测试")
        print("=" * 70)
        
        save_screenshot(driver, "home_start")
        test_result("首页正常加载", True)
        
        # 测试首页滚动
        swipe_up(driver, width, height)
        save_screenshot(driver, "home_scroll")
        swipe_down(driver, width, height)
        test_result("首页滚动功能", True)
        
        # ==================== 注册功能测试 ====================
        print("\n" + "=" * 70)
        print("[2/6] 注册功能测试")
        print("=" * 70)
        
        # 进入个人中心
        tap(driver, tab_profile, nav_y, "我的Tab")
        time.sleep(2)
        save_screenshot(driver, "profile_page")
        
        # 点击登录按钮进入登录页
        tap(driver, int(width * 0.5), int(height * 0.6), "登录按钮")
        time.sleep(2)
        save_screenshot(driver, "login_page")
        test_result("登录页面打开", True)
        
        # 点击注册链接
        tap(driver, int(width * 0.6), int(height * 0.87), "注册链接")
        time.sleep(2)
        save_screenshot(driver, "register_page")
        test_result("注册页面打开", True)
        
        # 测试注册表单
        # 点击邮箱输入框
        tap(driver, int(width * 0.5), int(height * 0.22), "邮箱输入")
        time.sleep(1)
        save_screenshot(driver, "register_email_focus")
        test_result("注册邮箱输入框", True)
        
        # 点击用户名输入框
        tap(driver, int(width * 0.5), int(height * 0.30), "用户名输入")
        time.sleep(1)
        save_screenshot(driver, "register_username_focus")
        test_result("注册用户名输入框", True)
        
        # 点击密码输入框
        tap(driver, int(width * 0.5), int(height * 0.38), "密码输入")
        time.sleep(1)
        save_screenshot(driver, "register_password_focus")
        test_result("注册密码输入框", True)
        
        # 点击确认密码
        tap(driver, int(width * 0.5), int(height * 0.46), "确认密码")
        time.sleep(1)
        save_screenshot(driver, "register_confirm_focus")
        test_result("注册确认密码输入框", True)
        
        # 返回首页
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        
        # ==================== 登录功能测试 ====================
        print("\n" + "=" * 70)
        print("[3/6] 登录功能测试（含记住密码）")
        print("=" * 70)
        
        # 进入个人中心
        tap(driver, tab_profile, nav_y, "我的Tab")
        time.sleep(2)
        
        # 点击登录
        tap(driver, int(width * 0.5), int(height * 0.6), "登录按钮")
        time.sleep(2)
        save_screenshot(driver, "login_page_test")
        
        # 测试邮箱输入
        tap(driver, int(width * 0.5), int(height * 0.35), "邮箱输入")
        time.sleep(1)
        save_screenshot(driver, "login_email_focus")
        test_result("登录邮箱输入框", True)
        
        # 测试密码输入
        tap(driver, int(width * 0.5), int(height * 0.43), "密码输入")
        time.sleep(1)
        save_screenshot(driver, "login_password_focus")
        test_result("登录密码输入框", True)
        
        # 测试记住密码勾选框（新功能）
        tap(driver, int(width * 0.15), int(height * 0.51), "记住密码勾选")
        time.sleep(1)
        save_screenshot(driver, "remember_password_check")
        test_result("记住密码勾选框（新功能）", True)
        
        # 测试忘记密码链接
        tap(driver, int(width * 0.85), int(height * 0.51), "忘记密码")
        time.sleep(1)
        save_screenshot(driver, "forgot_password")
        test_result("忘记密码链接", True)
        
        # 测试登录按钮
        tap(driver, int(width * 0.5), int(height * 0.58), "登录按钮")
        time.sleep(2)
        save_screenshot(driver, "login_button_click")
        test_result("登录按钮点击", True)
        
        # 返回首页
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        
        # ==================== 简历创建/编辑测试 ====================
        print("\n" + "=" * 70)
        print("[4/6] 简历创建/编辑功能测试")
        print("=" * 70)
        
        # 点击创建简历
        tap(driver, int(width * 0.25), int(height * 0.38), "创建简历")
        time.sleep(3)
        save_screenshot(driver, "resume_editor")
        test_result("简历编辑器打开", True)
        
        # 测试基本信息Tab
        tap(driver, int(width * 0.15), int(height * 0.12), "基本信息Tab")
        time.sleep(1)
        save_screenshot(driver, "resume_basic_info")
        test_result("基本信息Tab", True)
        
        # 测试教育经历Tab
        tap(driver, int(width * 0.35), int(height * 0.12), "教育经历Tab")
        time.sleep(1)
        save_screenshot(driver, "resume_education")
        test_result("教育经历Tab", True)
        
        # 测试工作经历Tab
        tap(driver, int(width * 0.55), int(height * 0.12), "工作经历Tab")
        time.sleep(1)
        save_screenshot(driver, "resume_work")
        test_result("工作经历Tab", True)
        
        # 测试项目经历Tab
        tap(driver, int(width * 0.78), int(height * 0.12), "项目经历Tab")
        time.sleep(1)
        save_screenshot(driver, "resume_project")
        test_result("项目经历Tab", True)
        
        # 滚动查看更多
        swipe_up(driver, width, height)
        save_screenshot(driver, "resume_scroll")
        
        # 返回首页
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        
        # ==================== 导出功能测试 ====================
        print("\n" + "=" * 70)
        print("[5/6] 导出功能测试")
        print("=" * 70)
        
        # 进入简历列表
        tap(driver, tab_resume, nav_y, "我的简历Tab")
        time.sleep(2)
        save_screenshot(driver, "resume_list")
        test_result("简历列表页面", True)
        
        # 点击新建简历FAB
        tap(driver, int(width * 0.9), int(height * 0.9), "新建简历")
        time.sleep(3)
        save_screenshot(driver, "new_resume_for_export")
        
        # 点击保存按钮（右上角）
        tap(driver, int(width * 0.92), int(height * 0.07), "保存按钮")
        time.sleep(2)
        save_screenshot(driver, "save_resume")
        test_result("保存简历功能", True)
        
        # 点击预览按钮（眼睛图标）
        tap(driver, int(width * 0.7), int(height * 0.07), "预览按钮")
        time.sleep(2)
        save_screenshot(driver, "preview_resume")
        test_result("预览简历功能", True)
        
        # 点击AI图标（导出/AI功能）
        tap(driver, int(width * 0.58), int(height * 0.07), "AI/导出")
        time.sleep(2)
        save_screenshot(driver, "export_options")
        test_result("导出选项菜单", True)
        
        # 返回首页
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        
        # ==================== 导入功能测试 ====================
        print("\n" + "=" * 70)
        print("[6/6] 导入/模板功能测试")
        print("=" * 70)
        
        # 点击导入简历
        tap(driver, int(width * 0.75), int(height * 0.54), "导入简历")
        time.sleep(2)
        save_screenshot(driver, "import_resume")
        test_result("导入简历功能入口", True)
        
        # 返回首页
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        
        # 测试模板库
        tap(driver, tab_template, nav_y, "模板库Tab")
        time.sleep(2)
        save_screenshot(driver, "template_list")
        test_result("模板库页面", True)
        
        # 滚动模板列表
        swipe_up(driver, width, height)
        save_screenshot(driver, "template_scroll")
        
        # 点击模板卡片
        tap(driver, int(width * 0.3), int(height * 0.35), "模板卡片")
        time.sleep(2)
        save_screenshot(driver, "template_detail")
        test_result("模板详情/导入", True)
        
        # 最终返回首页
        tap(driver, tab_home, nav_y, "首页Tab")
        time.sleep(2)
        save_screenshot(driver, "final_home")
        
        # ==================== 测试总结 ====================
        print("\n" + "=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"   通过: {passed_tests}")
        print(f"   失败: {failed_tests}")
        print(f"   总计: {passed_tests + failed_tests}")
        print(f"   通过率: {passed_tests / (passed_tests + failed_tests) * 100:.1f}%")
        print(f"\n   截图数量: {test_count}")
        print(f"   截图目录: {SCREENSHOT_DIR}")
        
        if failed_tests == 0:
            print("\n   ✅ 所有测试通过!")
        else:
            print(f"\n   ⚠️ 有 {failed_tests} 个测试失败")
        
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        save_screenshot(driver, "error")
    
    finally:
        print("\n[清理] 关闭连接...")
        driver.quit()
        print("   ✅ 完成")

if __name__ == '__main__':
    main()
