// ApiConfig.cj - API配置
package services

public class ApiConfig {
    // API基础URL
    public static let BASE_URL: String = "http://localhost:8000"
    public static let API_VERSION: String = "/api/v1"

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

    // 请求超时
    public static let CONNECT_TIMEOUT: Int64 = 30000  // 30秒
    public static let READ_TIMEOUT: Int64 = 60000     // 60秒
    public static let WRITE_TIMEOUT: Int64 = 60000    // 60秒

    // 获取完整URL
    public static func getFullUrl(endpoint: String): String {
        return BASE_URL + API_VERSION + endpoint
    }
}
