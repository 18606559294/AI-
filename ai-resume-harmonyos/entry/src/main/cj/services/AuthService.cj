// AuthService.cj - 认证服务
package services

import models.*
import std.collection.*
import std.json.*

public class AuthService {
    private let httpClient: HttpClient
    private let tokenStorage: TokenStorage

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
            let token = parseAuthToken(response.body)
            if (token.accessToken != "") {
                tokenStorage.saveToken(token)
                httpClient.setAuthToken(token.accessToken)
                return Result<AuthToken>.success(token)
            }
        }

        return Result<AuthToken>.failure(response.error)
    }

    // 用户注册
    public func register(email: String, username: String, password: String, fullName: String): Result<User> {
        let request = RegisterRequest(email, username, password, fullName)
        let jsonBody = serializeRegisterRequest(request)
        let response = httpClient.post(ApiConfig.AUTH_REGISTER, jsonBody)

        if (response.isSuccess()) {
            let user = parseUser(response.body)
            return Result<User>.success(user)
        }

        return Result<User>.failure(response.error)
    }

    // 刷新Token
    public func refreshToken(): Result<AuthToken> {
        let savedToken = tokenStorage.getToken()
        if (savedToken.refreshToken == "") {
            return Result<AuthToken>.failure("No refresh token available")
        }

        let body = "{\"refresh_token\": \"${savedToken.refreshToken}\"}"
        let response = httpClient.post(ApiConfig.AUTH_REFRESH, body)

        if (response.isSuccess()) {
            let token = parseAuthToken(response.body)
            tokenStorage.saveToken(token)
            httpClient.setAuthToken(token.accessToken)
            return Result<AuthToken>.success(token)
        }

        return Result<AuthToken>.failure(response.error)
    }

    // 登出
    public func logout(): Unit {
        httpClient.post(ApiConfig.AUTH_LOGOUT, "{}")
        tokenStorage.clearToken()
        httpClient.clearAuthToken()
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

    // 序列化登录请求
    private func serializeLoginRequest(request: LoginRequest): String {
        return "{\"email\": \"${request.email}\", \"password\": \"${request.password}\"}"
    }

    // 序列化注册请求
    private func serializeRegisterRequest(request: RegisterRequest): String {
        return "{\"email\": \"${request.email}\", \"username\": \"${request.username}\", \"password\": \"${request.password}\", \"full_name\": \"${request.fullName}\"}"
    }

    // 解析AuthToken
    private func parseAuthToken(json: String): AuthToken {
        let token = AuthToken()
        try {
            let obj = JsonParser.parse(json)
            token.accessToken = obj.getString("access_token")
            token.refreshToken = obj.getString("refresh_token")
            token.tokenType = obj.getString("token_type", "bearer")
            token.expiresIn = obj.getInt64("expires_in", 0)
        } catch (e: Exception) {
            println("Failed to parse auth token: ${e.message}")
        }
        return token
    }

    // 解析User
    private func parseUser(json: String): User {
        let user = User()
        try {
            let obj = JsonParser.parse(json)
            user.id = obj.getInt64("id", 0)
            user.email = obj.getString("email", "")
            user.username = obj.getString("username", "")
            user.fullName = obj.getString("full_name", "")
            user.avatar = obj.getString("avatar", "")
            user.isActive = obj.getBool("is_active", false)
            user.isVerified = obj.getBool("is_verified", false)
            user.createdAt = obj.getString("created_at", "")
            user.updatedAt = obj.getString("updated_at", "")
        } catch (e: Exception) {
            println("Failed to parse user: ${e.message}")
        }
        return user
    }
}

// Token存储类
public class TokenStorage {
    private let prefs: Preferences

    public init() {
        this.prefs = Preferences.get("auth_prefs")
    }

    public func saveToken(token: AuthToken): Unit {
        prefs.putString("access_token", token.accessToken)
        prefs.putString("refresh_token", token.refreshToken)
        prefs.putString("token_type", token.tokenType)
        prefs.putInt64("expires_in", token.expiresIn)
        prefs.flush()
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
