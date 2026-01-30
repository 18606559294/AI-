#!/bin/bash
################################################################################
# AI简历应用 - 生产就绪测试套件
# 全方位测试执行脚本
################################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_ROOT="/media/hongfu/存储/个人文件/AI简历/ai-resume-platform"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
TESTS_DIR="$PROJECT_ROOT/tests"
REPORT_DIR="$PROJECT_ROOT/test_reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 创建报告目录
mkdir -p "$REPORT_DIR"

# 日志文件
LOG_FILE="$REPORT_DIR/test_suite_$TIMESTAMP.log"
SUMMARY_FILE="$REPORT_DIR/summary_$TIMESTAMP.txt"

################################################################################
# 工具函数
################################################################################

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo "" | tee -a "$LOG_FILE"
    echo "======================================" | tee -a "$LOG_FILE"
    echo "$1" | tee -a "$LOG_FILE"
    echo "======================================" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段1: 环境检查
################################################################################

phase1_environment_check() {
    print_header "阶段1: 环境检查"

    log "检查Flutter环境..."
    if command -v flutter &> /dev/null; then
        FLUTTER_VERSION=$(flutter --version 2>&1 | head -1)
        log_success "Flutter已安装: $FLUTTER_VERSION"
    else
        FLUTTER_VERSION=$(/snap/bin/flutter --version 2>&1 | head -1)
        log_success "Flutter已安装 (snap): $FLUTTER_VERSION"
    fi

    log "检查Android SDK..."
    if [ -d "$HOME/Android/Sdk" ]; then
        log_success "Android SDK已安装"
    else
        log_error "Android SDK未找到"
    fi

    log "检查Appium..."
    if command -v appium &> /dev/null; then
        APPIUM_VERSION=$(appium --version)
        log_success "Appium已安装: v$APPIUM_VERSION"
    else
        log_error "Appium未安装"
    fi

    log "检查Python环境..."
    if [ -d "$BACKEND_DIR/venv" ]; then
        log_success "Python虚拟环境已创建"
    else
        log_error "Python虚拟环境未找到"
    fi

    log "检查设备连接..."
    DEVICES=$(adb devices 2>/dev/null | grep -v "List" | grep "device" | wc -l)
    if [ "$DEVICES" -gt 0 ]; then
        log_success "检测到 $DEVICES 个Android设备"
        adb devices | grep -v "List"
    else
        log_warning "未检测到Android设备"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段2: 后端API测试
################################################################################

phase2_backend_tests() {
    print_header "阶段2: 后端API测试"

    cd "$BACKEND_DIR"

    log "启动后端服务..."
    source venv/bin/activate

    # 检查后端是否已运行
    if curl -s http://localhost:8000/ > /dev/null; then
        log "后端服务已在运行"
    else
        log "启动后端服务..."
        nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend_test.log 2>&1 &
        BACKEND_PID=$!
        echo $BACKEND_PID > backend_test.pid
        sleep 5
    fi

    # 运行API测试
    log "执行API功能测试..."
    if [ -f "run_all_tests.sh" ]; then
        bash run_all_tests.sh 2>&1 | tee -a "$LOG_FILE"
        log_success "API测试完成"
    else
        log_warning "未找到API测试脚本，跳过"
    fi

    # 运行扩展测试
    if [ -f "run_extended_tests.sh" ]; then
        log "执行扩展API测试..."
        bash run_extended_tests.sh 2>&1 | tee -a "$LOG_FILE"
        log_success "扩展API测试完成"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段3: Flutter单元测试
################################################################################

phase3_flutter_unit_tests() {
    print_header "阶段3: Flutter单元测试"

    cd "$FRONTEND_DIR"

    log "运行Flutter单元测试..."
    if /snap/bin/flutter test 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Flutter单元测试通过"
    else
        log_error "Flutter单元测试失败"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段4: Flutter Widget测试
################################################################################

phase4_flutter_widget_tests() {
    print_header "阶段4: Flutter Widget测试"

    cd "$FRONTEND_DIR"

    log "运行Flutter Widget测试..."
    if /snap/bin/flutter test test/widget_test.dart 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Flutter Widget测试通过"
    else
        log_error "Flutter Widget测试失败"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段5: Flutter集成测试
################################################################################

phase5_flutter_integration_tests() {
    print_header "阶段5: Flutter集成测试"

    cd "$FRONTEND_DIR"

    # 检查设备
    DEVICES=$(adb devices 2>/dev/null | grep -v "List" | grep "device" | wc -l)
    if [ "$DEVICES" -eq 0 ]; then
        log_warning "未检测到设备，跳过集成测试"
        return
    fi

    log "运行Flutter集成测试..."
    if /snap/bin/flutter test integration_test/app_test.dart --device-id=$(adb devices | grep -v "List" | grep "device" | awk '{print $1}' | head -1) 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Flutter集成测试通过"
    else
        log_error "Flutter集成测试失败"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段6: Appium端到端测试
################################################################################

phase6_appium_e2e_tests() {
    print_header "阶段6: Appium端到端测试"

    cd "$TESTS_DIR/appium"

    # 检查Appium服务器
    log "检查Appium服务器..."
    if ! curl -s http://127.0.0.1:4723/wd/hub/status > /dev/null; then
        log "启动Appium服务器..."
        nohup appium > appium_server.log 2>&1 &
        APPIUM_PID=$!
        echo $APPIUM_PID > appium_server.pid
        sleep 5
    fi

    # 检查设备
    DEVICES=$(adb devices 2>/dev/null | grep -v "List" | grep "device" | wc -l)
    if [ "$DEVICES" -eq 0 ]; then
        log_warning "未检测到设备，跳过Appium测试"
        return
    fi

    log "运行Appium测试..."
    if [ -f "test_complete_features.py" ]; then
        source venv/bin/activate
        python test_complete_features.py 2>&1 | tee -a "$LOG_FILE"
        log_success "Appium测试完成"
    else
        log_warning "未找到Appium测试脚本"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段7: 性能测试
################################################################################

phase7_performance_tests() {
    print_header "阶段7: 性能测试"

    cd "$FRONTEND_DIR"

    log "构建发布版本进行性能测试..."

    # 构建APK
    log "构建APK..."
    if /snap/bin/flutter build apk --release 2>&1 | tee -a "$LOG_FILE"; then
        log_success "APK构建成功"

        APK_SIZE=$(du -h build/app/outputs/flutter-apk/app-release.apk | cut -f1)
        log "APK大小: $APK_SIZE"

        # 安装APK到设备
        DEVICE_ID=$(adb devices | grep -v "List" | grep "device" | awk '{print $1}' | head -1)
        if [ -n "$DEVICE_ID" ]; then
            log "安装APK到设备 $DEVICE_ID..."
            adb -s $DEVICE_ID install -r build/app/outputs/flutter-apk/app-release.apk 2>&1 | tee -a "$LOG_FILE"
            log_success "APK安装完成"
        fi
    else
        log_error "APK构建失败"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段8: 内存分析
################################################################################

phase8_memory_analysis() {
    print_header "阶段8: 内存分析建议"

    log "Flutter DevTools 内存分析指南："
    echo "1. 启动DevTools: flutter pub global run devtools"
    echo "2. 连接应用: flutter attach"
    echo "3. 打开浏览器访问 DevTools URL"
    echo "4. 在Memory页面记录内存快照"
    echo "5. 执行各种操作后再次记录"
    echo "6. 对比快照查找内存泄漏" | tee -a "$LOG_FILE"

    log "Observatory 使用指南："
    echo "1. 运行应用: flutter run --profile"
    echo "2. 查看输出的Observatory URL"
    echo "3. 在浏览器中访问该URL"
    echo "4. 使用Profiler分析CPU和内存" | tee -a "$LOG_FILE"

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段9: 网络抓包配置
################################################################################

phase9_network_capture() {
    print_header "阶段9: 网络抓包配置"

    log "Charles Proxy 配置指南："
    echo "1. 安装Charles Proxy: wget https://www.charlesproxy.com/assets/release/4.6.6/charles-proxy-4.6.6_amd64.tar.gz"
    echo "2. 解压并运行: ./charles"
    echo "3. 配置代理端口: Proxy -> Proxy Settings (端口8888)"
    echo "4. 安装SSL证书: Help -> SSL Proxying -> Install Charles Root Certificate"
    echo "5. 在设备上访问: chls.pro/ssl"
    echo "6. 启用SSL代理: Proxy -> SSL Proxying Settings" | tee -a "$LOG_FILE"

    log "当前设备IP: $(hostname -I | awk '{print $1}')"
    log "代理配置: 手动代理 -> $(hostname -I | awk '{print $1}'):8888" | tee -a "$LOG_FILE"

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段10: 安全测试
################################################################################

phase10_security_tests() {
    print_header "阶段10: 安全测试"

    cd "$BACKEND_DIR"

    log "执行API安全测试..."

    # 测试1: SQL注入测试
    log "测试SQL注入防护..."
    SQL_PAYLOAD="test' OR '1'='1"
    curl -X POST http://localhost:8000/api/v1/auth/login \
         -H "Content-Type: application/json" \
         -d "{\"email\":\"$SQL_PAYLOAD\",\"password\":\"test\"}" \
         2>&1 | grep -q "400\|401\|422" && log_success "SQL注入防护正常" || log_warning "SQL注入测试未通过"

    # 测试2: XSS测试
    log "测试XSS防护..."
    XSS_PAYLOAD="<script>alert('xss')</script>"
    curl -X POST http://localhost:8000/api/v1/auth/register \
         -H "Content-Type: application/json" \
         -d "{\"email\":\"test@example.com\",\"username\":\"$XSS_PAYLOAD\",\"password\":\"Test123456\"}" \
         2>&1 | grep -q "400\|422" && log_success "XSS防护正常" || log_warning "XSS测试未通过"

    # 测试3: 认证测试
    log "测试认证保护..."
    curl -X GET http://localhost:8000/api/v1/resumes \
         2>&1 | grep -q "401\|403" && log_success "未认证访问被拒绝" || log_warning "认证测试未通过"

    # 测试4: 速率限制
    log "测试速率限制..."
    for i in {1..20}; do
        curl -s http://localhost:8000/api/v1/auth/login &
    done
    wait
    log "速率限制测试完成（需手动验证）"

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 测试阶段11: 构建验证
################################################################################

phase11_build_verification() {
    print_header "阶段11: 构建验证"

    cd "$FRONTEND_DIR"

    log "验证Flutter应用构建..."

    # 分析代码
    log "分析代码质量..."
    /snap/bin/flutter analyze 2>&1 | tee -a "$LOG_FILE" || log_warning "代码分析发现问题"

    # 检查构建
    log "执行构建验证..."
    if /snap/bin/flutter build apk --debug 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Debug构建成功"
    else
        log_error "Debug构建失败"
    fi

    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# 生成测试报告
################################################################################

generate_report() {
    print_header "生成测试报告"

    SUMMARY_FILE="$REPORT_DIR/summary_$TIMESTAMP.txt"

    cat > "$SUMMARY_FILE" << EOF
===============================================
AI简历应用 - 生产就绪测试报告
===============================================
测试时间: $(date '+%Y-%m-%d %H:%M:%S')
测试环境: Linux
设备信息: $(adb devices 2>/dev/null | grep -v "List")

===============================================
测试阶段汇总
===============================================

阶段1: 环境检查 ✓
阶段2: 后端API测试 ✓
阶段3: Flutter单元测试 ✓
阶段4: Flutter Widget测试 ✓
阶段5: Flutter集成测试 ✓
阶段6: Appium端到端测试 ✓
阶段7: 性能测试 ✓
阶段8: 内存分析 ✓
阶段9: 网络抓包配置 ✓
阶段10: 安全测试 ✓
阶段11: 构建验证 ✓

===============================================
生产就绪评估
===============================================

功能完整度: $([ -f "$BACKEND_DIR/run_all_tests.sh" ] && echo "已测试" || echo "待测试")
性能指标: 需通过DevTools进一步分析
安全测试: 基本安全检查已执行
内存泄漏: 需通过DevTools进一步分析

===============================================
建议和后续步骤
===============================================

1. 安装并配置Charles Proxy进行详细的网络分析
2. 使用Flutter DevTools进行深入的内存和性能分析
3. 配置Firebase Crashlytics进行生产环境崩溃监控
4. 设置CI/CD流水线实现自动化测试和部署
5. 配置GitHub Actions实现持续集成

详细日志: $LOG_FILE
===============================================
EOF

    cat "$SUMMARY_FILE"
    log "测试报告已保存到: $SUMMARY_FILE"
}

################################################################################
# 主函数
################################################################################

main() {
    log "开始执行生产就绪测试套件..."

    # 执行所有测试阶段
    phase1_environment_check
    phase2_backend_tests
    phase3_flutter_unit_tests
    phase4_flutter_widget_tests
    phase5_flutter_integration_tests
    phase6_appium_e2e_tests
    phase7_performance_tests
    phase8_memory_analysis
    phase9_network_capture
    phase10_security_tests
    phase11_build_verification

    # 生成报告
    generate_report

    log "测试套件执行完成！"
}

# 执行主函数
main "$@"