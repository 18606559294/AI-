@echo off
chcp 65001 >nul
echo ========================================
echo   AI简历平台 - 远程部署脚本
echo ========================================
echo.

echo [1/6] 检查服务器状态...
ssh root@113.45.64.145 "uname -a && free -h"
echo.

echo [2/6] 检查项目目录...
ssh root@113.45.64.145 "ls -la /var/www/ai-resume/"
echo.

echo [3/6] 安装后端依赖...
ssh root@113.45.64.145 "cd /var/www/ai-resume/backend && source venv/bin/activate 2>/dev/null || (python3.11 -m venv venv && source venv/bin/activate) && pip install --upgrade pip -q && pip install fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart email-validator aiosqlite -q"
echo 依赖安装完成
echo.

echo [4/6] 配置环境变量...
ssh root@113.45.64.145 "cd /var/www/ai-resume/backend && openssl rand -hex 32 > /tmp/secret.txt && cat > .env << EOFILE
SECRET_KEY=$(cat /tmp/secret.txt)
DEBUG=False
USE_SQLITE=True
DATABASE_URL=sqlite+aiosqlite:///./ai_resume.db
DEFAULT_AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=
OPENAI_API_KEY=
EOFILE
rm /tmp/secret.txt"
echo 环境配置完成
echo.

echo [5/6] 重启服务...
ssh root@113.45.64.145 "supervisorctl restart ai-resume-backend"
ssh root@113.45.64.145 "systemctl restart nginx"
echo 服务已重启
echo.

echo [6/6] 检查服务状态...
echo.
echo --- 后端状态 ---
ssh root@113.45.64.145 "supervisorctl status ai-resume-backend"
echo.
echo --- Nginx 状态 ---
ssh root@113.45.64.145 "systemctl status nginx --no-pager | head -5"
echo.

echo ========================================
echo   部署完成！
echo   访问: http://113.45.64.145
echo ========================================
echo.
pause
