# DevOps 快速参考

> **AI Resume Platform - DevOps 工程师快速参考**
> 更新时间: 2026-04-02

---

## 🚀 关键服务器信息

### Dokploy 管理面板
```
URL: http://113.45.64.145:3000
邮箱: 641600780@qq.com
密码: li780swsgbo
```

### 云服务器
```
IP: 113.45.64.145
OS: Ubuntu 24.04 LTS
SSH用户: root
```

### GitHub 仓库
```
URL: https://github.com/18606559294/AI-.git
分支: main
待推送: 103 个提交
```

---

## ⚡ 快速命令

### 健康检查
```bash
# 检查所有服务状态
docker ps

# 后端 API 健康检查
curl http://localhost:8000/health

# 运行健康检查脚本
./scripts/health-check.sh
```

### Git 操作
```bash
# 检查待推送提交
git log --oneline origin/main..HEAD

# 推送代码 (需先配置身份验证)
./scripts/push-to-github.sh

# 查看状态
git status
```

### 部署操作
```bash
# Dokploy 部署准备
./scripts/deploy-dokploy.sh

# 备份数据
./scripts/backup.sh
```

---

## 🔑 GitHub 身份验证配置

### 方案 A: Personal Access Token (推荐)
1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限: `repo` (全部)
4. 复制生成的 Token
5. 推送: `git push https://<TOKEN>@github.com/18606559294/AI-.git main`

### 方案 B: SSH 密钥
1. 复制公钥: `cat ~/.ssh/id_ed25519.pub`
2. 添加到: https://github.com/settings/ssh
3. 切换 URL: `git remote set-url origin git@github.com:18606559294/AI-.git`
4. 推送: `git push origin main`

---

## 📊 服务端口映射

| 服务 | 容器端口 | 主机端口 | 健康检查 |
|------|----------|----------|----------|
| Backend | 8000 | 8000 | `/health` |
| Frontend | 80 | 3000 | `/` |
| Redis | 6379 | 6379 | `redis-cli ping` |
| Prometheus | 9090 | 9090 | - |
| Grafana | 3001 | 3001 | - |

---

## 📚 重要文档

| 文档 | 说明 |
|------|------|
| `DOKPLOY_MANUAL_STEPS.md` | Dokploy 详细配置步骤 |
| `GIT_PUSH_GUIDE.md` | GitHub 推送指南 |
| `DEVOPS_GUIDE.md` | DevOps 操作指南 |
| `DEPLOYMENT_CHECKLIST.md` | 部署检查清单 |

---

## 🛠️ 运维脚本

| 脚本 | 用途 |
|------|------|
| `scripts/deploy-dokploy.sh` | Dokploy 部署准备 |
| `scripts/push-to-github.sh` | GitHub 推送辅助 |
| `scripts/health-check.sh` | 系统健康检查 |
| `scripts/backup.sh` | 完整系统备份 |
| `scripts/monitor.sh` | 服务监控 |

---

## 🎯 部署流程

1. **配置 GitHub 身份验证** (5 分钟)
2. **推送代码到 GitHub** (2 分钟)
3. **登录 Dokploy 面板** (1 分钟)
4. **创建并配置应用** (20 分钟)
5. **触发部署** (5 分钟)
6. **验证服务健康** (10 分钟)

**总计: ~45 分钟**

---

## 🆘 故障排查

### 推送失败
```bash
# 检查远程仓库
git remote -v

# 检查身份验证
git ls-remote origin
```

### 服务异常
```bash
# 查看容器日志
docker logs ai-resume-backend
docker logs ai-resume-frontend

# 重启服务
docker-compose restart backend
```

### 网络问题
```bash
# 测试 Dokploy 连接
curl -I http://113.45.64.145:3000

# 测试 GitHub 连接
ping github.com
```

---

**DevOps 工程师: Agent 29126157-6833-4f1e-94bd-6493bd95d3f2**
