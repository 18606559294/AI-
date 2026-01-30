"""
Appium测试配置文件
AI简历应用全面自动化测试
"""

import pytest
import os
import time
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 设备配置
DEVICE_CONFIG = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'EYFBB22923201473',
    'appPackage': 'com.example.ai_resume_app',
    'appActivity': '.MainActivity',
    'noReset': False,
    'fullReset': False,
    'forceAppLaunch': True,
    'shouldTerminateApp': True,
    'newCommandTimeout': 300,
    'autoGrantPermissions': True,
    'uiautomator2ServerInstallTimeout': 60000,
    'adbExecTimeout': 60000,
}

# Appium服务器配置
APPIUM_SERVER = 'http://127.0.0.1:4723/wd/hub'

# 截图目录
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


class AppDriver:
    """应用驱动封装类"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    def find_element(self, by, value, timeout=15):
        """查找元素"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by, value, timeout=15):
        """查找多个元素"""
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.presence_of_element_located((by, value)))
            return self.driver.find_elements(by, value)
        except:
            return []
    
    def click_element(self, by, value, timeout=15):
        """点击元素"""
        element = self.find_element(by, value, timeout)
        element.click()
        return element
    
    def input_text(self, by, value, text, timeout=15):
        """输入文本"""
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)
        return element
    
    def is_element_present(self, by, value, timeout=5):
        """检查元素是否存在"""
        try:
            self.find_element(by, value, timeout)
            return True
        except:
            return False
    
    def get_text(self, by, value, timeout=15):
        """获取元素文本"""
        element = self.find_element(by, value, timeout)
        return element.text
    
    def swipe_up(self):
        """向上滑动"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)
    
    def swipe_down(self):
        """向下滑动"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.2)
        end_y = int(size['height'] * 0.8)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)
    
    def screenshot(self, name):
        """截图"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        print(f"📸 截图已保存: {filepath}")
        return filepath
    
    def back(self):
        """返回"""
        self.driver.back()
    
    def tap(self, x, y):
        """点击坐标"""
        self.driver.tap([(x, y)])


@pytest.fixture(scope='session')
def driver():
    """创建Appium驱动"""
    options = UiAutomator2Options()
    options.load_capabilities(DEVICE_CONFIG)
    
    print("\n🚀 正在连接Appium服务器...")
    driver = webdriver.Remote(APPIUM_SERVER, options=options)
    driver.implicitly_wait(10)
    
    print("✅ 连接成功，开始测试")
    
    yield driver
    
    print("\n🔚 测试完成，关闭连接")
    driver.quit()


@pytest.fixture
def app(driver):
    """创建AppDriver实例"""
    return AppDriver(driver)


@pytest.fixture(autouse=True)
def test_setup_teardown(request, app):
    """测试前后处理"""
    test_name = request.node.name
    print(f"\n{'='*50}")
    print(f"🧪 开始测试: {test_name}")
    print(f"{'='*50}")
    
    yield
    
    # 测试失败时截图
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        app.screenshot(f"failed_{test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """记录测试结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
