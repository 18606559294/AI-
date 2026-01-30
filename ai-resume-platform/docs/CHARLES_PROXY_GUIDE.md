# Charles Proxy 网络抓包配置指南

Charles Proxy 是一个强大的HTTP/HTTPS抓包工具，用于调试网络请求、分析第三方SDK行为、模拟异常数据等。

## 安装Charles Proxy

### Linux系统
```bash
# 下载Charles Proxy
wget https://www.charlesproxy.com/assets/release/4.6.6/charles-proxy-4.6.6_amd64.tar.gz

# 解压
tar -xzf charles-proxy-4.6.6_amd64.tar.gz

# 启动Charles Proxy
./charles/bin/charles
```

### macOS/Windows
从官网下载安装包：https://www.charlesproxy.com/download/

## 配置Charles Proxy

### 1. 配置代理端口
1. 打开Charles Proxy
2. 菜单：Proxy -> Proxy Settings
3. 设置端口：8888（默认）
4. 勾选 "Support HTTP/2"

### 2. 安装SSL证书（用于HTTPS抓包）

#### Android设备配置
1. 确保Android设备和Charles Proxy在同一网络
2. 在Charles Proxy中：Help -> SSL Proxying -> Install Charles Root Certificate on a Mobile Device
3. 在手机浏览器中访问：`chls.pro/ssl`
4. 下载证书文件
5. 安装证书：设置 -> 安全 -> 安装证书 -> CA证书
6. 命名证书（如：Charles Proxy）
7. 启用证书：设置 -> 安全 -> 受信任的凭据 -> 用户

#### 模拟器配置
```bash
# 启动模拟器
emulator -avd <avd_name> -http-proxy http://<your_ip>:8888

# 或者在模拟器中设置代理
# 设置 -> WLAN -> 长按网络 -> 修改网络 -> 高级选项 -> 代理 -> 手动
# 代理服务器主机名：<your_ip>
# 代理服务器端口：8888
```

### 3. 启用SSL代理
1. 菜单：Proxy -> SSL Proxying Settings
2. 勾选 "Enable SSL Proxying"
3. 添加要抓包的域名：
   - Host: `*`
   - Port: `*`

## Charles Proxy功能

### 1. 查看网络请求
- **Structure视图**：按域名和路径组织请求
- **Sequence视图**：按时间顺序显示请求
- **Request视图**：查看请求头、请求体
- **Response视图**：查看响应头、响应体

### 2. 断点调试
1. 右键点击请求 -> Breakpoints
2. 修改请求或响应内容
3. 执行请求
4. 查看修改后的效果

### 3. 模拟网络条件
1. Tools -> Throttle Settings
2. 设置网络速度：
   - 2G：256 Kbps, 500ms延迟
   - 3G：1 Mbps, 300ms延迟
   - 4G：10 Mbps, 100ms延迟
   - 自定义网络条件

### 4. 模拟服务器错误
1. 右键点击请求 -> Local Response
2. 设置响应状态码、响应体
3. 测试应用的错误处理

### 5. 网络请求重放
1. 右键点击请求 -> Repeat
2. 修改请求参数
3. 重新发送请求

### 6. 压力测试
1. 右键点击请求 -> Repeat Advanced
2. 设置并发数和重复次数
3. 测试服务器性能

## 测试AI简历应用

### 1. 监控API请求
```
预期请求：
- POST /api/v1/auth/register - 用户注册
- POST /api/v1/auth/login - 用户登录
- GET /api/v1/resumes - 获取简历列表
- POST /api/v1/resumes - 创建简历
- PUT /api/v1/resumes/{id} - 更新简历
- DELETE /api/v1/resumes/{id} - 删除简历
- GET /api/v1/templates - 获取模板列表
- POST /api/v1/ai/generate - AI生成内容
- POST /api/v1/export/{format} - 导出简历
```

### 2. 检查请求头
```
预期请求头：
- Content-Type: application/json
- Authorization: Bearer <token>
- User-Agent: AIResumeApp/1.0.0
- X-Device-ID: <设备ID>
- X-Platform: Android
```

### 3. 验证响应格式
```
成功响应：
{
  "code": 200,
  "message": "success",
  "data": {...}
}

错误响应：
{
  "code": 400/401/403/404/500,
  "message": "错误描述",
  "detail": "详细错误信息（仅开发模式）"
}
```

### 4. 测试网络异常
1. 使用Throttle Settings模拟慢速网络
2. 使用Local Response模拟服务器错误
3. 断开网络连接，测试离线行为
4. 验证应用的错误处理和用户提示

### 5. 性能分析
1. 查看请求耗时
2. 识别慢请求
3. 分析请求体大小
4. 优化网络请求

## Charles Proxy技巧

### 1. 过滤请求
```
- 使用搜索框过滤特定请求
- 使用Filter设置过滤规则
- 只显示特定域名的请求
```

### 2. 导出请求/响应
```
- 右键 -> Save Response -> 保存响应体
- File -> Export -> 导出所有请求
- 用于后续分析和测试
```

### 3. 自动化测试
```
- 使用Charles Proxy录制请求
- 导出为HAR文件
- 使用其他工具（如Postman）重放
```

### 4. 调试WebSocket
```
- Charles Proxy支持WebSocket抓包
- 查看WebSocket连接、消息
- 实时监控通信
```

### 5. 调试HTTPS
```
- 安装SSL证书后可以抓取HTTPS请求
- 查看加密流量的明文内容
- 验证证书配置
```

## 常见问题

### 1. 无法抓取HTTPS请求
- 确保已安装SSL证书
- 确保证书已启用
- 检查SSL Proxying设置

### 2. 模拟器无法连接Charles
- 确保设备和Charles在同一网络
- 检查防火墙设置
- 使用设备IP而非localhost

### 3. 请求显示乱码
- 确保Content-Type正确
- 检查响应编码
- 使用合适的编码查看器

### 4. Charles启动失败
- 检查端口8888是否被占用
- 检查Java版本
- 尝试重启Charles

## 安全注意事项

⚠️ **重要提醒**：
1. Charles Proxy会拦截所有网络流量
2. 不要在生产环境中使用
3. 测试完成后关闭代理
4. 删除测试设备上的证书
5. 不要泄露敏感数据

## 与其他工具配合

### 1. Stetho
- Chrome DevTools调试
- 查看数据库
- 查看SharedPreferences
- 网络请求监控

### 2. Android Profiler
- CPU性能分析
- 内存使用分析
- 网络活动监控
- 电量消耗分析

### 3. Postman
- 导入Charles请求
- 手动测试API
- 创建自动化测试
- 生成API文档

## 性能指标

### 目标指标
- API响应时间 < 1秒
- 首屏加载时间 < 2秒
- 图片加载时间 < 3秒
- 并发请求处理能力 > 100 QPS

### 性能优化建议
1. 使用HTTP/2
2. 启用压缩（gzip）
3. 使用CDN加速
4. 实现请求缓存
5. 优化图片大小
6. 减少请求数量

## 测试检查清单

- [ ] 所有API请求都能被抓取
- [ ] HTTPS请求可以正常查看
- [ ] 请求头包含所有必要信息
- [ ] 响应格式符合规范
- [ ] 错误处理正确
- [ ] 网络异常处理正确
- [ ] 慢网络表现正常
- [ ] 无内存泄漏
- [ ] 无安全漏洞

## 参考资料

- Charles Proxy官方文档：https://www.charlesproxy.com/documentation/
- Android网络安全：https://developer.android.com/training/articles/security-config
- HTTP/2协议：https://http2.github.io/

---

**配置完成后，就可以开始全面测试AI简历应用的网络请求了！**