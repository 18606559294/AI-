#!/bin/bash

# AI简历应用 Appium 自动化测试运行脚本

echo "=========================================="
echo "AI简历应用 - Appium 全面自动化测试"
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 检查设备连接
echo ""
echo "📱 检查设备连接..."
DEVICE=$(adb devices | grep -w "device" | head -1 | cut -f1)
if [ -z "$DEVICE" ]; then
    echo "❌ 未检测到已连接的Android设备"
    echo "请确保:"
    echo "  1. USB已连接"
    echo "  2. 开发者模式已开启"
    echo "  3. USB调试已授权"
    exit 1
fi
echo "✅ 检测到设备: $DEVICE"

# 检查应用是否安装
echo ""
echo "📦 检查应用安装状态..."
APP_INSTALLED=$(adb shell pm list packages | grep "com.example.ai_resume_app")
if [ -z "$APP_INSTALLED" ]; then
    echo "❌ 应用未安装，请先安装应用"
    exit 1
fi
echo "✅ 应用已安装"

# 检查Appium
echo ""
echo "🔧 检查Appium状态..."
APPIUM_VERSION=$(appium --version 2>/dev/null)
if [ -z "$APPIUM_VERSION" ]; then
    echo "❌ Appium未安装"
    exit 1
fi
echo "✅ Appium版本: $APPIUM_VERSION"

# 启动Appium服务器 (后台)
echo ""
echo "🚀 启动Appium服务器..."
pkill -f "appium" 2>/dev/null || true
sleep 1
appium --address 127.0.0.1 --port 4723 --allow-cors > appium_server.log 2>&1 &
APPIUM_PID=$!
echo "✅ Appium服务器已启动 (PID: $APPIUM_PID)"

# 等待服务器就绪
echo ""
echo "⏳ 等待Appium服务器就绪..."
sleep 5

# 检查服务器是否运行
if ! curl -s http://127.0.0.1:4723/status > /dev/null; then
    echo "❌ Appium服务器启动失败"
    cat appium_server.log
    exit 1
fi
echo "✅ Appium服务器就绪"

# 激活虚拟环境并运行测试
echo ""
echo "🧪 开始运行自动化测试..."
echo "=========================================="

source venv/bin/activate

# 运行测试并生成HTML报告
pytest test_full_app.py \
    -v \
    --html=report.html \
    --self-contained-html \
    --capture=no \
    2>&1 | tee test_output.log

TEST_RESULT=$?

# 停止Appium服务器
echo ""
echo "🛑 停止Appium服务器..."
kill $APPIUM_PID 2>/dev/null || true

# 显示测试结果
echo ""
echo "=========================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ 所有测试通过!"
else
    echo "⚠️  部分测试失败"
fi
echo "=========================================="
echo ""
echo "📊 测试报告: $SCRIPT_DIR/report.html"
echo "📸 截图目录: $SCRIPT_DIR/screenshots/"
echo ""

exit $TEST_RESULT
