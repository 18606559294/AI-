# DevOps 操作指南

> **AI Resume Platform - DevOps 工具和配置**
> 最后更新: 2026-04-02

## 目录

- [Dokploy 部署](#dokploy-部署)
- [监控与告警](#监控与告警)
- [备份与恢复](#备份与恢复)
- [健康检查](#健康检查)
- [CI/CD 流水线](#cicd-流水线)

---

## Dokploy 部署

### 配置文件

项目已配置 `dokploy.config.json` 用于 Dokploy 一键部署。

### 部署流程

1. **准备环境**
   ```bash
   # 配置环境变量
   cp .env.production .env

   # 编辑配置
   nano .env
   ```

2. **启动监控服务** (可选)
   ```bash
   docker-compose -f docker-compose.prod.yml -f docker-compose.monitoring.yml up -d
   ```

3. **通过 Dokploy 部署**
   ```bash
   # Dokploy 会自动读取 dokploy.config.json
   # 在 Dokploy 控制台点击 "Deploy"
   ```

### 服务资源限制

| 服务 | 内存 | CPU | 副本数 |
|------|------|-----|--------|
| Backend | 2Gi | 2 | 2 |
| Frontend | 512Mi | 0.5 | 1 |
| MySQL | 2Gi | 2 | 1 |
| Redis | 512Mi | 0.5 | 1 |

---

## 监控与告警

### 启动监控服务

```bash
# 启动所有监控组件
docker-compose -f docker-compose.monitoring.yml --profile monitoring up -d

# 查看服务状态
docker-compose -f docker-compose.monitoring.yml ps
```

### 访问监控界面

| 服务 | 地址 | 默认用户名 | 默认密码 |
|------|------|-----------|----------|
| Prometheus | http://localhost:9090 | - | - |
| Grafana | http://localhost:3001 | admin | admin |
| Loki | http://localhost:3100 | - | - |

### 告警规则

项目已配置以下告警规则 (见 `monitoring/prometheus/rules/alerts.yml`):

| 告警 | 阈值 | 级别 | 说明 |
|------|------|------|------|
| ServiceDown | 服务宕机 1 分钟 | Critical | 服务不可用 |
| HighErrorRate | 错误率 > 5% | Warning | 服务质量下降 |
| HighResponseTime | P95 > 1 秒 | Warning | 响应缓慢 |
| HighCPUUsage | CPU > 80% | Warning | CPU 压力高 |
| HighMemoryUsage | 内存 > 1GB | Warning | 内存使用高 |
| DiskSpaceLow | 可用空间 < 15% | Critical | 磁盘空间不足 |
| RedisDown | Redis 宕机 1 分钟 | Critical | 缓存不可用 |

---

## 备份与恢复

### 自动备份

使用定时任务配置自动备份:

```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点备份
0 2 * * * cd /home/hongfu/ai-resume && ./scripts/backup.sh
```

### 手动备份

```bash
# 运行备份脚本
./scripts/backup.sh

# 备份位置
# - /opt/backups/ai-resume/database/   - 数据库备份
# - /opt/backups/ai-resume/uploads/    - 上传文件
# - /opt/backups/ai-resume/exports/    - 导出文件
# - /opt/backups/ai-resume/config/     - 配置文件
```

### 恢复流程

```bash
# 1. 恢复数据库
gunzip < /opt/backups/ai-resume/database/backup_YYYYMMDD.sql.gz | \
  docker exec -i ai-resume-mysql mysql -u airesume -pairesume_password ai_resume

# 2. 恢复上传文件
tar -xzf /opt/backups/ai-resume/uploads/uploads_YYYYMMDD.tar.gz -C /home/hongfu/ai-resume/backend/

# 3. 恢复配置
cp /opt/backups/ai-resume/config/env_YYYYMMDD /home/hongfu/ai-resume/.env.production
```

---

## 健康检查

### 运行健康检查

```bash
# 基础健康检查
./scripts/health-check.sh

# 设置环境变量
export BACKEND_URL=http://localhost:8000
export FRONTEND_URL=http://localhost:3000
export ALERT_WEBHOOK=https://hooks.slack.com/...

./scripts/health-check.sh
```

### 健康检查项目

- ✅ Docker 容器运行状态
- ✅ Backend 健康端点
- ✅ Frontend 可访问性
- ✅ 磁盘空间使用
- ✅ 内存使用情况
- ✅ Docker 资源统计

---

## CI/CD 流水线

### GitHub Actions 工作流

项目配置了完整的 CI/CD 流水线 (`.github/workflows/ci-cd.yml`):

```
触发: push to main/develop, PR, manual

├── Backend Tests      # 后端测试
├── Frontend Tests     # 前端测试
├── Security Scan      # 安全扫描
├── Build & Push       # 构建并推送 Docker 镜像
├── Deploy Dokploy     # 部署到 Dokploy (可选)
└── Deploy Production  # 部署到生产环境
```

### 配置 GitHub Secrets

在 GitHub 仓库设置中配置以下 Secrets:

| Secret | 说明 | 必需 |
|--------|------|------|
| `DOKPLOY_URL` | Dokploy 服务器地址 | 可选 |
| `DOKPLOY_API_KEY` | Dokploy API 密钥 | 可选 |
| `PRODUCTION_HOST` | 生产服务器地址 | 必需 |
| `PRODUCTION_USER` | SSH 用户名 | 必需 |
| `SSH_PRIVATE_KEY` | SSH 私钥 | 必需 |
| `PRODUCTION_PATH` | 部署路径 | 可选 |
| `PRODUCTION_URL` | 生产环境 URL | 必需 |
| `SLACK_WEBHOOK` | Slack 通知 Webhook | 可选 |

---

## 常用命令

### Docker Compose 操作

```bash
# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 重启服务
docker-compose -f docker-compose.prod.yml restart

# 停止服务
docker-compose -f docker-compose.prod.yml down

# 查看资源使用
docker stats
```

### 监控操作

```bash
# 查看 Prometheus 指标
curl http://localhost:9090/api/v1/targets

# 查看 Loki 日志
curl http://localhost:3100/loki/api/v1/label/job/values

# Grafana 备份
docker exec ai-resume-grafana grafana-cli admin export-dashboard > backup.json
```

---

## 故障排查

### 问题: 服务无法启动

```bash
# 检查日志
docker-compose logs backend

# 检查配置
cat .env.production | grep -v "SECRET\|PASSWORD"

# 验证端口
sudo netstat -tlnp | grep -E '8000|3000|3306|6379'
```

### 问题: 监控数据不显示

```bash
# 检查 Prometheus
curl http://localhost:9090/api/v1/status/config

# 检查 targets
curl http://localhost:9090/api/v1/targets

# 重启监控服务
docker-compose -f docker-compose.monitoring.yml restart
```

### 问题: 备份失败

```bash
# 检查备份目录
ls -la /opt/backups/ai-resume/

# 手动运行备份
bash -x ./scripts/backup.sh

# 检查磁盘空间
df -h
```

---

## 安全建议

1. **密钥管理**
   - 定期更新 SECRET_KEY 和 JWT_SECRET
   - 使用环境变量存储敏感信息
   - 不要将 .env 文件提交到 Git

2. **访问控制**
   - 限制 Grafana 访问 IP
   - 修改默认密码
   - 启用 HTTPS

3. **日志安全**
   - 定期清理旧日志
   - 避免记录敏感信息
   - 使用日志脱敏

---

## 联系方式

如有问题，请联系 DevOps 团队或查看相关文档:
- `DEPLOYMENT.md` - 部署指南
- `DOCKER_DEPLOYMENT.md` - Docker 部署详情
- `CI_CD_GUIDE.md` - CI/CD 配置说明
