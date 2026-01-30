package com.example.ai_resume_app

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.By
import androidx.test.uiautomator.UiDevice
import androidx.test.uiautomator.UiObject2
import androidx.test.uiautomator.Until
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith

/**
 * UI Automator跨应用测试示例
 * 用于测试系统级操作和跨应用交互
 */
@RunWith(AndroidJUnit4::class)
@LargeTest
class CrossAppTest {

    private lateinit var device: UiDevice
    private val launcherPackage = "com.example.ai_resume_app"
    private val timeout = 5000L

    @Before
    fun setup() {
        device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
        device.pressHome()
    }

    @After
    fun tearDown() {
        device.pressHome()
    }

    /**
     * 测试应用启动
     */
    @Test
    fun testAppLaunch() {
        // 打开应用抽屉
        device.openLauncher()
        
        // 等待应用图标出现
        val appIcon = device.wait(
            Until.findObject(By.text("ai_resume_app")),
            timeout
        )
        
        if (appIcon != null) {
            appIcon.click()
            
            // 验证应用是否启动
            val appLaunched = device.wait(
                Until.hasObject(By.pkg(launcherPackage).depth(0)),
                timeout
            )
            
            assert(appLaunched) { "应用启动失败" }
        }
    }

    // 更多UI Automator测试示例：
    /*
    @Test
    fun testDeviceRotation() {
        // 横向旋转设备
        device.setOrientationLandscape()
        
        // 等待旋转完成
        Thread.sleep(1000)
        
        // 验证UI是否正确调整
        val landscapeElement = device.findObject(By.res(launcherPackage, "element_id"))
        assertNotNull(landscapeElement)
        
        // 恢复纵向
        device.setOrientationPortrait()
    }
    
    @Test
    fun testSystemNotification() {
        // 打开通知栏
        device.openNotification()
        
        // 等待通知栏展开
        Thread.sleep(1000)
        
        // 查找特定通知
        val notification = device.findObject(By.textContains("通知文本"))
        
        if (notification != null) {
            notification.click()
        }
        
        // 返回
        device.pressBack()
    }
    
    @Test
    fun testMultiAppFlow() {
        // 启动第一个应用
        device.executeShellCommand("am start -n com.example.app1/.MainActivity")
        
        // 执行某些操作...
        
        // 切换到另一个应用
        device.executeShellCommand("am start -n com.example.app2/.MainActivity")
        
        // 验证应用切换是否成功
        val currentPackage = device.currentPackageName
        assertEquals("com.example.app2", currentPackage)
    }
    */
}