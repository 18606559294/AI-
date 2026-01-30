#!/bin/bash

# AI简历平台 - 开发环境启动脚本

set -e

echo "=========================================="
echo "    AI简历智能生成平台 - 开发环境启动"
echo "=========================================="

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在，正在从模板创建..."
    cp .env.example .env
    echo "请编辑 .env 文件配置必要的环境变量"
    echo ""
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 选择启动模式
echo ""
echo "请选择启动模式:"
echo "1) 完整启动 (后端 + 数据库 + Redis + Nginx)"
echo "2) 仅后端服务 (后端 + 数据库 + Redis)"
echo "3) 本地开发 (仅数据库和Redis，后端手动启动)"
echo ""
read -p "请输入选项 [1-3]: " choice

case $choice in
    1)
        echo "启动完整服务..."
        docker-compose up -d
        ;;
    2)
        echo "启动后端服务..."
        docker-compose up -d backend db redis
        ;;
    3)
        echo "启动数据库和缓存..."
        docker-compose up -d db redis
        echo ""
        echo "数据库和Redis已启动"
        echo "请手动启动后端: cd backend && uvicorn app.main:app --reload"
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "服务启动完成!"
echo ""
echo "后端 API: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo "前端页面: http://localhost (需要先构建Flutter Web)"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
echo "=========================================="
