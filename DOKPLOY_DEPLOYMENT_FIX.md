# Dokploy 部署修复 - 执行指南

## 📋 当前状态总结

### ✅ 正常运行的服务
- **Backend容器**: 健康运行，本地访问响应时间0.002秒
- **Frontend容器**: 健康运行，外部可访问
- **Redis容器**: 健康运行，内部通信正常
- **Dokploy面板**: 可访问 (http://113.45.64.145:3000)

### ❌ 待解决问题
1. **Backend外部访问**: 被防火墙阻止 (端口8000)
2. **MySQL容器**: 端口3306被占用
3. **SSH密钥**: 未授权，无法直接访问服务器

## 🎯 快速修复步骤

### 第一步: 通过Dokploy面板添加SSH密钥

1. **登录Dokploy管理面板**
   ```
   URL: http://113.45.64.145:3000
   邮箱: 641600780@qq.com
   密码: 353980swsgbo
   ```

2. **导航到SSH Keys设置**
   - 点击左侧菜单的 "Settings" 或 "设置"
   - 选择 "SSH Keys" 选项卡

3. **添加新的SSH密钥**
   - 点击 "Add SSH Key" 或 "添加SSH密钥" 按钮
   - 填写以下信息:
     ```
     名称: AI_Agent_Deployment_Key
     密钥内容: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPhpLCnOdDAksakqgydJAqd3vL0rHvJ7I2N/SE6wHgu5 AI_Agent_Key
     ```
   - 点击 "Save" 或 "保存"

### 第二步: 配置防火墙规则

#### 方法A: 通过Dokploy Terminal (推荐)

1. **在Dokploy面板中打开Terminal**
   - 在项目页面找到 "Terminal" 或 "终端" 选项
   - 点击打开命令行界面

2. **执行防火墙配置命令**
   ```bash
   # 允许Backend API端口
   sudo ufw allow 8000/tcp

   # 允许Frontend端口 (如果尚未配置)
   sudo ufw allow 3000/tcp

   # 查看防火墙状态
   sudo ufw status verbose
   ```

#### 方法B: 通过SSH (完成第一步后)

1. **SSH连接到服务器**
   ```bash
   ssh -i ~/.ssh/id_ed25519 root@113.45.64.145
   ```

2. **执行防火墙配置**
   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw status verbose
   ```

#### 方法C: 通过云服务商控制台

1. **登录云服务商控制台** (阿里云/腾讯云/AWS等)
2. **找到安全组设置**
3. **添加入站规则**:
   - 类型: 自定义TCP
   - 端口: 8000
   - 来源: 0.0.0.0/0
   - 协议: TCP

### 第三步: 验证修复效果

1. **测试Backend外部访问**
   ```bash
   curl http://113.45.64.145:8000/health
   ```

2. **检查服务健康状态**
   ```bash
   # 运行验证脚本
   bash scripts/deployment-verification.sh
   ```

3. **预期结果**
   - Backend外部访问返回健康检查响应
   - 所有服务状态为 "✓ 通过"
   - 成功率达到 90% 以上

## 🔧 MySQL端口冲突解决

### 临时解决方案
如果MySQL容器启动失败，可以暂时使用外部数据库或更改端口映射:

```yaml
# 修改 docker-compose.prod.yml
services:
  db:
    ports:
      - "3307:3306"  # 使用3307端口避免冲突
```

### 永久解决方案
1. **查找占用3306端口的进程**
   ```bash
   netstat -tlnp | grep :3306
   ```

2. **停止冲突的服务** (如果不需要)

3. **重启MySQL容器**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d db
   ```

## 📊 验证清单

完成修复后，请确认以下项目:

- [ ] SSH密钥已添加到Dokploy面板
- [ ] 可以通过SSH连接到服务器
- [ ] UFW防火墙规则已配置 (端口8000)
- [ ] Backend外部访问可访问
- [ ] Frontend外部访问正常
- [ ] 所有Docker容器运行正常
- [ ] Dokploy管理面板功能正常

## 🚀 下一步计划

### 立即执行
1. 通过Dokploy面板添加SSH密钥
2. 配置防火墙规则
3. 验证Backend外部访问

### 短期任务
1. 解决MySQL容器端口冲突
2. 配置环境变量优化
3. 建立基础监控

### 中期目标
1. 配置自定义域名
2. 启用SSL证书 (HTTPS)
3. 建立CI/CD流水线

### 长期规划
1. 完善监控告警系统
2. 配置自动备份策略
3. 建立灾备方案

## 📞 技术支持

如有问题，请参考以下文档:
- `firewall-solution-guide.md` - 详细防火墙配置
- `devops-final-deployment-report.md` - 完整诊断报告
- `scripts/deployment-verification.sh` - 自动验证脚本

## ⏱️ 预计完成时间

- **SSH密钥配置**: 2-3分钟
- **防火墙配置**: 1-2分钟
- **验证测试**: 1分钟
- **总计**: 约5-10分钟

---

**生成时间**: 2026-04-06 06:30
**状态**: 等待执行
**优先级**: 🔴 高优先级