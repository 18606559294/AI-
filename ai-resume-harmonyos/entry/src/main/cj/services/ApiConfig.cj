// ApiConfig.cj - API配置
package services

/**
 * API 配置类
 *
 * 提供统一的 API 端点配置和环境管理
 * 支持开发环境和生产环境的自动切换
 */
public class ApiConfig {
    // 环境配置
    private static let IS_DEV = isDevelopmentMode()
    private static let ENABLE_SSL = !IS_DEV

    // API基础URL - 根据环境自动切换
    public static let BASE_URL: String = IS_DEV
        ? "http://localhost:8000"
        : "https://api.yourapp.com"

    public static let API_VERSION: String = "/api/v1"

    // SSL证书校验（生产环境必须启用）
    public static let ENABLE_SSL_PINNING: Bool = ENABLE_SSL

    // API端点
    public static let AUTH_LOGIN: String = "/auth/login"
    public static let AUTH_REGISTER: String = "/auth/register"
    public static let AUTH_REFRESH: String = "/auth/refresh"
    public static let AUTH_LOGOUT: String = "/auth/logout"

    public static let RESUMES: String = "/resumes"
    public static let RESUME_BY_ID: String = "/resumes/{id}"
    public static let RESUME_GENERATE: String = "/resumes/generate"

    public static let TEMPLATES: String = "/templates"
    public static let TEMPLATE_BY_ID: String = "/templates/{id}"

    public static let AI_GENERATE: String = "/ai/generate"
    public static let AI_USAGE: String = "/ai/usage"

    public static let EXPORT_PDF: String = "/export/pdf"
    public static let EXPORT_DOCX: String = "/export/docx"

    // 请求超时配置
    public static let CONNECT_TIMEOUT: Int64 = 30 * SECOND  // 30秒
    public static let READ_TIMEOUT: Int64 = 60 * SECOND     // 60秒
    public static let WRITE_TIMEOUT: Int64 = 60 * SECOND    // 60秒

    // 时间常量
    public static let SECOND: Int64 = 1000
    public static let MINUTE: Int64 = 60 * SECOND

    /**
     * 检测是否为开发模式
     */
    private static func isDevelopmentMode(): Bool {
        // 通过构建配置或环境变量判断
        // 这里假设使用 BuildConfig（实际实现根据项目构建系统调整）
        return true  // 默认为开发模式
    }

    /**
     * 获取完整URL
     */
    public static func getFullUrl(endpoint: String): String {
        return BASE_URL + API_VERSION + endpoint
    }

    /**
     * 获取环境信息
     */
    public static func getEnvironment(): String {
        return IS_DEV ? "development" : "production"
    }

    /**
     * 是否为生产环境
     */
    public static func isProduction(): Bool {
        return !IS_DEV
    }
}
