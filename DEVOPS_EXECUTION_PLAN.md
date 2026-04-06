# DevOps 执行计划 - 防火墙配置后

**更新时间**: 2026-04-06 08:07 UTC+8
**当前状态**: Phase 2 95% | Phase 3 准备就绪
**工程师**: AI DevOps Agent (29126157-6833-4f1e-94bd-6493bd95d3f2)

---

## 🎯 总体路线图

```
当前: Phase 2 (95%) ──→ Phase 3 ──→ Phase 4 ──→ Phase 5
       ↓                    ↓            ↓            ↓
    防火墙配置          基础完善      自动化集成    优化扩展
```

---

## 📋 防火墙配置后立即执行 (30分钟)

### 步骤1: 验证外部访问 (2分钟)
```bash
bash scripts/verify-external-access.sh
```

**预期结果**:
- ✅ Backend (8000) 外部可访问
- ✅ 所有API端点响应正常
- ✅ 响应时间 < 500ms

### 步骤2: 修复 MySQL 容器 (10分钟)
```bash
bash scripts/mysql-container-fix.sh
# 选择方案1: 更改端口映射到 3307
```

### 步骤3: 部署监控系统 (15分钟)
```bash
# 1. 部署监控服务
bash scripts/deploy-monitoring-system.sh

# 2. 启动监控
systemctl start ai-resume-monitor

# 3. 设置开机自启
systemctl enable ai-resume-monitor

# 4. 验证监控状态
systemctl status ai-resume-monitor
```

### 步骤4: 配置自动备份 (5分钟)
```bash
# 1. 配置备份系统
bash scripts/setup-backup-automation.sh

# 2. 测试备份
/backup/ai-resume/backup.sh

# 3. 查看备份文件
/backup/ai-resume/list.sh
```

### 步骤5: 完整验证 (3分钟)
```bash
./ai-resume-deploy.sh diagnose
bash scripts/quick-monitor.sh
```

---

## 🔧 详细操作指南

### 1. 防火墙配置步骤

#### 阿里云 ECS
```bash
# 1. 登录控制台
https://ecs.console.aliyun.com

# 2. 导航路径
实例列表 → 找到 113.45.64.145 → 安全组 → 配置规则 → 添加安全组规则

# 3. 规则配置
端口范围: 8000/8000
授权对象: 0.0.0.0/0
协议类型: TCP
优先级: 1
描述: Backend API

# 4. 保存并等待1-2分钟生效
```

#### 腾讯云 CVM
```bash
# 1. 登录控制台
https://console.cloud.tencent.com/cvm

# 2. 导航路径
实例 → 找到 113.45.64.145 → 安全组 → 修改规则 → 添加入站规则

# 3. 规则配置
端口: 8000
来源: 0.0.0.0/0
协议: TCP
策略: 允许

# 4. 保存并等待1-2分钟生效
```

#### 验证命令
```bash
# 测试外部访问
curl http://113.45.64.145:8000/health

# 预期响应
# {"status":"healthy","version":"1.0.0"}

# 或运行完整验证
bash scripts/verify-external-access.sh
```

---

### 2. MySQL 修复方案详解

#### 方案1: 更改端口映射 (推荐)
```bash
bash scripts/mysql-container-fix.sh
# 选择: 1

# 优点: 不影响其他服务
# 缺点: 需要更新连接配置
```

#### 方案2: 停止冲突服务
```bash
bash scripts/mysql-container-fix.sh
# 选择: 2

# 优点: 保持默认端口
# 缺点: 可能影响其他MySQL实例
```

#### 方案3: 使用外部MySQL
```bash
bash scripts/mysql-container-fix.sh
# 选择: 3

# 适用于: 生产环境有独立数据库服务器
```

---

### 3. 监控系统验证

```bash
# 检查服务状态
systemctl status ai-resume-monitor

# 查看监控日志
tail -f ~/ai-resume-monitoring/logs/monitor.log

# 查看告警记录
cat ~/ai-resume-monitoring/logs/alerts.log

# 启动实时仪表板
~/ai-resume-monitoring/scripts/dashboard.sh
```

