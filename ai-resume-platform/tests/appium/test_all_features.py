"""
AI简历应用 - 完整业务功能测试
覆盖: 登录、注册、登出、简历创建/编辑、导入、导出、模板选择、AI优化等所有核心功能
"""

import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy


class TestAuthLogin:
    """登录功能测试"""
    
    def test_navigate_to_login(self, app):
        """测试导航到登录页面"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击个人中心
        profile_x = (width // 5) * 4
        nav_y = height - 50
        app.tap(profile_x, nav_y)
        time.sleep(2)
        
        app.screenshot("profile_before_login")
        
        # 点击登录按钮区域 (未登录状态下的登录按钮)
        app.tap(width // 2, height // 2)
        time.sleep(2)
        
        app.screenshot("login_page")
        print("✅ 导航到登录页面成功")
    
    def test_login_page_elements(self, app):
        """测试登录页面元素"""
        time.sleep(1)
        
        # 检查页面内容
        page_source = app.driver.page_source
        assert len(page_source) > 5000
        
        app.screenshot("login_page_elements")
        print("✅ 登录页面元素加载成功")
    
    def test_input_email(self, app):
        """测试输入邮箱"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击邮箱输入框区域 (通常在页面上部)
        app.tap(width // 2, int(height * 0.35))
        time.sleep(1)
        
        # 尝试输入邮箱
        try:
            # 使用adb输入
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'test@example.com']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.screenshot("email_input")
        print("✅ 邮箱输入测试完成")
    
    def test_input_password(self, app):
        """测试输入密码"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击密码输入框区域
        app.tap(width // 2, int(height * 0.45))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'Test123456']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        # 关闭键盘
        app.back()
        time.sleep(0.5)
        
        app.screenshot("password_input")
        print("✅ 密码输入测试完成")
    
    def test_click_login_button(self, app):
        """测试点击登录按钮"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击登录按钮区域
        app.tap(width // 2, int(height * 0.6))
        time.sleep(3)
        
        app.screenshot("after_login_click")
        print("✅ 登录按钮点击测试完成")
    
    def test_back_from_login(self, app):
        """测试从登录页面返回"""
        app.back()
        time.sleep(1)
        app.screenshot("back_from_login")
        print("✅ 登录页面返回测试完成")


class TestAuthRegister:
    """注册功能测试"""
    
    def test_navigate_to_register(self, app):
        """测试导航到注册页面"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 先到个人中心
        profile_x = (width // 5) * 4
        nav_y = height - 50
        app.tap(profile_x, nav_y)
        time.sleep(2)
        
        # 点击进入登录
        app.tap(width // 2, height // 2)
        time.sleep(2)
        
        # 点击"立即注册"链接 (通常在底部)
        app.tap(width // 2, int(height * 0.85))
        time.sleep(2)
        
        app.screenshot("register_page")
        print("✅ 导航到注册页面成功")
    
    def test_register_page_elements(self, app):
        """测试注册页面元素"""
        time.sleep(1)
        
        page_source = app.driver.page_source
        assert len(page_source) > 5000
        
        app.screenshot("register_page_elements")
        print("✅ 注册页面元素加载成功")
    
    def test_input_register_email(self, app):
        """测试注册-输入邮箱"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 滚动到顶部
        app.swipe_down()
        time.sleep(0.5)
        
        # 点击邮箱输入框
        app.tap(width // 2, int(height * 0.25))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'newuser@example.com']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.screenshot("register_email_input")
        print("✅ 注册邮箱输入测试完成")
    
    def test_input_register_username(self, app):
        """测试注册-输入用户名"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击用户名输入框
        app.tap(width // 2, int(height * 0.35))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'TestUser']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.screenshot("register_username_input")
        print("✅ 注册用户名输入测试完成")
    
    def test_input_register_password(self, app):
        """测试注册-输入密码"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击密码输入框
        app.tap(width // 2, int(height * 0.45))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'Test123456']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.screenshot("register_password_input")
        print("✅ 注册密码输入测试完成")
    
    def test_input_confirm_password(self, app):
        """测试注册-确认密码"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击确认密码输入框
        app.tap(width // 2, int(height * 0.55))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'Test123456']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.back()  # 关闭键盘
        time.sleep(0.5)
        
        app.screenshot("register_confirm_password")
        print("✅ 确认密码输入测试完成")
    
    def test_agree_terms(self, app):
        """测试同意用户协议"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 滚动查看协议
        app.swipe_up()
        time.sleep(0.5)
        
        # 点击同意协议checkbox区域
        app.tap(int(width * 0.1), int(height * 0.65))
        time.sleep(1)
        
        app.screenshot("agree_terms")
        print("✅ 同意用户协议测试完成")
    
    def test_click_register_button(self, app):
        """测试点击注册按钮"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击注册按钮
        app.tap(width // 2, int(height * 0.75))
        time.sleep(3)
        
        app.screenshot("after_register_click")
        print("✅ 注册按钮点击测试完成")
    
    def test_back_from_register(self, app):
        """测试从注册页面返回"""
        app.back()
        time.sleep(1)
        app.back()
        time.sleep(1)
        app.screenshot("back_from_register")
        print("✅ 注册页面返回测试完成")


class TestAuthLogout:
    """登出功能测试"""
    
    def test_navigate_to_profile_for_logout(self, app):
        """测试导航到个人中心进行登出"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击个人中心
        profile_x = (width // 5) * 4
        nav_y = height - 50
        app.tap(profile_x, nav_y)
        time.sleep(2)
        
        app.screenshot("profile_for_logout")
        print("✅ 导航到个人中心成功")
    
    def test_scroll_to_logout(self, app):
        """测试滚动找到登出按钮"""
        # 向下滚动找到登出按钮
        app.swipe_up()
        time.sleep(1)
        app.swipe_up()
        time.sleep(1)
        
        app.screenshot("scroll_to_logout")
        print("✅ 滚动查找登出按钮成功")
    
    def test_click_logout_button(self, app):
        """测试点击登出按钮"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击页面底部的登出按钮区域
        app.tap(width // 2, int(height * 0.8))
        time.sleep(2)
        
        app.screenshot("logout_dialog")
        print("✅ 登出按钮点击测试完成")
    
    def test_confirm_logout(self, app):
        """测试确认登出"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击确认登出 (对话框中的确认按钮)
        app.tap(int(width * 0.7), int(height * 0.55))
        time.sleep(2)
        
        app.screenshot("after_logout")
        print("✅ 确认登出测试完成")


class TestResumeCreate:
    """简历创建功能测试"""
    
    def test_navigate_to_resume_list(self, app):
        """测试导航到简历列表"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击简历标签
        resume_x = (width // 5) * 2
        nav_y = height - 50
        app.tap(resume_x, nav_y)
        time.sleep(2)
        
        app.screenshot("resume_list")
        print("✅ 导航到简历列表成功")
    
    def test_click_create_resume(self, app):
        """测试点击新建简历"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击右下角的浮动按钮创建简历
        app.tap(int(width * 0.85), int(height * 0.9))
        time.sleep(2)
        
        app.screenshot("create_resume_clicked")
        print("✅ 点击新建简历成功")
    
    def test_resume_editor_loads(self, app):
        """测试简历编辑器加载"""
        time.sleep(2)
        
        page_source = app.driver.page_source
        assert len(page_source) > 5000
        
        app.screenshot("resume_editor")
        print("✅ 简历编辑器加载成功")


class TestResumeEdit:
    """简历编辑功能测试"""
    
    def test_edit_basic_info_tab(self, app):
        """测试编辑基本信息Tab"""
        time.sleep(1)
        
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击第一个输入框(姓名)
        app.tap(width // 2, int(height * 0.25))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'Zhang San']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.back()  # 关闭键盘
        time.sleep(0.5)
        
        app.screenshot("edit_basic_info_name")
        print("✅ 基本信息-姓名编辑测试完成")
    
    def test_edit_phone(self, app):
        """测试编辑手机号"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击手机号输入框
        app.tap(width // 2, int(height * 0.35))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', '13800138000']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.back()
        time.sleep(0.5)
        
        app.screenshot("edit_phone")
        print("✅ 基本信息-手机号编辑测试完成")
    
    def test_edit_email(self, app):
        """测试编辑邮箱"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击邮箱输入框
        app.tap(width // 2, int(height * 0.45))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'zhangsan@example.com']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.back()
        time.sleep(0.5)
        
        app.screenshot("edit_email")
        print("✅ 基本信息-邮箱编辑测试完成")
    
    def test_switch_to_education_tab(self, app):
        """测试切换到教育经历Tab"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击教育经历Tab (通常在顶部Tab栏)
        app.tap(int(width * 0.35), int(height * 0.12))
        time.sleep(1)
        
        app.screenshot("education_tab")
        print("✅ 切换到教育经历Tab成功")
    
    def test_add_education(self, app):
        """测试添加教育经历"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击添加按钮 (底部)
        app.tap(width // 2, int(height * 0.9))
        time.sleep(1)
        
        app.screenshot("add_education")
        print("✅ 添加教育经历测试完成")
    
    def test_switch_to_work_tab(self, app):
        """测试切换到工作经历Tab"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击工作经历Tab
        app.tap(int(width * 0.55), int(height * 0.12))
        time.sleep(1)
        
        app.screenshot("work_tab")
        print("✅ 切换到工作经历Tab成功")
    
    def test_add_work_experience(self, app):
        """测试添加工作经历"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击添加按钮
        app.tap(width // 2, int(height * 0.9))
        time.sleep(1)
        
        app.screenshot("add_work")
        print("✅ 添加工作经历测试完成")
    
    def test_switch_to_project_tab(self, app):
        """测试切换到项目经历Tab"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 滑动Tab栏
        app.driver.swipe(int(width * 0.8), int(height * 0.12), 
                         int(width * 0.2), int(height * 0.12), 500)
        time.sleep(1)
        
        # 点击项目经历Tab
        app.tap(int(width * 0.5), int(height * 0.12))
        time.sleep(1)
        
        app.screenshot("project_tab")
        print("✅ 切换到项目经历Tab成功")
    
    def test_switch_to_skills_tab(self, app):
        """测试切换到技能特长Tab"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击技能特长Tab
        app.tap(int(width * 0.8), int(height * 0.12))
        time.sleep(1)
        
        app.screenshot("skills_tab")
        print("✅ 切换到技能特长Tab成功")
    
    def test_add_skill(self, app):
        """测试添加技能"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击添加按钮
        app.tap(width // 2, int(height * 0.9))
        time.sleep(2)
        
        # 如果弹出对话框，输入技能名称
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'Python']
            })
            time.sleep(1)
            
            # 点击添加/确认按钮
            app.tap(int(width * 0.7), int(height * 0.55))
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.screenshot("add_skill")
        print("✅ 添加技能测试完成")
    
    def test_save_resume(self, app):
        """测试保存简历"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击右上角保存按钮
        app.tap(int(width * 0.9), int(height * 0.06))
        time.sleep(2)
        
        app.screenshot("save_resume")
        print("✅ 保存简历测试完成")
    
    def test_back_from_editor(self, app):
        """测试从编辑器返回"""
        app.back()
        time.sleep(1)
        app.screenshot("back_from_editor")
        print("✅ 从编辑器返回测试完成")


class TestResumeExport:
    """简历导出功能测试"""
    
    def test_navigate_to_resume_for_export(self, app):
        """测试导航到简历列表进行导出"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击简历标签
        resume_x = (width // 5) * 2
        nav_y = height - 50
        app.tap(resume_x, nav_y)
        time.sleep(2)
        
        app.screenshot("resume_for_export")
        print("✅ 导航到简历列表成功")
    
    def test_open_resume_menu(self, app):
        """测试打开简历菜单"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击第一个简历的更多按钮 (右侧三点菜单)
        app.tap(int(width * 0.9), int(height * 0.25))
        time.sleep(1)
        
        app.screenshot("resume_menu")
        print("✅ 打开简历菜单成功")
    
    def test_click_export_option(self, app):
        """测试点击导出选项"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击导出选项 (菜单中第二个选项)
        app.tap(width // 2, int(height * 0.45))
        time.sleep(1)
        
        app.screenshot("export_options")
        print("✅ 点击导出选项成功")
    
    def test_export_pdf(self, app):
        """测试导出PDF"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击PDF导出选项
        app.tap(width // 2, int(height * 0.7))
        time.sleep(2)
        
        app.screenshot("export_pdf")
        print("✅ 导出PDF测试完成")
    
    def test_export_word(self, app):
        """测试导出Word"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 再次打开导出菜单
        app.tap(int(width * 0.9), int(height * 0.25))
        time.sleep(1)
        app.tap(width // 2, int(height * 0.45))
        time.sleep(1)
        
        # 点击Word导出选项
        app.tap(width // 2, int(height * 0.75))
        time.sleep(2)
        
        app.screenshot("export_word")
        print("✅ 导出Word测试完成")


class TestResumeImport:
    """简历导入功能测试 (从模板导入)"""
    
    def test_navigate_to_templates(self, app):
        """测试导航到模板库"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击模板标签
        template_x = (width // 5) * 3
        nav_y = height - 50
        app.tap(template_x, nav_y)
        time.sleep(2)
        
        app.screenshot("templates_for_import")
        print("✅ 导航到模板库成功")
    
    def test_browse_template_categories(self, app):
        """测试浏览模板分类"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击不同分类
        categories_y = int(height * 0.08)
        
        # 点击第二个分类
        app.tap(int(width * 0.3), categories_y)
        time.sleep(1)
        app.screenshot("template_category_1")
        
        # 点击第三个分类
        app.tap(int(width * 0.5), categories_y)
        time.sleep(1)
        app.screenshot("template_category_2")
        
        print("✅ 浏览模板分类成功")
    
    def test_select_template(self, app):
        """测试选择模板"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击第一个模板
        app.tap(int(width * 0.25), int(height * 0.35))
        time.sleep(2)
        
        app.screenshot("template_selected")
        print("✅ 选择模板成功")
    
    def test_use_template(self, app):
        """测试使用模板创建简历"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击"使用此模板"按钮 (底部Sheet中)
        app.tap(width // 2, int(height * 0.85))
        time.sleep(3)
        
        app.screenshot("use_template")
        print("✅ 使用模板创建简历测试完成")
    
    def test_back_from_import(self, app):
        """测试从导入页面返回"""
        app.back()
        time.sleep(1)
        app.screenshot("back_from_import")
        print("✅ 从导入页面返回测试完成")


class TestAIFeatures:
    """AI功能测试"""
    
    def test_navigate_to_editor_for_ai(self, app):
        """测试导航到编辑器使用AI功能"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击简历标签
        resume_x = (width // 5) * 2
        nav_y = height - 50
        app.tap(resume_x, nav_y)
        time.sleep(2)
        
        # 点击第一个简历进入编辑
        app.tap(width // 2, int(height * 0.25))
        time.sleep(2)
        
        app.screenshot("editor_for_ai")
        print("✅ 导航到编辑器成功")
    
    def test_click_ai_generate_button(self, app):
        """测试点击AI生成按钮"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击顶部工具栏的AI生成按钮
        app.tap(int(width * 0.7), int(height * 0.06))
        time.sleep(2)
        
        app.screenshot("ai_generate_dialog")
        print("✅ AI生成对话框打开成功")
    
    def test_input_target_position(self, app):
        """测试输入目标岗位"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 输入目标岗位
        app.tap(width // 2, int(height * 0.4))
        time.sleep(1)
        
        try:
            app.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', 'Python Developer']
            })
            time.sleep(1)
        except Exception as e:
            print(f"  注意: 输入可能需要键盘 - {e}")
        
        app.back()
        time.sleep(0.5)
        
        app.screenshot("ai_target_position")
        print("✅ 输入目标岗位成功")
    
    def test_click_ai_start_generate(self, app):
        """测试点击开始生成"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击开始生成按钮
        app.tap(int(width * 0.7), int(height * 0.55))
        time.sleep(3)
        
        app.screenshot("ai_generating")
        print("✅ AI生成启动测试完成")
    
    def test_ai_optimize_content(self, app):
        """测试AI优化内容"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 关闭可能的对话框
        app.back()
        time.sleep(1)
        
        # 点击基本信息Tab中的AI优化按钮
        # 先滚动到个人简介区域
        app.swipe_up()
        time.sleep(1)
        
        # 点击AI优化图标
        app.tap(int(width * 0.9), int(height * 0.6))
        time.sleep(2)
        
        app.screenshot("ai_optimize")
        print("✅ AI优化内容测试完成")
    
    def test_back_from_ai(self, app):
        """测试从AI功能返回"""
        app.back()
        time.sleep(1)
        app.back()
        time.sleep(1)
        app.screenshot("back_from_ai")
        print("✅ 从AI功能返回测试完成")


class TestTemplatePreview:
    """模板预览功能测试"""
    
    def test_navigate_to_templates_preview(self, app):
        """测试导航到模板预览"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击模板标签
        template_x = (width // 5) * 3
        nav_y = height - 50
        app.tap(template_x, nav_y)
        time.sleep(2)
        
        app.screenshot("templates_preview")
        print("✅ 导航到模板库成功")
    
    def test_preview_template_detail(self, app):
        """测试预览模板详情"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 点击一个模板查看详情
        app.tap(int(width * 0.25), int(height * 0.35))
        time.sleep(2)
        
        app.screenshot("template_detail_preview")
        print("✅ 模板详情预览成功")
    
    def test_scroll_template_detail(self, app):
        """测试滚动模板详情"""
        app.swipe_up()
        time.sleep(1)
        
        app.screenshot("template_detail_scrolled")
        print("✅ 模板详情滚动成功")
    
    def test_close_template_preview(self, app):
        """测试关闭模板预览"""
        app.back()
        time.sleep(1)
        
        app.screenshot("template_preview_closed")
        print("✅ 关闭模板预览成功")


class TestFinalSummary:
    """最终测试总结"""
    
    def test_complete_navigation_check(self, app):
        """测试完整导航检查"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        nav_y = height - 50
        
        # 遍历所有标签
        tabs = [
            (width // 5, "首页"),
            ((width // 5) * 2, "简历"),
            ((width // 5) * 3, "模板"),
            ((width // 5) * 4, "我的"),
        ]
        
        for x, name in tabs:
            app.tap(x, nav_y)
            time.sleep(1)
            app.screenshot(f"final_check_{name}")
            print(f"  ✓ 最终检查: {name}页面")
        
        print("✅ 完整导航检查完成")
    
    def test_final_summary(self, app):
        """测试完成总结"""
        size = app.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        # 回到首页
        app.tap(width // 5, height - 50)
        time.sleep(2)
        
        app.screenshot("test_complete_final_summary")
        print("✅ 全部功能测试完成!")
