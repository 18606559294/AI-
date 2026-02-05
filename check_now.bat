@echo off
chcp 65001 >nul
set SERVER=113.45.64.145
set USER=root

echo ========================================
echo   检查部署状态
echo ========================================
echo.

echo [1/5] 后端服务状态...
ssh %USER%@%SERVER% "supervisorctl status ai-resume-backend"
echo.

echo [2/5] Nginx 状态...
ssh %USER%@%SERVER% "systemctl is-active nginx"
echo.

echo [3/5] 端口监听情况...
ssh %USER%@%SERVER% "netstat -tlnp 2>/dev/null | grep -E '80|8000' || ss -tlnp | grep -E '80|8000'"
echo.

echo [4/5] 后端日志 (最后10行)...
ssh %USER%@%SERVER% "tail -10 /var/www/ai-resume/logs/backend.log 2>/dev/null || tail -10 /var/www/ai-resume/logs/*.log 2>/dev/null || echo '日志文件不存在'"
echo.

echo [5/5] 测试 API 健康检查...
ssh %USER%@%SERVER% "curl -s http://localhost:8000/docs 2>/dev/null | head -5 || curl -s http://localhost/api/v1/ 2>/dev/null | head -5"
echo.

echo ========================================
echo   访问地址: http://113.45.64.145
echo   API文档: http://113.45.64.145/docs
echo ========================================
echo.
pause
