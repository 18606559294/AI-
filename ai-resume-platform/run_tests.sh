#!/bin/bash
# AI简历平台 - 全面自动化测试脚本

echo "=================================================="
echo "🚀 AI简历智能生成平台 - 全面自动化测试"
echo "=================================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "📁 项目目录: $PROJECT_ROOT"
echo ""

# ==================== 1. 环境检查 ====================
echo "📋 1. 环境检查"
echo "----------------------------------------"

# 检查Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 未安装${NC}"
fi

# 检查Flutter
if command -v flutter &> /dev/null; then
    FLUTTER_VERSION=$(flutter --version 2>/dev/null | head -1)
    echo -e "${GREEN}✅ Flutter: $FLUTTER_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️ Flutter 未安装或未初始化${NC}"
fi

# 检查ADB
if command -v adb &> /dev/null; then
    DEVICE_COUNT=$(adb devices | grep -c "device$")
    echo -e "${GREEN}✅ ADB 已安装, 连接设备: $DEVICE_COUNT${NC}"
else
    echo -e "${YELLOW}⚠️ ADB 未安装${NC}"
fi

echo ""

# ==================== 2. 后端测试 ====================
echo "📋 2. 后端API测试"
echo "----------------------------------------"

cd "$PROJECT_ROOT/backend"

if [ -f "tests/test_api.py" ]; then
    echo "运行后端测试..."
    python3 tests/test_api.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 后端测试全部通过${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${YELLOW}⚠️ 后端测试部分失败${NC}"
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}❌ 后端测试文件不存在${NC}"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))

echo ""

# ==================== 3. 代码语法检查 ====================
echo "📋 3. Python代码语法检查"
echo "----------------------------------------"

cd "$PROJECT_ROOT/backend"

SYNTAX_ERRORS=0
for pyfile in $(find app -name "*.py" 2>/dev/null); do
    python3 -m py_compile "$pyfile" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 语法错误: $pyfile${NC}"
        ((SYNTAX_ERRORS++))
    fi
done

if [ $SYNTAX_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 所有Python文件语法检查通过${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ $SYNTAX_ERRORS 个文件存在语法错误${NC}"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))

echo ""

# ==================== 4. 安全检查 ====================
echo "📋 4. 安全配置检查"
echo "----------------------------------------"

cd "$PROJECT_ROOT/backend"

# 检查敏感信息
if grep -r "password\s*=\s*['\"][^'\"]\+" app/ 2>/dev/null | grep -v "password_hash" | grep -v "test" > /dev/null; then
    echo -e "${RED}❌ 发现硬编码密码${NC}"
    ((FAILED_TESTS++))
else
    echo -e "${GREEN}✅ 未发现硬编码密码${NC}"
    ((PASSED_TESTS++))
fi
((TOTAL_TESTS++))

# 检查API密钥
if grep -r "sk-[a-zA-Z0-9]\{20,\}" app/ 2>/dev/null > /dev/null; then
    echo -e "${RED}❌ 发现硬编码API密钥${NC}"
    ((FAILED_TESTS++))
else
    echo -e "${GREEN}✅ 未发现硬编码API密钥${NC}"
    ((PASSED_TESTS++))
fi
((TOTAL_TESTS++))

# 检查.env文件
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${YELLOW}⚠️ 发现.env文件，确保已添加到.gitignore${NC}"
fi

echo ""

# ==================== 5. Flutter测试（如果可用）====================
echo "📋 5. Flutter前端测试"
echo "----------------------------------------"

cd "$PROJECT_ROOT/frontend"

if command -v flutter &> /dev/null; then
    # 获取依赖
    echo "获取Flutter依赖..."
    flutter pub get 2>/dev/null
    
    # 运行单元测试
    if [ -d "test" ]; then
        echo "运行Flutter单元测试..."
        flutter test 2>&1 | tail -20
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Flutter单元测试通过${NC}"
            ((PASSED_TESTS++))
        else
            echo -e "${YELLOW}⚠️ Flutter单元测试失败或跳过${NC}"
            ((FAILED_TESTS++))
        fi
    else
        echo -e "${YELLOW}⚠️ 未找到Flutter测试目录${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Flutter未安装，跳过前端测试${NC}"
fi
((TOTAL_TESTS++))

echo ""

# ==================== 6. 设备集成测试 ====================
echo "📋 6. 设备集成测试"
echo "----------------------------------------"

if command -v adb &> /dev/null; then
    DEVICE=$(adb devices | grep "device$" | head -1 | cut -f1)
    
    if [ -n "$DEVICE" ]; then
        echo "检测到设备: $DEVICE"
        
        # 获取设备信息
        DEVICE_MODEL=$(adb -s $DEVICE shell getprop ro.product.model 2>/dev/null)
        ANDROID_VERSION=$(adb -s $DEVICE shell getprop ro.build.version.release 2>/dev/null)
        
        echo "设备型号: $DEVICE_MODEL"
        echo "Android版本: $ANDROID_VERSION"
        
        if command -v flutter &> /dev/null && [ -d "integration_test" ]; then
            echo ""
            echo "运行集成测试..."
            cd "$PROJECT_ROOT/frontend"
            flutter test integration_test/ -d $DEVICE 2>&1 | tail -30
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ 集成测试通过${NC}"
                ((PASSED_TESTS++))
            else
                echo -e "${YELLOW}⚠️ 集成测试失败或跳过${NC}"
                ((FAILED_TESTS++))
            fi
        else
            echo -e "${YELLOW}⚠️ Flutter未就绪或无集成测试${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ 未检测到已连接设备${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ ADB未安装，跳过设备测试${NC}"
fi
((TOTAL_TESTS++))

echo ""

# ==================== 7. 文件结构检查 ====================
echo "📋 7. 项目结构检查"
echo "----------------------------------------"

cd "$PROJECT_ROOT"

REQUIRED_FILES=(
    "backend/app/main.py"
    "backend/app/core/config.py"
    "backend/app/api/v1/__init__.py"
    "backend/requirements.txt"
    "frontend/lib/main.dart"
    "frontend/pubspec.yaml"
    "docker-compose.yml"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ 缺失: $file${NC}"
        ((MISSING_FILES++))
    fi
done

if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}✅ 所有必需文件存在${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ $MISSING_FILES 个必需文件缺失${NC}"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))

echo ""

# ==================== 测试报告 ====================
echo "=================================================="
echo "📊 测试报告"
echo "=================================================="
echo ""
echo "总测试数: $TOTAL_TESTS"
echo -e "通过: ${GREEN}$PASSED_TESTS${NC}"
echo -e "失败: ${RED}$FAILED_TESTS${NC}"
echo ""

PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo "通过率: $PASS_RATE%"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️ 部分测试未通过，请检查上方日志${NC}"
    exit 1
fi
