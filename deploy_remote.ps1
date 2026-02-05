# AI Resume Platform - Remote Deployment Script
$SERVER = "113.45.64.145"
$USER = "root"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI简历平台 - 远程部署脚本"           -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to execute remote command
function Remote-Exec {
    param([string]$Command)
    $result = ssh "$USER@$SERVER" $Command
    return $result
}

Write-Host "[1/6] 检查服务器状态..." -ForegroundColor Yellow
Remote-Exec "uname -a && free -h"
Write-Host ""

Write-Host "[2/6] 检查项目目录..." -ForegroundColor Yellow
Remote-Exec "ls -la /var/www/ai-resume/"
Write-Host ""

Write-Host "[3/6] 安装后端依赖..." -ForegroundColor Yellow
Remote-Exec "cd /var/www/ai-resume/backend && source venv/bin/activate 2>/dev/null || (python3.11 -m venv venv && source venv/bin/activate) && pip install --upgrade pip -q && pip install fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart email-validator aiosqlite -q"
Write-Host "依赖安装完成" -ForegroundColor Green
Write-Host ""

Write-Host "[4/6] 配置环境变量..." -ForegroundColor Yellow
Remote-Exec "cd /var/www/ai-resume/backend && export SECRET=\$(openssl rand -hex 32) && cat > .env << EOFILE
SECRET_KEY=\$SECRET
DEBUG=False
USE_SQLITE=True
DATABASE_URL=sqlite+aiosqlite:///./ai_resume.db
DEFAULT_AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=
OPENAI_API_KEY=
EOFILE"
Write-Host "环境配置完成" -ForegroundColor Green
Write-Host ""

Write-Host "[5/6] 重启服务..." -ForegroundColor Yellow
Remote-Exec "supervisorctl restart ai-resume-backend"
Remote-Exec "systemctl restart nginx"
Write-Host "服务已重启" -ForegroundColor Green
Write-Host ""

Write-Host "[6/6] 检查服务状态..." -ForegroundColor Yellow
Write-Host ""
Write-Host "--- 后端状态 ---" -ForegroundColor Cyan
Remote-Exec "supervisorctl status ai-resume-backend"
Write-Host ""
Write-Host "--- Nginx 状态 ---" -ForegroundColor Cyan
Remote-Exec "systemctl status nginx --no-pager | head -5"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  部署完成！"                          -ForegroundColor Green
Write-Host "  访问: http://113.45.64.145"          -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
