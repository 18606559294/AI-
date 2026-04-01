# Dokploy 手动配置指南

> **AI Resume Platform - DevOps 部署步骤**
> 生成时间: 2026-04-02
> Dokploy 版本: v0.28.8

---

## 📋 前提条件

- ✅ Dokploy 服务器可访问: http://113.45.64.145:3000
- ✅ 登录凭据已准备: 641600780@qq.com / li780swsgbo
- ✅ 本地配置文件完整 (已验证)
- ⚠️ 待处理: GitHub 代码推送 (99 个提交待推送)

---

## 🔑 步骤 1: 登录 Dokploy 管理面板

1. **访问登录页面**
   ```
   URL: http://113.45.64.145:3000
   ```

2. **输入登录凭据**
   ```
   邮箱: 641600780@qq.com
   密码: li780swsgbo
   ```

3. **验证登录成功**
   - 应看到 Dokploy 主面板
   - 显示现有项目: "AI智能体简历"

---

## 🔐 步骤 2: 配置 SSH 密钥

1. **导航到 SSH Keys 设置**
   ```
   左侧菜单 → Settings → SSH Keys
   ```

2. **添加新的 SSH 密钥**
   - 点击 "Add SSH Key" 按钮
   - 粘贴以下公钥内容:
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPhpLCnOdDAksakqgydJAqd3vL0rHvJ7I2N/SE6wHgu5 AI_Agent_Key
   ```

3. **保存密钥**
   - 点击 "Save" 或 "Add" 按钮

4. **验证 SSH 连接** (可选)
   ```bash
   ssh -i ~/.ssh/id_ed25519 root@113.45.64.145
   ```

---

## 🚀 步骤 3: 创建新应用

1. **进入项目页面**
   ```
   点击 "AI智能体简历" 项目
   ```

2. **创建新应用**
   - 点击 "Create Application" 或 "New Application" 按钮
   - 选择应用类型: **Docker Compose**
   - 填写应用信息:
   ```
   应用名称: ai-resume-platform
   描述: AI Resume Platform - 智能简历生成系统
   ```

3. **继续配置** (根据向导)

---

## 📦 步骤 4: 配置 Git 仓库

1. **设置 Git 源**
   - 仓库 URL: `https://github.com/18606559294/AI-.git`
   - 分支: `main`
   - 构建类型: `Docker Compose`

2. **配置 Docker Compose**
   - Docker Compose 文件路径: `docker-compose.prod.yml`
   - 工作目录: `.` (根目录)

3. **验证配置**
   - 确保 Dokploy 可以访问仓库
   - 检查分支是否存在

---

## 🔧 步骤 5: 设置环境变量

1. **进入环境变量设置**
   ```
   应用设置 → Environment Variables
   ```

2. **配置方式选择**

   **方式 A: 上传 .env 文件**
   - 上传 `.env.production` 文件内容

   **方式 B: 手动设置关键变量**
   ```env
   DEBUG=false
   SECRET_KEY=48f5ff7d1aa60c67f2a48636b4ee450fce688f9816f66dea152aa66745916ba9
   DATABASE_URL=sqlite+aiosqlite:///./data/ai_resume.db
   REDIS_URL=redis://redis:6379/0
   JWT_SECRET=7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=60
   ```

3. **敏感信息提醒**
   - ⚠️ 不要在生产环境使用示例密钥
   - ⚠️ XIAOMI_API_KEY 需要配置实际值
   - ⚠️ ALLOWED_ORIGINS 需要更新为实际域名

---

## 🌐 步骤 6: 配置域名和 SSL

1. **添加域名**
   ```
   应用设置 → Domains → Add Domain
   ```

2. **配置后端域名**
   ```
   域名: api.yourdomain.com
   服务: ai-resume-backend
   端口: 8000
   HTTPS: 启用
   ```

3. **配置前端域名**
   ```
   域名: yourdomain.com
   服务: ai-resume-frontend
   端口: 80
   HTTPS: 启用
   ```

4. **SSL 证书**
   - Dokploy 会自动申请 Let's Encrypt 证书
   - 确保 DNS 已正确解析到 113.45.64.145
   - 等待证书签发 (可能需要 5-10 分钟)

---

## 📊 步骤 7: 配置监控 (可选)

1. **启用 Prometheus**
   ```
   应用设置 → Monitoring → Enable Prometheus
   端口: 9090
   ```

2. **启用 Grafana**
   ```
   应用设置 → Monitoring → Enable Grafana
   端口: 3001
   默认用户: admin
   默认密码: admin
   ```

3. **配置告警** (可选)
   - Slack Webhook URL
   - Email 通知设置

---

## ▶️ 步骤 8: 部署应用

1. **触发部署**
   - 点击 "Deploy" 或 "Redeploy" 按钮
   - 等待镜像构建 (首次可能需要 5-15 分钟)

2. **监控部署日志**
   ```
   应用 → Logs 标签页
   ```
   - 查看构建进度
   - 检查是否有错误

3. **验证容器启动**
   - 确保 ai-resume-backend 运行正常
   - 确保 ai-resume-frontend 运行正常
   - 确保 ai-resume-redis 运行正常

---

## ✅ 步骤 9: 健康检查验证

1. **检查后端 API**
   ```bash
   curl http://api.yourdomain.com/health
   ```
   预期响应: `{"status": "ok", "version": "1.0.0"}`

2. **检查前端**
   ```bash
   curl http://yourdomain.com/
   ```
   预期: 返回 HTML 内容

3. **检查监控服务**
   - Prometheus: http://113.45.64.145:9090
   - Grafana: http://113.45.64.145:3001

4. **检查容器状态**
   ```bash
   docker ps | grep ai-resume
   ```

---

## 🔄 步骤 10: 配置自动部署 (可选)

1. **配置 Webhook**
   - 在 GitHub 仓库设置中添加 Dokploy Webhook URL
   - 选择触发事件: push to main

2. **启用自动部署**
   ```
   应用设置 → Auto Deploy → Enable
   ```
   - 每次 push 到 main 分支自动触发部署

---

## 📝 配置检查清单

- [ ] SSH 密钥已添加
- [ ] Git 仓库已配置
- [ ] 环境变量已设置
- [ ] 域名已配置
- [ ] SSL 证书已签发
- [ ] 应用已成功部署
- [ ] 健康检查通过
- [ ] 监控服务已启用
- [ ] 告警通知已配置

---

## 🆘 常见问题

### 问题 1: 镜像构建失败
**解决方案**: 检查 Dockerfile 语法，确认所有依赖可用

### 问题 2: 健康检查失败
**解决方案**: 检查应用日志，确认服务正常启动

### 问题 3: SSL 证书签发失败
**解决方案**: 检查 DNS 解析，确保域名指向服务器 IP

### 问题 4: 端口冲突
**解决方案**: 修改 docker-compose.prod.yml 中的端口映射

---

## 📞 支持

如遇到问题，请参考:
- `DOKPLOY_DEPLOYMENT_GUIDE.md` - 详细部署指南
- `DEVOPS_GUIDE.md` - DevOps 操作指南
- `DEPLOYMENT_CHECKLIST.md` - 部署检查清单

---

**文档版本**: 1.0
**最后更新**: 2026-04-02
**维护者**: DevOps 工程师
