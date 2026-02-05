@echo off
chcp 65001 >nul
echo ========================================
echo   检查部署状态
echo ========================================
echo.

echo --- 后端服务状态 ---
ssh root@113.45.64.145 "supervisorctl status ai-resume-backend"
echo.

echo --- Nginx 状态 ---
ssh root@113.45.64.145 "systemctl status nginx --no-pager | head -5"
echo.

echo --- 端口监听情况 ---
ssh root@113.45.64.145 "netstat -tlnp | grep -E '80|8000'"
echo.

echo --- 后端日志 (最后10行) ---
ssh root@113.45.64.145 "tail -10 /var/www/ai-resume/logs/backend.log"
echo.

echo ========================================
echo   访问地址: http://113.45.64.145
echo   API文档: http://113.45.64.145/docs
echo ========================================
echo.
pause
