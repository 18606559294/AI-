@echo off
chcp 65001 >nul
echo ========================================
echo   SSH 连接诊断
echo ========================================
echo.

echo [测试 1] 基本连通性...
ping -n 2 113.45.64.145
echo.

echo [测试 2] SSH 端口检测...
powershell -Command "Test-NetConnection -ComputerName 113.45.64.145 -Port 22 | Select-Object -Property ComputerName, RemotePort, TcpTestSucceeded"
echo.

echo [测试 3] 尝试详细 SSH 连接...
echo 请输入密码后按回车:
ssh -vvv root@113.45.64.145 "echo '连接成功'; uname -a"
echo.

echo ========================================
echo   如果连接失败，可能原因:
echo   1. 密码错误或多次失败被锁定
echo   2. SSH 服务配置问题
echo   3. 防火墙阻止
echo ========================================
echo.
pause
