# 微信登录配置指南

## 后端配置

### 1. 环境变量配置

在 `backend/.env` 文件中添加以下配置：

```bash
# 微信小程序配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
```

### 2. 获取微信AppID和AppSecret

1. 登录微信公众平台：https://mp.weixin.qq.com/
2. 进入"开发" -> "开发管理" -> "开发设置"
3. 记录以下信息：
   - AppID (小程序ID)
   - AppSecret (小程序密钥)

### 3. 配置服务器域名

在微信小程序后台配置服务器域名：
- request合法域名：添加你的后端API域名
- 例如：https://your-api.com

## 前端配置

### 1. Android配置

在 `frontend/android/app/src/main/AndroidManifest.xml` 中添加：

```xml
<application>
    <!-- 微信分享和登录 -->
    <activity
        android:name=".wxapi.WXEntryActivity"
        android:exported="true"
        android:launchMode="singleTop" />
</application>
```

在 `frontend/android/app/build.gradle` 中添加：

```gradle
defaultConfig {
    manifestPlaceholders = [
        WECHAT_APP_ID: "your_wechat_app_id"
    ]
}
```

### 2. iOS配置

在 `frontend/ios/Runner/Info.plist` 中添加：

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>your_wechat_app_id</string>
        </array>
    </dict>
</array>
```

### 3. Flutter配置

确保 `pubspec.yaml` 中已添加：

```yaml
dependencies:
  fluwx: ^4.0.0
```

## 测试流程

### 1. 后端测试

使用curl测试微信登录API：

```bash
curl -X POST "http://localhost:8000/api/v1/auth/wechat/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}'
```

### 2. 前端测试

在登录页面点击"微信登录"按钮，测试以下流程：
1. 调起微信授权
2. 获取授权码
3. 发送到后端
4. 完成登录

## 注意事项

1. **开发环境**：使用微信开发者工具进行测试
2. **生产环境**：需要在微信小程序后台完成域名配置和服务器白名单
3. **安全建议**：
   - AppSecret不要泄露
   - 使用HTTPS通信
   - 实现严格的token验证机制
4. **错误处理**：
   - 授权失败
   - 网络错误
   - 用户取消授权

## 常见问题

### Q: 微信登录返回"code been used"
A: code只能使用一次，需要重新获取

### Q: 提示" redirect_uri 参数错误"
A: 检查微信小程序后台的授权域名配置

### Q: 无法调起微信
A: 检查AppID是否正确，以及Android/iOS配置是否完整

## 当前状态

✅ 后端API已实现 (backend/app/api/v1/auth.py)
✅ 前端fluwx SDK已集成
⚠️  需要配置微信AppID和AppSecret
⚠️  需要完成Android/iOS平台配置
