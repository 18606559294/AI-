# AI简历平台 - 后端启动脚本
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host "  AI简历平台 - 后端服务启动"            -ForegroundColor Cyan
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host ""

$backendDir = "D:\ai_resume\AI-\ai-resume-platform\backend"
$python = "$backendDir\venv\Scripts\python.exe"

# 检查Python
if (-not (Test-Path $python)) {
    Write-Host "错误: 未找到Python虚拟环境" -ForegroundColor Red
    Write-Host "路径: $python" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Python: $python" -ForegroundColor Green
Write-Host "后端目录: $backendDir" -ForegroundColor Green
Write-Host ""

Set-Location $backendDir

Write-Host "启动FastAPI服务..." -ForegroundColor Yellow
Write-Host "服务地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

& $python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
