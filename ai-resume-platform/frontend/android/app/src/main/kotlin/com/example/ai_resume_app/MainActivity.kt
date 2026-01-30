package com.example.ai_resume_app

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import androidx.annotation.NonNull

/**
 * MainActivity - AI简历应用主Activity
 *
 * 开发调试工具集成:
 * - LeakCanary: 内存泄漏自动检测
 * - Stetho: Chrome DevTools调试
 *
 * 调试工具仅在debug构建中启用，release构建不会包含
 */
class MainActivity : FlutterActivity() {

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        // 初始化调试工具 (仅在debug构建中)
        if (BuildConfig.DEBUG) {
            initDebugTools()
        }
    }

    /**
     * 初始化调试工具
     *
     * LeakCanary会自动初始化，无需手动配置
     * Stetho需要手动初始化
     */
    private fun initDebugTools() {
        try {
            // 初始化Stetho - Chrome DevTools调试
            val stethoClass = Class.forName("com.facebook.stetho.Stetho")
            val initializeWithDefaults = stethoClass.getMethod("initializeWithDefaults")
            initializeWithDefaults.invoke(null)

            android.util.Log.d("MainActivity", "Debug tools initialized: Stetho enabled")
        } catch (e: ClassNotFoundException) {
            android.util.Log.w("MainActivity", "Stetho not available in this build")
        } catch (e: Exception) {
            android.util.Log.e("MainActivity", "Failed to initialize debug tools", e)
        }
    }

    companion object {
        init {
        // 确保LeakCanary能正确检测Activity泄漏
            System.loadLibrary("flutter")
        }
    }
}
