package com.example.ai_resume_app.benchmark

import androidx.benchmark.macro.CompilationMode
import androidx.benchmark.macro.FrameTimingMetric
import androidx.benchmark.macro.StartupMode
import androidx.benchmark.macro.junit4.MacrobenchmarkRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Macrobenchmark 性能测试套件
 *
 * 测试内容:
 * 1. 冷启动性能 - 应用完全关闭后启动
 * 2. 温启动性能 - 应用从后台恢复
 * 3. 热启动性能 - 应用从内存中恢复
 * 4. 帧率性能 - UI渲染帧率
 * 5. 编译模式对比 - 不同编译模式下的性能
 *
 * 运行方式:
 * ./gradlew :app:connectedCheck
 * 或在Android Studio中右键运行
 */
@RunWith(AndroidJUnit4::class)
@LargeTest
class StartupBenchmark {

    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    /**
     * 测试1: 冷启动性能测试
     * 
     * 目标: 启动时间 < 1000ms
     * 测量: 从系统启动到第一帧完全渲染的时间
     */
    @Test
    fun startupCompilationNone() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            FrameTimingMetric(),          // 帧时间指标
            androidx.benchmark.macro.StartupTimingMetric()  // 启动时间指标
        ),
        iterations = 10,
        startupMode = StartupMode.COLD,  // 冷启动
        compilationMode = CompilationMode.None()  // 无编译
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试2: 温启动性能测试
     * 
     * 目标: 启动时间 < 400ms
     * 测量: 应用从后台恢复的时间
     */
    @Test
    fun startupWarm() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            androidx.benchmark.macro.StartupTimingMetric()
        ),
        iterations = 10,
        startupMode = StartupMode.WARM,  // 温启动
        compilationMode = CompilationMode.None()
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试3: 热启动性能测试
     * 
     * 目标: 启动时间 < 200ms
     * 测量: 应用从内存中恢复的时间
     */
    @Test
    fun startupHot() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            androidx.benchmark.macro.StartupTimingMetric()
        ),
        iterations = 10,
        startupMode = StartupMode.HOT,  // 热启动
        compilationMode = CompilationMode.None()
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试4: 部分编译模式性能
     * 
     * 模拟实际使用中的性能
     * 基准配置文件优化后的性能
     */
    @Test
    fun startupCompilationPartial() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            androidx.benchmark.macro.StartupTimingMetric(),
            FrameTimingMetric()
        ),
        iterations = 10,
        startupMode = StartupMode.COLD,
        compilationMode = CompilationMode.Partial(   // 部分编译
            compilationMode = androidx.benchmark.macro.CompilationMode.Mode.Partial
                .baselineProfile() as androidx.benchmark.macro.CompilationMode
        )
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试5: 完全编译模式性能
     * 
     * 测量最佳性能（AOT编译后）
     */
    @Test
    fun startupCompilationFull() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            androidx.benchmark.macro.StartupTimingMetric(),
            FrameTimingMetric()
        ),
        iterations = 10,
        startupMode = StartupMode.COLD,
        compilationMode = CompilationMode.Full()  // 完全编译
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试6: UI渲染性能测试
     * 
     * 测量帧率和卡顿情况
     * 目标: 90th percentile 帧时间 < 16ms (60fps)
     */
    @Test
    fun frameRenderingPerformance() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            FrameTimingMetric()
        ),
        iterations = 5,
        startupMode = StartupMode.COLD
    ) {
        pressHome()
        startActivityAndWait()
        // 等待UI稳定
        device.waitForIdle()
    }

    /**
     * 测试7: 页面导航性能
     * 
     * 测量页面切换的流畅度
     */
    @Test
    fun navigationPerformance() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            FrameTimingMetric()
        ),
        iterations = 5,
        startupMode = StartupMode.WARM
    ) {
        pressHome()
        startActivityAndWait()
        device.waitForIdle()
        // 这里可以添加具体的导航操作
        // 例如: 点击底部导航栏切换页面
    }
}
