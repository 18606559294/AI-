// AuthService.cj - 认证服务
package services

import models.*
import std.collection.*
import std.json.*
import utils.*

public class AuthService {
    private let httpClient: HttpClient
    private let tokenStorage: TokenStorage
    private static let logger = Logger("AuthService")

    public init() {
        this.httpClient = HttpClient(ApiConfig.BASE_URL + ApiConfig.API_VERSION)
        this.tokenStorage = TokenStorage()
    }

    // 用户登录
    public func login(email: String, password: String): Result<AuthToken> {
        let request = LoginRequest(email, password)
        let jsonBody = serializeLoginRequest(request)
        let response = httpClient.post(ApiConfig.AUTH_LOGIN, jsonBody)

        if (response.isSuccess()) {
            let result = parseAuthToken(response.body)
            if (result.isSuccess()) {
                let token = result.getValue()!!
                tokenStorage.saveToken(token)
                httpClient.setAuthToken(token.accessToken)
                logger.info("User logged in successfully: ${email}")
                return Result<AuthToken>.success(token)
            } else {
                return Result<AuthToken>.failure(result.getError())
            }
        } else {
            let error = ErrorHandler.handleHttpError(response.statusCode, response.body)
            ErrorHandler.logError(error)
            return Result<AuthToken>.failure(error.message)
        }
    }

    // 用户注册
    public func register(email: String, username: String, password: String, fullName: String): Result<User> {
        let request = RegisterRequest(email, username, password, fullName)
        let jsonBody = serializeRegisterRequest(request)
        let response = httpClient.post(ApiConfig.AUTH_REGISTER, jsonBody)

        if (response.isSuccess()) {
            let result = parseUser(response.body)
            if (result.isSuccess()) {
                logger.info("User registered successfully: ${email}")
                return Result<User>.success(result.getValue()!!)
            } else {
                return Result<User>.failure(result.getError())
            }
        } else {
            let error = ErrorHandler.handleHttpError(response.statusCode, response.body)
            ErrorHandler.logError(error)
            return Result<User>.failure(error.message)
        }
    }

    // 刷新Token
    public func refreshToken(): Result<AuthToken> {
        let savedToken = tokenStorage.getToken()
        if (savedToken.refreshToken == "") {
            let error = AppError(
                type: ErrorType.AUTH_ERROR,
                code: "AUTH_003",
                message: "没有可用的刷新令牌"
            )
            ErrorHandler.logError(error)
            return Result<AuthToken>.failure(error.message)
        }

        let obj = JsonObject()
        obj.put("refresh_token", savedToken.refreshToken)
        let body = obj.toJson()

        let response = httpClient.post(ApiConfig.AUTH_REFRESH, body)

        if (response.isSuccess()) {
            let result = parseAuthToken(response.body)
            if (result.isSuccess()) {
                let token = result.getValue()!!
                tokenStorage.saveToken(token)
                httpClient.setAuthToken(token.accessToken)
                logger.info("Token refreshed successfully")
                return Result<AuthToken>.success(token)
            } else {
                return Result<AuthToken>.failure(result.getError())
            }
        } else {
            let error = ErrorHandler.handleHttpError(response.statusCode, response.body)
            ErrorHandler.logError(error)
            return Result<AuthToken>.failure(error.message)
        }
    }

    // 登出
    public func logout(): Unit {
        try {
            httpClient.post(ApiConfig.AUTH_LOGOUT, "{}")
        } catch (e: Exception) {
            logger.warn("Logout request failed: ${e.message}")
        }

        tokenStorage.clearToken()
        httpClient.clearAuthToken()
        logger.info("User logged out")
    }

    // 检查是否已登录
    public func isAuthenticated(): Bool {
        let token = tokenStorage.getToken()
        return token.accessToken != ""
    }

    // 获取当前Token
    public func getCurrentToken(): AuthToken {
        return tokenStorage.getToken()
    }

