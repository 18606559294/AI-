package com.example.ai_resume_app

import android.content.Intent
import androidx.benchmark.macro.CompilationMode
import androidx.benchmark.macro.ExperimentalBaselineProfilesApi
import androidx.benchmark.macro.StartupMode
import androidx.benchmark.macro.StartupTimingMetric
import androidx.benchmark.macro.junit4.MacrobenchmarkRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Macrobenchmark性能测试示例
 * 用于测试应用启动、UI交互等大规模用户操作的性能
 * 
 * 使用方法：
 * 1. 需要单独创建benchmark模块
 * 2. 在benchmark模块中运行测试
 * 3. 测试结果包括启动时间、帧率等性能指标
 */
@RunWith(AndroidJUnit4::class)
class MacrobenchmarkExample {

    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    /**
     * 测试应用冷启动性能
     * 冷启动：应用进程不存在，系统需要创建新进程
     */
    @Test
    fun benchmarkColdStart() {
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.COLD,
            compilationMode = CompilationMode.DEFAULT()
        ) {
            pressHome()
            startActivityAndWait()
        }
    }

    /**
     * 测试应用热启动性能
     * 热启动：应用进程在后台运行，切换回前台
     */
    @Test
    fun benchmarkWarmStart() {
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.WARM,
            compilationMode = CompilationMode.DEFAULT()
        ) {
            pressHome()
            startActivityAndWait()
        }
    }

    /**
     * 测试应用温启动性能
     * 温启动：应用被系统杀死但进程缓存还存在
     */
    @Test
    fun benchmarkHotStart() {
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.HOT,
            compilationMode = CompilationMode.DEFAULT()
        ) {
            pressHome()
            startActivityAndWait()
        }
    }

    /**
     * 测试使用Baseline Profile优化的启动性能
     * Baseline Profile可以显著提升应用启动速度
     */
    @OptIn(ExperimentalBaselineProfilesApi::class)
    @Test
    fun benchmarkStartupWithBaselineProfiles() {
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.COLD,
            compilationMode = CompilationMode.Partial()
        ) {
            pressHome()
            startActivityAndWait()
        }
    }

    /**
     * 测试UI操作性能（示例：滚动操作）
     */
    @Test
    fun benchmarkScrolling() {
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.COLD,
            compilationMode = CompilationMode.DEFAULT()
        ) {
            pressHome()
            startActivityAndWait()
            
            // 执行滚动操作
            device.drag(
                startX = device.displayWidth / 2,
                startY = device.displayHeight * 3 / 4,
                endX = device.displayWidth / 2,
                endY = device.displayHeight / 4,
                steps = 50
            )
            
            // 等待动画完成
            device.waitForIdle()
        }
    }

    // 更多Macrobenchmark测试示例：
    /*
    @Test
    fun benchmarkScreenTransition() {
        // 测试页面切换性能
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.COLD
        ) {
            pressHome()
            startActivityAndWait()
            
            // 执行页面切换操作
            val button = device.findObject(
                By.res("com.example.ai_resume_app:id/nav_button")
            )
            button.click()
            
            device.waitForIdle()
        }
    }
    
    @Test
    fun benchmarkListLoading() {
        // 测试列表加载性能
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(
                StartupTimingMetric(),
                FrameTimingMetric() // 帧率指标
            ),
            iterations = 10,
            startupMode = StartupMode.COLD
        ) {
            pressHome()
            startActivityAndWait()
            
            // 等待列表加载完成
            device.wait(
                Until.hasObject(By.res("com.example.ai_resume_app:id/list_view")),
                5000
            )
            
            // 执行列表滚动
            val listView = device.findObject(
                By.res("com.example.ai_resume_app:id/list_view")
            )
            listView.fling(Direction.DOWN)
        }
    }
    */
}

/*
运行Macrobenchmark的步骤：
1. 创建benchmark模块（需要单独的gradle模块）
2. 在benchmark模块的build.gradle.kts中添加依赖：
   ```
   dependencies {
       implementation("androidx.benchmark:benchmark-macro-junit4:1.2.0")
   }
   ```
3. 在benchmark模块中创建测试类
4. 运行测试（使用benchmark运行配置）

注意事项：
- Macrobenchmark需要在单独的模块中运行
- 测试会在模拟器或真机上安装应用
- 每次测试会多次启动应用以获得稳定结果
- 建议在性能较好的设备上运行测试
- 使用Baseline Profile可以显著提升应用性能
*/