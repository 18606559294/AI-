// User.cj - 用户数据模型
package models

import std.collection.*

public class User {
    public var id: Int64 = 0
    public var email: String = ""
    public var username: String = ""
    public var fullName: String = ""
    public var avatar: String = ""
    public var isActive: Bool = false
    public var isVerified: Bool = false
    public var createdAt: String = ""
    public var updatedAt: String = ""

    public init() {}

    public init(
        id: Int64,
        email: String,
        username: String,
        fullName: String,
        avatar: String,
        isActive: Bool,
        isVerified: Bool,
        createdAt: String,
        updatedAt: String
    ) {
        this.id = id
        this.email = email
        this.username = username
        this.fullName = fullName
        this.avatar = avatar
        this.isActive = isActive
        this.isVerified = isVerified
        this.createdAt = createdAt
        this.updatedAt = updatedAt
    }
}

public class AuthToken {
    public var accessToken: String = ""
    public var refreshToken: String = ""
    public var tokenType: String = "bearer"
    public var expiresIn: Int64 = 0

    public init() {}

    public init(accessToken: String, refreshToken: String, tokenType: String, expiresIn: Int64) {
        this.accessToken = accessToken
        this.refreshToken = refreshToken
        this.tokenType = tokenType
        this.expiresIn = expiresIn
    }
}

public class LoginRequest {
    public var email: String = ""
    public var password: String = ""

    public init(email: String, password: String) {
        this.email = email
        this.password = password
    }
}

public class RegisterRequest {
    public var email: String = ""
    public var username: String = ""
    public var password: String = ""
    public var fullName: String = ""

    public init(email: String, username: String, password: String, fullName: String) {
        this.email = email
        this.username = username
        this.password = password
        this.fullName = fullName
    }
}
