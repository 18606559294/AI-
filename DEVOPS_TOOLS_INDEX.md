# AI Resume Platform - DevOps 工具完整索引

**版本**: v1.0 Complete  
**更新时间**: 2026-04-06 07:35  
**工程师**: AI DevOps Agent (29126157-6833-4f1e-94bd-6493bd95d3f2)

---

## 🛠️ 主要管理工具

### 综合部署管理 ⭐
```bash
./ai-resume-deploy.sh              # 一键式部署管理工具
```

**功能**: 服务启动/停止/重启、日志查看、健康检查、问题诊断  
**使用场景**: 日常运维、服务管理、状态查询  
**命令示例**:
```bash
./ai-resume-deploy.sh status       # 查看完整状态
./ai-resume-deploy.sh restart     # 重启所有服务
./ai-resume-deploy.sh logs        # 查看所有日志
./ai-resume-deploy.sh diagnose    # 运行完整诊断
```

---

## 📊 监控和诊断工具

### 1. 快速状态监控 ⭐
```bash
scripts/quick-monitor.sh           # 快速状态监控
```

**功能**: 实时显示容器状态、资源使用、服务访问  
**特点**: 简洁输出、彩色显示、快速执行  
**使用频率**: 每日检查

### 2. 详细状态仪表板
```bash
scripts/status-dashboard.sh        # 详细状态仪表板
```

**功能**: 实时监控面板、自动刷新、详细指标  
**特点**: 界面友好、信息全面、自动更新  
**使用频率**: 持续监控

### 3. 性能监控工具 ⭐
```bash
scripts/performance-monitor.sh     # 性能监控工具
```

**功能**: 系统性能监控、API性能测试、资源趋势分析  
**子命令**:
- `monitor` - 实时性能监控
- `test` - API性能测试
- `trends` - 资源使用趋势
- `alerts` - 性能告警检查
- `report` - 生成性能报告

**使用频率**: 性能分析时

### 4. 完整部署验证
```bash
scripts/deployment-verification.sh # 完整部署验证
```

**功能**: 16项检查、详细报告、成功率统计  
**检查项目**: 容器状态、端口监听、本地/外部访问、资源使用  
**使用频率**: 部署后验证

### 5. Backend深度诊断
```bash
scripts/backend-diagnosis.sh      # Backend深度诊断
```

**功能**: Backend服务问题诊断、日志分析、配置检查  
**使用场景**: Backend问题排查

---

## 🔧 维护和修复工具

### 6. MySQL容器修复 ⭐
```bash
scripts/mysql-container-fix.sh     # MySQL容器修复
```

**功能**: 解决端口3306冲突、3种修复方案  
**解决方案**:
- 方案1: 更改容器端口映射
- 方案2: 停止冲突服务
- 方案3: 使用外部MySQL

**使用场景**: MySQL容器启动失败

### 7. 外部访问验证 ⭐
```bash
scripts/verify-external-access.sh    # 外部访问验证
```

**功能**: 4项验证测试、响应时间测试、成功率计算  
**检查项目**: 端口连通性、API端点、响应时间、成功率  
**使用频率**: 防火墙配置后验证 (立即使用)  

**特点**:
- 自动化测试所有外部访问端点
- 响应时间性能测试
- 详细的故障排查建议
- 彩色输出和进度显示

### 8. 防火墙配置验证 (旧版)
```bash
scripts/post-firewall-verification.sh # 防火墙配置验证
```

**功能**: 6项检查、验证防火墙配置效果、成功率计算  
**检查项目**: Backend/Frontend外部访问、API端点、容器状态  
**使用频率**: 防火墙配置后验证

### 8. 数据备份管理 ⭐
```bash
scripts/backup-manager.sh          # 数据备份管理
```

**功能**: 自动化备份、配置备份、数据库备份、定时备份  
**子命令**:
- `backup` - 执行完整备份
- `restore` - 恢复指定备份
- `list` - 列出所有备份
- `cron` - 设置定时备份

**备份内容**: 配置文件、数据库数据、Docker配置、日志文件  
**使用频率**: 每日自动备份

### 9. 日志分析工具 ⭐
```bash
scripts/log-analyzer.sh            # 日志分析工具
```

**功能**: 容器日志分析、访问日志分析、系统日志分析、报告生成  
**子命令**:
- `container` - 分析指定容器日志
- `access` - 分析访问日志
- `system` - 分析系统日志
- `report` - 生成分析报告
- `monitor` - 实时日志监控
- `all` - 分析所有容器

**使用频率**: 问题排查、性能分析

---

## 🚀 部署和配置工具

### 10. 监控系统部署
```bash
scripts/deploy-monitoring-system.sh # 监控系统部署
```

**功能**: 自动化部署基础监控、健康检查、资源监控、告警通知  
**包含**: systemd服务、定时任务、配置文件、告警脚本  
**使用场景**: 初始部署、监控体系建设

### 11. Dokploy部署监控
```bash
scripts/monitor-dokploy-deployment.sh # Dokploy部署监控
```

**功能**: 实时监控Dokploy部署状态、服务健康检查  
**使用场景**: Dokploy平台监控

---

## 📚 快速参考指南

### 日常运维

#### 查看服务状态
```bash
# 方式1: 使用主要工具
./ai-resume-deploy.sh status

# 方式2: 使用快速监控
bash scripts/quick-monitor.sh

# 方式3: 使用Docker命令
docker ps --filter "name=ai-resume"
```

#### 重启服务
```bash
# 重启所有服务
./ai-resume-deploy.sh restart

# 重启特定服务
docker restart ai-resume-backend
```