    // 序列化登录请求 - 使用安全的 JSON 序列化
    private func serializeLoginRequest(request: LoginRequest): String {
        let obj = JsonObject()
        obj.put("email", request.email)
        obj.put("password", request.password)
        return obj.toJson()
    }

    // 序列化注册请求 - 使用安全的 JSON 序列化
    private func serializeRegisterRequest(request: RegisterRequest): String {
        let obj = JsonObject()
        obj.put("email", request.email)
        obj.put("username", request.username)
        obj.put("password", request.password)
        obj.put("full_name", request.fullName)
        return obj.toJson()
    }

    // 解析AuthToken - 返回 Result 类型
    private func parseAuthToken(json: String): Result<AuthToken> {
        try {
            let obj = JsonParser.parse(json)
            let token = AuthToken()
            token.accessToken = obj.getString("access_token", "")
            token.refreshToken = obj.getString("refresh_token", "")
            token.tokenType = obj.getString("token_type", "bearer")
            token.expiresIn = obj.getInt64("expires_in", 0)

            if (token.accessToken == "") {
                return Result<AuthToken>.failure("无效的访问令牌")
            }

            return Result<AuthToken>.success(token)
        } catch (e: Exception) {
            let error = ErrorHandler.handleParseException(e, "parseAuthToken")
            ErrorHandler.logError(error)
            return Result<AuthToken>.failure(error.message)
        }
    }

    // 解析User - 返回 Result 类型
    private func parseUser(json: String): Result<User> {
        try {
            let obj = JsonParser.parse(json)
            let user = User()
            user.id = obj.getInt64("id", 0)
            user.email = obj.getString("email", "")
            user.username = obj.getString("username", "")
            user.fullName = obj.getString("full_name", "")
            user.avatar = obj.getString("avatar", "")
            user.isActive = obj.getBool("is_active", false)
            user.isVerified = obj.getBool("is_verified", false)
            user.createdAt = obj.getString("created_at", "")
            user.updatedAt = obj.getString("updated_at", "")

            return Result<User>.success(user)
        } catch (e: Exception) {
            let error = ErrorHandler.handleParseException(e, "parseUser")
            ErrorHandler.logError(error)
            return Result<User>.failure(error.message)
        }
    }
}

// Token存储类
public class TokenStorage {
    private let prefs: Preferences
    private static let logger = Logger("TokenStorage")

    public init() {
        this.prefs = Preferences.get("auth_prefs")
    }

    public func saveToken(token: AuthToken): Unit {
        prefs.putString("access_token", token.accessToken)
        prefs.putString("refresh_token", token.refreshToken)
        prefs.putString("token_type", token.tokenType)
        prefs.putInt64("expires_in", token.expiresIn)
        prefs.flush()
        logger.debug("Token saved to storage")
    }

    public func getToken(): AuthToken {
        let token = AuthToken()
        token.accessToken = prefs.getString("access_token", "")
        token.refreshToken = prefs.getString("refresh_token", "")
        token.tokenType = prefs.getString("token_type", "bearer")
        token.expiresIn = prefs.getInt64("expires_in", 0)
        return token
    }

    public func clearToken(): Unit {
        prefs.remove("access_token")
        prefs.remove("refresh_token")
        prefs.remove("token_type")
        prefs.remove("expires_in")
        prefs.flush()
        logger.debug("Token cleared from storage")
    }
}

// Result类型
public class Result<T> {
    private var value: ?T = None
    private var error: String = ""
    private var success: Bool = false

    public static func success(value: T): Result<T> {
        let result = Result<T>()
        result.value = Some(value)
        result.success = true
        return result
    }

    public static func failure(error: String): Result<T> {
        let result = Result<T>()
        result.error = error
        result.success = false
        return result
    }

    public func isSuccess(): Bool {
        return success
    }

    public func getValue(): ?T {
        return value
    }

    public func getError(): String {
        return error
    }
}
