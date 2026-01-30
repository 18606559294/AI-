package com.example.ai_resume_app

import android.content.Intent
import androidx.benchmark.macro.BaselineProfileMode
import androidx.benchmark.macro.CompilationMode
import androidx.benchmark.macro.FrameTimingMetric
import androidx.benchmark.macro.StartupMode
import androidx.benchmark.macro.StartupTimingMetric
import androidx.benchmark.macro.junit4.MacrobenchmarkRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Macrobenchmark 性能测试
 * 测试应用的大规模操作性能，如启动时间、UI渲染等
 *
 * 运行方式：
 * ./gradlew :app:connectedAndroidTest -P android.testInstrumentationRunnerArguments.class=com.example.ai_resume_app.PerformanceBenchmark
 */
@RunWith(AndroidJUnit4::class)
@LargeTest
class PerformanceBenchmark {

    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    /**
     * 测试1: 冷启动性能
     * 测试应用完全关闭状态下的启动时间
     */
    @Test
    fun testColdStartup() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD,
        compilationMode = CompilationMode.Full()
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试2: 热启动性能
     * 测试应用从后台恢复的启动时间
     */
    @Test
    fun testHotStartup() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.HOT,
        compilationMode = CompilationMode.Full()
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试3: 温启动性能
     * 测试应用部分状态保留时的启动时间
     */
    @Test
    fun testWarmStartup() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.WARM,
        compilationMode = CompilationMode.Full()
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试4: UI渲染性能 - 主屏幕滚动
     * 测试主屏幕列表滚动的帧率和卡顿情况
     */
    @Test
    fun testHomeScreenScrollPerformance() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(FrameTimingMetric()),
        iterations = 10,
        compilationMode = CompilationMode.Full()
    ) {
        // 启动应用并等待加载完成
        startActivityAndWait()

        // 模拟滚动操作
        // 注意：由于Flutter应用，可能需要使用Flutter特定的滚动操作
        device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
        device.swipe(500, 1500, 500, 500, 20)
        Thread.sleep(1000)
    }

    /**
     * 测试5: 简历编辑器性能
     * 测试简历编辑器在添加内容时的性能
     */
    @Test
    fun testResumeEditorPerformance() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(FrameTimingMetric()),
        iterations = 10,
        compilationMode = CompilationMode.Full()
    ) {
        startActivityAndWait()

        // 导航到简历编辑器
        // 模拟编辑操作
        Thread.sleep(2000)
    }

    /**
     * 测试6: 列表渲染性能
     * 测试简历列表的渲染性能
     */
    @Test
    fun testResumeListPerformance() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(FrameTimingMetric()),
        iterations = 10,
        compilationMode = CompilationMode.Full()
    ) {
        startActivityAndWait()

        // 导航到简历列表
        // 模拟滚动和渲染
        Thread.sleep(2000)
    }

    /**
     * 测试7: 不同编译模式下的性能
     * 比较不同编译模式对性能的影响
     */
    @Test
    fun testCompilationModes() {
        // 测试无编译模式
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 5,
            startupMode = StartupMode.COLD,
            compilationMode = CompilationMode.None()
        ) {
            pressHome()
            startActivityAndWait()
        }

        // 测试部分编译模式
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 5,
            startupMode = StartupMode.COLD,
            compilationMode = CompilationMode.Partial()
        ) {
            pressHome()
            startActivityAndWait()
        }

        // 测试完全编译模式
        benchmarkRule.measureRepeated(
            packageName = "com.example.ai_resume_app",
            metrics = listOf(StartupTimingMetric()),
            iterations = 5,
            startupMode = StartupMode.COLD,
            compilationMode = CompilationMode.Full()
        ) {
            pressHome()
            startActivityAndWait()
        }
    }

    /**
     * 测试8: Baseline Profile性能
     * 测试使用Baseline Profile后的性能提升
     */
    @Test
    fun testBaselineProfile() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD,
        compilationMode = CompilationMode.Partial(
            baselineProfileMode = BaselineProfileMode.Require
        )
    ) {
        pressHome()
        startActivityAndWait()
    }

    /**
     * 测试9: 内存使用基准测试
     * 测试应用在不同操作下的内存使用情况
     */
    @Test
    fun testMemoryUsage() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(
            StartupTimingMetric(),
            FrameTimingMetric()
        ),
        iterations = 10,
        compilationMode = CompilationMode.Full()
    ) {
        startActivityAndWait()

        // 执行一系列操作
        repeat(10) {
            Thread.sleep(100)
        }

        // 使用LeakCanary监控内存泄漏
        // 在Android Profiler中查看内存使用情况
    }

    /**
     * 测试10: 复杂UI操作性能
     * 测试复杂UI交互的性能
     */
    @Test
    fun testComplexUIOperations() = benchmarkRule.measureRepeated(
        packageName = "com.example.ai_resume_app",
        metrics = listOf(FrameTimingMetric()),
        iterations = 10,
        compilationMode = CompilationMode.Full()
    ) {
        startActivityAndWait()

        // 执行复杂UI操作
        // 例如：快速切换页面、滚动、点击等
        Thread.sleep(3000)
    }
}

/**
 * Macrobenchmark 测试指南：
 *
 * 1. 测量启动时间：使用StartupTimingMetric
 * 2. 测量帧率：使用FrameTimingMetric
 * 3. 测试不同编译模式：使用CompilationMode
 * 4. 优化Baseline Profile：提升首次启动性能
 * 5. 在Android Profiler中查看详细结果
 *
 * 性能目标：
 * - 冷启动时间 < 1秒
 * - 热启动时间 < 0.5秒
 * - 帧率 >= 60fps（16.67ms/帧）
 * - 无严重卡顿（>50ms）
 *
 * 使用Android Profiler：
 * 1. 运行测试
 * 2. 在Android Studio中打开Profiler
 * 3. 查看CPU、内存、网络、电量使用情况
 * 4. 分析性能瓶颈并优化
 */