#### 查看日志
```bash
# 查看所有服务日志
./ai-resume-deploy.sh logs

# 查看Backend日志
./ai-resume-deploy.sh logs-backend

# 实时监控日志
bash scripts/log-analyzer.sh monitor backend
```

### 问题排查

#### 完整诊断
```bash
# 使用部署验证脚本
bash scripts/deployment-verification.sh

# 使用部署工具诊断
./ai-resume-deploy.sh diagnose

# Backend专门诊断
bash scripts/backend-diagnosis.sh
```

#### 性能分析
```bash
# 性能测试
bash scripts/performance-monitor.sh test

# 性能监控
bash scripts/performance-monitor.sh monitor

# 趋势分析
bash scripts/performance-monitor.sh trends
```

#### 日志分析
```bash
# 容器日志分析
bash scripts/log-analyzer.sh container backend 1000

# 系统日志分析
bash scripts/log-analyzer.sh system

# 生成分析报告
bash scripts/log-analyzer.sh report
```

### 备份和恢复

#### 执行备份
```bash
# 手动备份
bash scripts/backup-manager.sh backup

# 查看备份列表
bash scripts/backup-manager.sh list

# 恢复备份
bash scripts/backup-manager.sh restore ai-resume-backup-20260406_073000
```

#### 设置自动备份
```bash
# 设置定时备份
bash scripts/backup-manager.sh cron

# 查看备份日志
tail -f /var/log/ai-resume-backup.log
```

---

## 🎯 使用场景指南

### 场景1: 日常状态检查
```bash
bash scripts/quick-monitor.sh
```

### 场景2: 服务异常处理
```bash
# 1. 快速诊断
./ai-resume-deploy.sh diagnose

# 2. 查看详细日志
./ai-resume-deploy.sh logs-backend

# 3. 分析日志
bash scripts/log-analyzer.sh container backend

# 4. 性能检查
bash scripts/performance-monitor.sh test
```

### 场景3: 防火墙配置后验证
```bash
bash scripts/post-firewall-verification.sh
```

### 场景4: MySQL容器修复
```bash
bash scripts/mysql-container-fix.sh
# 选择方案1: 更改端口映射
```

### 场景5: 监控系统部署
```bash
bash scripts/deploy-monitoring-system.sh
systemctl start ai-resume-monitor
```

### 场景6: 完整备份和恢复
```bash
# 备份
bash scripts/backup-manager.sh backup

# 恢复
bash scripts/backup-manager.sh restore <backup-name>
```

---

## 📊 当前部署状态

### 容器状态
```
✅ ai-resume-backend  运行中 (本地: 0.002s, 外部: 被阻止)
✅ ai-resume-frontend 运行中 (外部: 可访问)
✅ ai-resume-redis    运行中 (内部: 正常)
❌ ai-resume-db       未启动 (端口冲突)
```

### 主要问题
- **Backend外部访问**: 被防火墙阻止 (8000端口)
- **MySQL容器**: 端口3306冲突

### 解决方案
- **防火墙配置**: 参考 `FIREWALL_EXECUTION_CHECKLIST.md`
- **MySQL修复**: 运行 `bash scripts/mysql-container-fix.sh`

---

## 🔗 相关文档

### 立即使用 ⭐
- `QUICK_REFERENCE.md` - 快速参考指南
- `DEPLOYMENT_GUIDE.md` - 完整部署管理指南
- `DEVOPS_TOOLS_GUIDE.md` - DevOps工具使用指南

### 配置指导
- `FIREWALL_EXECUTION_CHECKLIST.md` - 防火墙执行清单
- `CLOUD_CONSOLE_FIREWALL_GUIDE.md` - 云控制台配置

### 规划文档
- `DEVOPS_ROADMAP.md` - 5阶段发展路线图
- `DEVOPS_FINAL_STATUS_REPORT.md` - 最终状态报告

---

## 💡 使用技巧

### 工具组合使用
```bash
# 日常检查组合
bash scripts/quick-monitor.sh && bash scripts/performance-monitor.sh test

# 完整诊断组合
./ai-resume-deploy.sh diagnose && bash scripts/deployment-verification.sh

# 备份和恢复组合
bash scripts/backup-manager.sh backup && ./ai-resume-deploy.sh restart
```

### 定时任务设置
```bash
# 添加到crontab
crontab -e

# 每小时状态检查
0 * * * * bash /home/hongfu/ai-resume/scripts/quick-monitor.sh >> /var/log/status-check.log 2>&1

# 每日凌晨2点备份
0 2 * * * bash /home/hongfu/ai-resume/scripts/backup-manager.sh backup

# 每周日凌晨3点性能报告
0 3 * * 0 bash /home/hongfu/ai-resume/scripts/performance-monitor.sh report
```

---

## 🎓 最佳实践

### 日常运维
1. **每日**: 运行快速状态检查
2. **每周**: 清理旧备份、性能分析
3. **每月**: 更新安全补丁、完整备份

### 故障处理
1. **诊断**: 使用 `./ai-resume-deploy.sh diagnose`
2. **分析**: 使用日志分析工具
3. **修复**: 使用对应的修复工具
4. **验证**: 运行完整验证测试

### 性能优化
1. **监控**: 使用性能监控工具
2. **分析**: 查看资源使用趋势
3. **优化**: 根据分析结果优化配置

---

**索引版本**: v1.0 Complete  
**维护**: AI DevOps Agent  
**状态**: 生产就绪

*所有工具已准备完毕，随时可以投入使用*