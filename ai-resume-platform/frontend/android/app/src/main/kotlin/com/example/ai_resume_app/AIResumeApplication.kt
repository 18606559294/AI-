package com.example.ai_resume_app

import android.app.Application
import androidx.startup.AppInitializer
import com.facebook.stetho.Stetho
import leakcanary.LeakCanary

/**
 * AI简历应用主类
 * 用于初始化调试工具和性能监控
 */
class AIResumeApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        // 仅在调试模式下初始化调试工具
        if (BuildConfig.DEBUG) {
            // 初始化LeakCanary - 内存泄漏检测
            // LeakCanary会自动监控Activity、Fragment等组件的内存泄漏
            // 检测到泄漏时会显示通知并提供详细的引用链分析
            initializeLeakCanary()

            // 初始化Stetho调试工具
            // 支持数据库查看、网络请求监控、SharedPreferences查看等功能
            initializeStetho()
        }
    }

    /**
     * 初始化LeakCanary内存泄漏检测工具
     * 检测Activity、Fragment、ViewModel等组件的内存泄漏
     */
    private fun initializeLeakCanary() {
        // LeakCanary会自动监控应用中的对象泄漏
        // 当检测到泄漏时，会在通知栏显示泄漏信息
        // 可以通过通知查看详细的引用链分析
        LeakCanary.install(this)
    }

    /**
     * 初始化Stetho调试工具
     * 支持数据库查看、网络请求监控、SharedPreferences查看等功能
     */
    private fun initializeStetho() {
        Stetho.initializeWithDefaults(this)
    }
}