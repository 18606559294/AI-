# AI Resume Platform - 运维手册

> **完整运维指南和故障排查手册**
> 版本: 1.0.0
> 更新时间: 2026-04-02
> 维护者: DevOps 工程师

---

## 📋 目录

1. [系统架构](#系统架构)
2. [日常运维操作](#日常运维操作)
3. [监控和告警](#监控和告警)
4. [备份与恢复](#备份与恢复)
5. [故障排查](#故障排查)
6. [性能优化](#性能优化)
7. [安全管理](#安全管理)
8. [应急响应](#应急响应)

---

## 系统架构

### 服务组件

| 组件 | 容器名 | 端口 | 健康检查 | 说明 |
|------|--------|------|----------|------|
| Backend | ai-resume-backend | 8000 | `/health` | FastAPI 后端服务 |
| Frontend | ai-resume-frontend | 3000 | `/` | Nginx 托管的前端 |
| Redis | ai-resume-redis | 6379 | `redis-cli ping` | 缓存和队列 |
| MySQL | ai-resume-mysql | 3306 | `mysqladmin ping` | 生产数据库 (可选) |

### 监控组件

| 组件 | 端口 | 用途 |
|------|------|------|
| Prometheus | 9090 | 指标收集和存储 |
| Grafana | 3001 | 可视化监控面板 |
| Alertmanager | 9093 | 告警路由和通知 |
| Loki | 3100 | 日志聚合 |
| Promtail | - | 日志收集 |

---

## 日常运维操作

### 服务管理

#### 启动所有服务
```bash
# 使用 Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 启动监控服务
docker-compose -f docker-compose.monitoring.yml --profile monitoring up -d
```

#### 停止服务
```bash
# 停止应用服务
docker-compose -f docker-compose.prod.yml down

# 停止监控服务
docker-compose -f docker-compose.monitoring.yml down
```

#### 重启单个服务
```bash
# 重启后端
docker-compose -f docker-compose.prod.yml restart backend

# 重启前端
docker-compose -f docker-compose.prod.yml restart frontend

# 重启 Redis
docker-compose -f docker-compose.prod.yml restart redis
```

### 健康检查

#### 手动健康检查
```bash
# 运行完整健康检查
./scripts/health-check.sh

# 检查后端 API
curl http://localhost:8000/health

# 检查前端
curl http://localhost:3000/

# 检查 Redis
docker exec ai-resume-redis redis-cli ping
```

#### 查看服务状态
```bash
# 查看所有容器
docker ps

# 查看容器资源使用
docker stats

# 查看特定容器日志
docker logs -f ai-resume-backend
docker logs -f ai-resume-frontend
```

### 日志查看

#### 实时日志
```bash
# 后端日志
docker logs -f ai-resume-backend

# 前端日志
docker logs -f ai-resume-frontend

# 监控服务日志
docker logs -f prometheus
docker logs -f grafana
```

#### 日志文件位置
```
logs/backend/        # 后端应用日志
logs/frontend/       # 前端 Nginx 日志
logs/monitoring/     # 监控服务日志
```

---

## 监控和告警

### 监控面板访问

#### Grafana 仪表板
```
URL: http://localhost:3001
默认用户: admin
默认密码: admin

首次登录后请修改密码
```

#### Prometheus 界面
```
URL: http://localhost:9090
```

#### Alertmanager
```
URL: http://localhost:9093
```

### 关键指标

#### 应用指标
- **请求速率**: `http_requests_total`
- **错误率**: `http_errors_total`
- **响应时间**: `http_request_duration_seconds`
- **数据库连接**: `database_connections_active`

#### 系统指标
- **CPU 使用率**: `cpu_usage_percent`
- **内存使用**: `memory_usage_bytes`
- **磁盘 I/O**: `disk_io_seconds`
- **网络流量**: `network_receive_bytes`

### 告警规则

#### 关键告警
- **服务不可用**: 服务健康检查失败超过 2 分钟
- **高错误率**: 错误率超过 5% 持续 5 分钟
- **响应时间慢**: P95 响应时间超过 2 秒
- **资源告警**: CPU/内存/磁盘使用率超过 80%

#### 告警通知配置
编辑 `monitoring/alertmanager/config/alertmanager.yml`

---

## 备份与恢复

### 自动备份

#### 备份计划
```bash
# 每日自动备份 (凌晨 2:00)
0 2 * * * /path/to/scripts/backup.sh

# 备份保留 7 天
```

#### 手动备份
```bash
# 完整系统备份
./scripts/backup.sh

# 仅备份数据库
./scripts/backup-db.sh

# 测试备份恢复
./scripts/backup-test.sh
```

### 备份内容

#### 数据备份
- SQLite 数据库文件
- Redis 持久化数据
- 上传文件和导出文件

#### 配置备份
- 环境变量文件
- Docker Compose 配置
- 监控配置文件

### 恢复流程

#### 数据库恢复
```bash
# 停止服务
docker-compose -f docker-compose.prod.yml stop backend

# 恢复数据库
docker cp backup/ai_resume.db ai-resume-backend:/app/data/

# 重启服务
docker-compose -f docker-compose.prod.yml start backend
```

#### 完整系统恢复
```bash
# 1. 停止所有服务
docker-compose -f docker-compose.prod.yml down

# 2. 恢复配置文件
cp backup/.env.production .
cp backup/docker-compose.prod.yml .

# 3. 恢复数据卷
docker run --rm -v ai-resume-backend-data:/data -v $(pwd)/backup:/backup \
  alpine tar xzf /backup/data.tar.gz -C /

# 4. 重启服务
docker-compose -f docker-compose.prod.yml up -d
```

---

## 故障排查

### 常见问题

#### 1. 服务启动失败

**症状**: 容器无法启动或立即退出

**排查步骤**:
```bash
# 查看容器日志
docker logs ai-resume-backend

# 检查配置文件
cat .env.production

# 验证端口占用
netstat -tulpn | grep 8000

# 检查磁盘空间
df -h
```

**常见原因**:
- 配置文件错误
- 端口被占用
- 磁盘空间不足
- 依赖服务未启动

**解决方案**:
```bash
# 修复配置后重启
docker-compose -f docker-compose.prod.yml restart backend

# 清理无用容器和镜像
docker system prune -a

# 清理未使用的卷
docker volume prune
```

#### 2. API 响应慢

**症状**: 请求响应时间过长

**排查步骤**:
```bash
# 检查资源使用
docker stats ai-resume-backend

# 查看 Prometheus 指标
curl http://localhost:9090/api/v1/query?query=http_request_duration_seconds

# 检查数据库连接
docker exec ai-resume-backend python -c "from app.database import engine; print(engine.pool.status())"
```

**常见原因**:
- 数据库查询慢
- 资源限制
- 网络延迟
- 锁竞争

**解决方案**:
```bash
# 增加资源限制
# 编辑 docker-compose.prod.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

# 重启服务
docker-compose -f docker-compose.prod.yml up -d backend
```

#### 3. 内存泄漏

**症状**: 内存使用持续增长

**排查步骤**:
```bash
# 监控内存使用
docker stats ai-resume-backend --format "table {{.MemUsage}}"

# 检查进程内存
docker exec ai-resume-backend ps aux

# 分析内存使用
docker exec ai-resume-backend python -m memory_profiler app/main.py
```

**解决方案**:
```bash
# 定期重启服务 (临时方案)
docker-compose -f docker-compose.prod.yml restart backend

# 优化代码和配置 (永久方案)
# 设置合理的资源限制
# 配置自动重启策略
```

#### 4. Redis 连接问题

**症状**: 无法连接到 Redis

**排查步骤**:
```bash
# 检查 Redis 状态
docker exec ai-resume-redis redis-cli ping

# 查看 Redis 日志
docker logs ai-resume-redis

# 测试连接
docker exec ai-resume-backend python -c "import redis; r=redis.Redis('redis'); print(r.ping())"
```

**解决方案**:
```bash
# 重启 Redis
docker-compose -f docker-compose.prod.yml restart redis

# 检查配置
docker exec ai-resume-redis redis-cli CONFIG GET bind

# 清理连接
docker exec ai-resume-redis redis-cli CLIENT LIST
docker exec ai-resume-redis redis-cli CLIENT KILL <addr>
```

### 紧急故障处理

#### 服务完全不可用

**应急步骤**:
1. **立即诊断** (2 分钟)
   ```bash
   # 检查所有容器
   docker ps -a

   # 查看错误日志
   docker logs --tail 100 ai-resume-backend
   ```

2. **快速恢复** (5 分钟)
   ```bash
   # 重启所有服务
   docker-compose -f docker-compose.prod.yml restart

   # 如果重启失败，重新部署
   docker-compose -f docker-compose.prod.yml down
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **验证恢复** (3 分钟)
   ```bash
   # 运行健康检查
   ./scripts/health-check.sh

   # 测试 API
   curl http://localhost:8000/health
   ```

---

## 性能优化

### 容器资源优化

#### 资源限制配置
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

#### 性能调优
```bash
# 查看资源使用
docker stats --no-stream

# 优化容器数量
docker-compose -f docker-compose.prod.yml up -d --scale backend=2
```

### 数据库优化

#### SQLite 优化
```python
# 在应用配置中
DATABASE_URL = "sqlite+aiosqlite:///./data/ai_resume.db"
# 添加以下参数:
# ?check_same_thread=False&journal_mode=WAL&synchronous=NORMAL
```

#### Redis 优化
```bash
# 设置最大内存
docker exec ai-resume-redis redis-cli CONFIG SET maxmemory 256mb

# 设置淘汰策略
docker exec ai-resume-redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### 应用优化

#### 缓存策略
```python
# 启用响应缓存
from functools import lru_cache

@lru_cache(maxsize=100)
def get_expensive_operation(param):
    # ...
    pass
```

#### 连接池配置
```python
# 数据库连接池
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800
)
```

---

## 安全管理

### 访问控制

#### API 访问限制
```bash
# 在 nginx.conf 中配置
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

#### 管理端口保护
```yaml
# 仅本地访问监控服务
ports:
  - "127.0.0.1:9090:9090"  # Prometheus
  - "127.0.0.1:3001:3001"  # Grafana
```

### 数据安全

#### 敏感数据加密
```bash
# 使用 Docker secrets
echo "db_password" | docker secret create db_password -

# 在 docker-compose.yml 中引用
secrets:
  db_password:
    external: true
```

#### SSL/TLS 配置
```nginx
# nginx.conf
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

### 安全审计

#### 日志审计
```bash
# 定期检查访问日志
tail -f /var/log/nginx/access.log | grep -v "200\|301\|302"

# 检查异常请求
grep "POST" /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -20
```

#### 安全扫描
```bash
# 容器镜像扫描
docker scout cves ai-resume-backend

# 依赖漏洞检查
pip install safety
safety check --file requirements.txt
```

---

## 应急响应

### 告警级别

#### 🔴 P0 - 紧急
- 服务完全不可用
- 数据丢失风险
- 安全漏洞被利用

**响应时间**: 15 分钟内
**升级时间**: 30 分钟内

#### 🟡 P1 - 高优先级
- 服务降级
- 性能严重下降
- 部分功能不可用

**响应时间**: 1 小时内
**升级时间**: 4 小时内

#### 🟢 P2 - 中优先级
- 轻微性能问题
- 非关键功能故障
- 资源使用告警

**响应时间**: 1 工作日内
**升级时间**: 3 工作日内

### 应急联系人

| 角色 | 姓名 | 联系方式 | 负责范围 |
|------|------|----------|----------|
| DevOps 工程师 | - | - | 基础设施、部署、监控 |
| 后端负责人 | - | - | 后端服务、API |
| 前端负责人 | - | - | 前端服务、UI |
| CTO | - | - | 技术决策、重大问题 |

### 应急流程

#### 1. 问题识别
- 监控告警触发
- 用户报告问题
- 定期检查发现

#### 2. 初步评估
- 确定影响范围
- 评估严重程度
- 通知相关人员

#### 3. 响应行动
- 执行应急方案
- 隔离问题服务
- 启用备用系统

#### 4. 问题解决
- 修复根本原因
- 恢复正常服务
- 验证修复效果

#### 5. 事后总结
- 编写事故报告
- 更新运维文档
- 改进应急预案

---

## 附录

### 快速命令参考

```bash
# 健康检查
./scripts/health-check.sh

# 备份数据
./scripts/backup.sh

# 查看日志
docker logs -f ai-resume-backend

# 重启服务
docker-compose -f docker-compose.prod.yml restart

# 查看资源使用
docker stats

# 进入容器
docker exec -it ai-resume-backend bash
```

### 重要端口

| 服务 | 端口 | 用途 |
|------|------|------|
| Backend API | 8000 | 后端 API |
| Frontend | 3000 | 前端 Web |
| Redis | 6379 | 缓存服务 |
| Prometheus | 9090 | 监控指标 |
| Grafana | 3001 | 监控面板 |
| Alertmanager | 9093 | 告警服务 |

### 相关文档

- `DEVOPS_GUIDE.md` - DevOps 操作指南
- `DEPLOYMENT_CHECKLIST.md` - 部署检查清单
- `ALERTING_GUIDE.md` - 告警配置指南
- `DOKPLOY_DEPLOYMENT_GUIDE.md` - Dokploy 部署指南

---

**文档版本**: 1.0.0
**最后更新**: 2026-04-02
**维护者**: DevOps 工程师 (Agent 29126157-6833-4f1e-94bd-6493bd95d3f2)