**预期输出**:
```
● ai-resume-monitor.service - AI Resume Platform Monitoring Service
   Loaded: loaded (/etc/systemd/system/ai-resume-monitor.service; enabled)
   Active: active (running) since Mon 2026-04-06 08:15:00 UTC; 5s ago
```

---

### 4. 备份系统验证

```bash
# 查看备份列表
/backup/ai-resume/list.sh

# 检查定时任务
crontab -l | grep ai-resume

# 查看备份日志
tail -f /backup/ai-resume/backup.log
```

**预期配置**:
```
# AI Resume Platform 自动备份
0 2 * * * /backup/ai-resume/backup.sh
```

---

## 📊 完成标准检查清单

### Phase 3 完成标准
- [ ] **防火墙配置**: Backend外部访问可访问 (8000端口)
- [ ] **MySQL修复**: MySQL容器正常运行，端口冲突解决
- [ ] **监控系统**: 监控服务运行中，自动检查启用
- [ ] **自动备份**: 备份系统配置完成，定时任务设置
- [ ] **健康检查**: 所有健康检查通过，无错误告警

### 验证命令组合
```bash
# 完整验证脚本
./ai-resume-deploy.sh diagnose && \
bash scripts/verify-external-access.sh && \
systemctl status ai-resume-monitor && \
/backup/ai-resume/list.sh
```

---

## 🚨 故障排查快速参考

### 问题: Backend外部访问失败
```bash
# 1. 检查防火墙配置
bash scripts/verify-external-access.sh

# 2. 查看Backend日志
docker logs ai-resume-backend --tail 50

# 3. 检查容器状态
docker ps | grep backend

# 4. 测试本地访问
curl http://localhost:8000/health

# 5. 查看防火墙规则
sudo ufw status
```

### 问题: MySQL容器启动失败
```bash
# 1. 查看错误日志
docker logs ai-resume-mysql --tail 50

# 2. 检查端口占用
sudo netstat -tlnp | grep 3306

# 3. 运行修复工具
bash scripts/mysql-container-fix.sh

# 4. 手动测试连接
docker compose exec mysql mysql -u root -p
```

### 问题: 监控服务不运行
```bash
# 1. 检查服务状态
systemctl status ai-resume-monitor

# 2. 查看服务日志
journalctl -u ai-resume-monitor -n 50

# 3. 手动运行监控脚本
~/ai-resume-monitoring/scripts/main-monitor.sh

# 4. 重启服务
systemctl restart ai-resume-monitor
```

---

## 🎓 下一步规划

### Phase 3 完成后 → Phase 4

```
Phase 4: 自动化集成 (预计1-2周)
├── CI/CD流水线集成
│   ├── GitHub Actions配置
│   ├── 自动化测试
│   └── 自动部署
├── 域名和SSL配置
│   ├── 域名解析
│   ├── Let's Encrypt证书
│   └── HTTPS强制跳转
└── 性能优化
    ├── 缓存策略
    ├── CDN配置
    └── 数据库优化
```

---

## 📚 相关文档索引

### 快速参考
- `QUICK_START_NEXT_STEPS.md` - 快速开始
- `PHASE3_DEPLOYMENT_GUIDE.md` - Phase 3指南
- `QUICK_REFERENCE.md` - 快速参考

### 工具和脚本
- `DEVOPS_TOOLS_INDEX.md` - 16个工具完整索引
- `scripts/` - 所有自动化脚本

### 配置和部署
- `docker-compose.prod.yml` - 生产环境配置
- `FIREWALL_EXECUTION_CHECKLIST.md` - 防火墙清单

### 监控和运维
- `MONITORING_ALERTING_PLAN.md` - 监控告警计划
- `DEVOPS_ROADMAP.md` - 完整路线图

---

## 💡 快速命令参考

```bash
# 状态监控
bash scripts/quick-monitor.sh

# 完整诊断
./ai-resume-deploy.sh diagnose

# 外部访问验证
bash scripts/verify-external-access.sh

# 性能监控
bash scripts/performance-monitor.sh monitor

# 日志分析
bash scripts/log-analyzer.sh container backend

# 备份管理
bash scripts/backup-manager.sh backup
```

---

**状态**: 🟡 等待防火墙配置 | ⚡ 所有脚本准备就绪 | 📋 执行计划完成
