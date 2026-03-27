# 部署快速指南

## 开发环境

### 启动开发服务器

```bash
# 后端
cd ~/ai-resume/backend
source venv/bin/activate
source .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端
cd ~/ai-resume/ai-resume-web
npm run dev
```

## Docker 部署

### 启动服务

```bash
cd ~/ai-resume

# 启动所有服务（开发环境）
docker-compose up -d

# 启动所有服务（生产环境）
docker-compose --profile production up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

### 服务访问

- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **前端**: http://localhost:3000
- **Nginx**: http://localhost:80（生产环境）

## 数据库操作

### SQLite（默认）

```bash
# 进入后端容器
docker-compose exec backend bash

# 备份数据库
cp data/ai_resume.db /app/backup/ai_resume_$(date +%Y%m%d).db
```

### MySQL（生产环境）

```bash
# 启动 MySQL
docker-compose --profile production up -d db

# 备份数据库
docker-compose exec db mysqldump -u airesume -pairesume_password ai_resume > backup.sql

# 恢复数据库
docker-compose exec -T db mysql -u airesume -pairesume_password ai_resume < backup.sql
```

## 日志查看

```bash
# 查看所有日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx

# 查看实时日志
docker-compose logs -f backend

# 查看最近 100 行
docker-compose logs --tail=100 backend
```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build

# 重启服务
docker-compose up -d

# 清理旧镜像
docker image prune -f
```

## 故障排查

### 服务无法启动

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs

# 重启服务
docker-compose restart backend
```

### 数据库连接失败

```bash
# 检查数据库状态
docker-compose ps db

# 查看 MySQL 日志
docker-compose logs db

# 进入数据库容器
docker-compose exec db bash
```

### 端口冲突

```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "9000:8000"  # 后端使用 9000
  - "4000:80"    # 前端使用 4000
```

## 性能优化

### 资源限制

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

### 日志轮转

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 备份策略

### 自动备份

```bash
# 添加到 crontab
0 2 * * * cd /path/to/ai-resume && ./scripts/backup.sh
```

### 手动备份

```bash
# 完整备份
./scripts/backup-all.sh
```

## 监控

### 健康检查

```bash
# 后端健康检查
curl http://localhost:8000/health

# 前端健康检查
curl http://localhost:3000
```

### 监控工具

- **Grafana** - 可视化监控
- **Prometheus** - 指标收集
- **ELK Stack** - 日志分析

## 安全

### SSL/TLS

```bash
# 使用 Let's Encrypt 获取证书
sudo certbot certonly --standalone -d yourdomain.com

# 配置 Nginx 使用 SSL
# 见 nginx.conf 配置
```

### 防火墙

```bash
# 只开放必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 故障恢复

### 数据丢失

```bash
# 从备份恢复
docker-compose exec db mysql -u airesume -pairesume_password ai_resume < backup.sql
```

### 服务崩溃

```bash
# 自动重启（已配置）
restart: unless-stopped

# 手动重启
docker-compose restart
```
