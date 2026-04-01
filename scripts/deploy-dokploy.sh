#!/bin/bash
# AI Resume Platform - Dokploy 部署脚本
# 用途: 自动化部署到 Dokploy 服务器

set -e

# 配置变量
DOKPLOY_SERVER="113.45.64.145"
DOKPLOY_PORT="3000"
DOKPLOY_URL="http://${DOKPLOY_SERVER}:${DOKPLOY_PORT}"
DOKPLOY_EMAIL="641600780@qq.com"
DOKPLOY_PASSWORD="li780swsgbo"

PROJECT_NAME="ai-resume-platform"
DOMAIN="yourdomain.com"
BACKEND_DOMAIN="api.${DOMAIN}"
FRONTEND_DOMAIN="${DOMAIN}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🚀 AI Resume Platform - Dokploy 部署脚本"
echo "================================"

# 检查环境
check_environment() {
    echo "🔍 检查部署环境..."

    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker 未安装${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker 已安装${NC}"

    # 检查 Docker Compose (支持现代语法)
    if docker compose version &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose 已安装${NC}"
        docker compose version | head -1
    elif command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose 已安装${NC}"
        docker-compose --version | head -1
    else
        echo -e "${RED}❌ Docker Compose 未安装${NC}"
        exit 1
    fi

    # 检查配置文件
    if [ ! -f "dokploy.config.json" ]; then
        echo -e "${RED}❌ dokploy.config.json 不存在${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Dokploy 配置文件存在${NC}"

    # 检查环境变量文件
    if [ ! -f ".env.production" ]; then
        echo -e "${YELLOW}⚠️  .env.production 不存在，使用默认配置${NC}"
    fi
}

# 测试 Dokploy 连接
test_dokploy_connection() {
    echo ""
    echo "🔗 测试 Dokploy 服务器连接..."

    if curl -s -f "${DOKPLOY_URL}" > /dev/null; then
        echo -e "${GREEN}✅ Dokploy 服务器可访问${NC}"
        echo "   地址: ${DOKPLOY_URL}"
    else
        echo -e "${RED}❌ 无法连接到 Dokploy 服务器${NC}"
        echo "   请检查服务器地址和网络连接"
        exit 1
    fi
}

# 显示部署信息
show_deployment_info() {
    echo ""
    echo "📋 部署信息:"
    echo "   项目名称: ${PROJECT_NAME}"
    echo "   Dokploy URL: ${DOKPLOY_URL}"
    echo "   域名配置:"
    echo "     - 后端: ${BACKEND_DOMAIN}"
    echo "     - 前端: ${FRONTEND_DOMAIN}"
}

# 显示手动部署步骤
show_manual_steps() {
    echo ""
    echo "📝 手动部署步骤:"
    echo ""
    echo "1. 登录 Dokploy 管理面板:"
    echo "   URL: ${DOKPLOY_URL}"
    echo "   邮箱: ${DOKPLOY_EMAIL}"
    echo ""
    echo "2. 创建新应用:"
    echo "   - 点击「Create Application」"
    echo "   - 选择「Docker Compose」类型"
    echo "   - 输入应用名称: ${PROJECT_NAME}"
    echo ""
    echo "3. 配置 Git 仓库:"
    echo "   - 仓库 URL: https://github.com/18606559294/AI-.git"
    echo "   - 分支: main"
    echo "   - 构建类型: Docker Compose"
    echo ""
    echo "4. 配置环境变量:"
    echo "   - 上传 .env.production 文件内容"
    echo "   - 或手动设置环境变量"
    echo ""
    echo "5. 配置域名:"
    echo "   - 后端: ${BACKEND_DOMAIN}"
    echo "   - 前端: ${FRONTEND_DOMAIN}"
    echo ""
    echo "6. 启用监控:"
    echo "   - Prometheus: 端口 9090"
    echo "   - Grafana: 端口 3001"
    echo ""
    echo "7. 部署应用:"
    echo "   - 点击「Deploy」按钮"
    echo "   - 等待部署完成"
}

# 显示 SSH 配置步骤
show_ssh_config() {
    echo ""
    echo "🔑 SSH 密钥配置:"
    echo ""
    echo "1. 在 Dokploy 面板中:"
    echo "   - 进入「Settings」→「SSH Keys」"
    echo "   - 点击「Add SSH Key」"
    echo ""
    echo "2. 添加以下公钥:"
    echo "---"
    cat ~/.ssh/id_ed25519.pub
    echo "---"
    echo ""
    echo "3. 配置完成后，可通过 SSH 访问服务器:"
    echo "   ssh -i ~/.ssh/id_ed25519 root@${DOKPLOY_SERVER}"
}

# 显示健康检查步骤
show_health_check() {
    echo ""
    echo "🏥 部署后健康检查:"
    echo ""
    echo "1. 检查后端 API:"
    echo "   curl http://${BACKEND_DOMAIN}/health"
    echo ""
    echo "2. 检查前端:"
    echo "   curl http://${FRONTEND_DOMAIN}/"
    echo ""
    echo "3. 检查监控服务:"
    echo "   - Prometheus: http://${DOKPLOY_SERVER}:9090"
    echo "   - Grafana: http://${DOKPLOY_SERVER}:3001"
    echo ""
    echo "4. 运行本地健康检查:"
    echo "   ./scripts/health-check.sh"
}

# 主函数
main() {
    check_environment
    test_dokploy_connection
    show_deployment_info
    show_manual_steps
    show_ssh_config
    show_health_check

    echo ""
    echo "================================"
    echo -e "${GREEN}✅ 部署准备完成！${NC}"
    echo ""
    echo "请按照上述步骤在 Dokploy 面板中完成部署配置。"
    echo ""
}

# 运行主函数
main
