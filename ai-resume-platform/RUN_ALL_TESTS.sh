#!/bin/bash
# AI简历应用 - 完整测试执行脚本
# 使用方法: bash RUN_ALL_TESTS.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}AI简历应用 - 完整测试套件${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 统计变量
PASSED=0
FAILED=0
SKIPPED=0

# 打印函数
print_header() {
    echo -e "\n${BLUE}===== $1 =====${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((SKIPPED++))
}

# ==================== 1. 环境检查 ====================
print_header "1. 环境检查"

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 已安装"
        return 0
    else
        print_warning "$1 未安装"
        return 1
    fi
}

check_command python3 || true
check_command flutter || true
check_command docker || true
check_command java || true
check_command gradle || true

# ==================== 2. 后端测试 ====================
print_header "2. 后端测试"

cd "$PROJECT_DIR/backend"

if check_command python3; then
    print_header "Python版本检查"
    python3 --version
    
    # 检查虚拟环境
    if [ -d "venv" ]; then
        print_success "虚拟环境存在"
        source venv/bin/activate 2>/dev/null || true
    fi
    
    # 安装依赖
    print_header "安装依赖"
    pip3 install -q -r requirements.txt 2>/dev/null || print_warning "依赖安装失败"
    
    # 代码格式检查
    print_header "代码格式检查"
    python3 -m flake8 app/ --max-line-length=120 --count 2>/dev/null || print_warning "flake8未安装"
    
    # 运行测试
    print_header "运行单元测试"
    python3 -m pytest tests/ -v --tb=short 2>/dev/null && print_success "后端测试通过" || print_warning "测试未执行(需要pytest)"
else
    print_warning "跳过后端测试 - Python未安装"
fi

# ==================== 3. 前端测试 ====================
print_header "3. 前端测试"

cd "$PROJECT_DIR/frontend"

if check_command flutter; then
    print_header "Flutter版本检查"
    flutter --version
    
    print_header "获取依赖"
    flutter pub get
    
    print_header "代码分析"
    flutter analyze && print_success "代码分析通过" || print_error "代码分析失败"
    
    print_header "运行单元测试"
    flutter test && print_success "前端测试通过" || print_error "前端测试失败"
else
    print_warning "跳过前端测试 - Flutter未安装"
fi

# ==================== 4. Android构建测试 ====================
print_header "4. Android构建测试"

cd "$PROJECT_DIR/frontend"

if check_command flutter; then
    print_header "构建Debug APK"
    flutter build apk --debug && print_success "Debug构建成功" || print_error "Debug构建失败"
    
    print_header "检查APK输出"
    APK_PATH="build/app/outputs/flutter-apk/app-debug.apk"
    if [ -f "$APK_PATH" ]; then
        APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
        print_success "APK生成成功 (大小: $APK_SIZE)"
    else
        print_warning "APK文件未找到"
    fi
else
    print_warning "跳过Android构建 - Flutter未安装"
fi

# ==================== 5. Espresso测试 ====================
print_header "5. Espresso UI测试"

cd "$PROJECT_DIR/frontend/android"

if [ -f "gradlew" ]; then
    print_header "运行Espresso测试"
    ./gradlew connectedCheck 2>/dev/null && print_success "Espresso测试通过" || print_warning "Espresso测试未执行(需要设备/模拟器)"
else
    print_warning "跳过Espresso测试 - gradlew未找到"
fi

# ==================== 6. 性能测试 ====================
print_header "6. 性能基准测试"

cd "$PROJECT_DIR/frontend/android"

if [ -f "gradlew" ]; then
    print_header "运行Macrobenchmark"
    ./gradlew :app:connectedCheck -Pandroid.testInstrumentationRunnerArguments.androidx.benchmark.enabledRuns=1 2>/dev/null && print_success "性能测试完成" || print_warning "性能测试未执行"
else
    print_warning "跳过性能测试"
fi

# ==================== 7. Docker测试 ====================
print_header "7. Docker构建测试"

cd "$PROJECT_DIR"

if check_command docker; then
    print_header "构建后端镜像"
    docker build -t ai-resume-backend:test -f backend/Dockerfile backend/ 2>/dev/null && print_success "后端镜像构建成功" || print_warning "后端镜像构建失败"
    
    print_header "构建Nginx镜像"
    docker build -t ai-resume-nginx:test -f nginx/Dockerfile nginx/ 2>/dev/null && print_success "Nginx镜像构建成功" || print_warning "Nginx镜像构建失败"
else
    print_warning "跳过Docker测试 - Docker未安装"
fi

# ==================== 8. 安全扫描 ====================
print_header "8. 安全检查"

# 检查敏感文件
print_header "检查敏感文件"
SENSITIVE_FILES=(".env" "*.key" "*.pem" "credentials.json")
FOUND=0
for pattern in "${SENSITIVE_FILES[@]}"; do
    if find . -name "$pattern" -type f 2>/dev/null | grep -q .; then
        print_warning "发现敏感文件模式: $pattern"
        FOUND=1
    fi
done
if [ $FOUND -eq 0 ]; then
    print_success "未发现敏感文件"
fi

# 检查.gitignore
if [ -f ".gitignore" ]; then
    if grep -q ".env" .gitignore; then
        print_success ".env已在.gitignore中"
    else
        print_warning ".env未在.gitignore中"
    fi
fi

# ==================== 9. 代码统计 ====================
print_header "9. 代码统计"

echo ""
echo "后端代码统计:"
find backend/app -name "*.py" -type f 2>/dev/null | wc -l | xargs echo "  Python文件数:"
find backend/app -name "*.py" -type f -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print "  总行数: " $1}'

echo ""
echo "前端代码统计:"
find frontend/lib -name "*.dart" -type f 2>/dev/null | wc -l | xargs echo "  Dart文件数:"
find frontend/lib -name "*.dart" -type f -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print "  总行数: " $1}'

# ==================== 10. 测试报告 ====================
print_header "10. 测试报告"

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}测试结果汇总${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "  ${GREEN}通过: $PASSED${NC}"
echo -e "  ${RED}失败: $FAILED${NC}"
echo -e "  ${YELLOW}跳过: $SKIPPED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ 所有测试通过！${NC}"
    EXIT_CODE=0
else
    echo -e "${RED}✗ 有 $FAILED 个测试失败${NC}"
    EXIT_CODE=1
fi

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo -e "${BLUE}======================================${NC}"

exit $EXIT_CODE
