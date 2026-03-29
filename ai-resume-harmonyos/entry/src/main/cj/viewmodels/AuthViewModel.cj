// AuthViewModel.cj - 认证视图模型
package viewmodels

import models.*
import services.*
import ohos.arkui.state.*

public class AuthViewModel {
    @State private var currentUser: ?User = None
    @State private var isAuthenticated: Bool = false
    @State private var isLoading: Bool = false
    @State private var errorMessage: String = ""

    private let authService: AuthService

    public init() {
        this.authService = AuthService()
        // 检查是否已登录
        this.isAuthenticated = authService.isAuthenticated()
    }

    // 登录
    public func login(email: String, password: String): Bool {
        isLoading = true
        errorMessage = ""

        let result = authService.login(email, password)
        isLoading = false

        if (result.isSuccess()) {
            isAuthenticated = true
            return true
        } else {
            errorMessage = result.getError()
            return false
        }
    }

    // 注册
    public func register(email: String, username: String, password: String, fullName: String): Bool {
        isLoading = true
        errorMessage = ""

        let result = authService.register(email, username, password, fullName)
        isLoading = false

        if (result.isSuccess()) {
            let value = result.getValue()
            if (value is Some<User>) {
                currentUser = Some(value.get())
            }
            return true
        } else {
            errorMessage = result.getError()
            return false
        }
    }

    // 登出
    public func logout(): Unit {
        authService.logout()
        currentUser = None
        isAuthenticated = false
    }

    // 刷新Token
    public func refreshToken(): Bool {
        let result = authService.refreshToken()
        return result.isSuccess()
    }

    // Getter方法
    public func getUser(): ?User {
        return currentUser
    }

    public func isLoggedIn(): Bool {
        return isAuthenticated
    }

    public func isLoading(): Bool {
        return isLoading
    }

    public func getError(): String {
        return errorMessage
    }
}
