#!/bin/bash

# AI简历应用 - 完整功能测试脚本
# 测试所有API端点

BASE_URL="http://127.0.0.1:8000"
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).txt"

echo "========================================" | tee $RESULTS_FILE
echo "AI简历应用 - 完整功能测试" | tee -a $RESULTS_FILE
echo "测试时间: $(date)" | tee -a $RESULTS_FILE
echo "========================================" | tee -a $RESULTS_FILE

# 全局变量
ACCESS_TOKEN=""
REFRESH_TOKEN=""
USER_ID=""
RESUME_ID=""
TEMPLATE_ID=""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_api() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local token="$5"
    
    echo "" | tee -a $RESULTS_FILE
    echo "测试: $name" | tee -a $RESULTS_FILE
    echo "----------------------------------------" | tee -a $RESULTS_FILE
    
    if [ -z "$token" ]; then
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            -d "$data")
    fi
    
    # 检查响应
    if echo "$response" | jq -e '.code' 2>/dev/null | grep -q '200'; then
        echo -e "${GREEN}✅ 通过${NC}" | tee -a $RESULTS_FILE
        echo "响应: $(echo "$response" | jq -r '.message')" | tee -a $RESULTS_FILE
        return 0
    else
        echo -e "${RED}❌ 失败${NC}" | tee -a $RESULTS_FILE
        echo "响应: $response" | tee -a $RESULTS_FILE
        return 1
    fi
}

echo ""
echo "开始测试..." | tee -a $RESULTS_FILE

# ========================================
# Phase 1: 认证功能测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 1: 认证功能测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 1.1 用户注册
echo ""
echo "### 1.1 用户注册" | tee -a $RESULTS_FILE
response=$(curl -s -X POST "$BASE_URL/api/v1/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"email":"testuser@example.com","password":"abc123","username":"TestUser"}')

echo "$response" | tee -a $RESULTS_FILE
if echo "$response" | jq -e '.data.id' > /dev/null 2>&1; then
    USER_ID=$(echo "$response" | jq -r '.data.id')
    echo -e "${GREEN}✅ 注册成功，用户ID: $USER_ID${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ 注册失败${NC}" | tee -a $RESULTS_FILE
fi

# 1.2 用户登录
echo ""
echo "### 1.2 用户登录" | tee -a $RESULTS_FILE
response=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser@example.com&password=abc123")

echo "$response" | jq -r '.message' | tee -a $RESULTS_FILE
ACCESS_TOKEN=$(echo "$response" | jq -r '.data.access_token')
REFRESH_TOKEN=$(echo "$response" | jq -r '.data.refresh_token')
echo "Token: ${ACCESS_TOKEN:0:20}..." | tee -a $RESULTS_FILE

# 1.3 获取用户信息
echo ""
echo "### 1.3 获取当前用户信息" | tee -a $RESULTS_FILE
test_api "获取用户信息" "GET" "/api/v1/auth/me" "" "$ACCESS_TOKEN"

# 1.4 Token刷新
echo ""
echo "### 1.4 Token刷新" | tee -a $RESULTS_FILE
response=$(curl -s -X POST "$BASE_URL/api/v1/auth/refresh" \
    -H "Content-Type: application/json" \
    -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}")

if echo "$response" | jq -e '.data.access_token' > /dev/null 2>&1; then
    NEW_TOKEN=$(echo "$response" | jq -r '.data.access_token')
    echo -e "${GREEN}✅ Token刷新成功${NC}" | tee -a $RESULTS_FILE
    ACCESS_TOKEN=$NEW_TOKEN
else
    echo -e "${RED}❌ Token刷新失败${NC}" | tee -a $RESULTS_FILE
fi

# ========================================
# Phase 2: 简历功能测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 2: 简历功能测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 2.1 创建简历
echo ""
echo "### 2.1 创建简历" | tee -a $RESULTS_FILE
response=$(curl -s -X POST "$BASE_URL/api/v1/resumes" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d '{"title":"测试简历","description":"这是一个测试简历"}')

echo "$response" | jq -r '.message' | tee -a $RESULTS_FILE
if echo "$response" | jq -e '.data.id' > /dev/null 2>&1; then
    RESUME_ID=$(echo "$response" | jq -r '.data.id')
    echo -e "${GREEN}✅ 简历创建成功，ID: $RESUME_ID${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ 简历创建失败${NC}" | tee -a $RESULTS_FILE
fi

# 2.2 获取简历列表
echo ""
echo "### 2.2 获取简历列表" | tee -a $RESULTS_FILE
test_api "获取简历列表" "GET" "/api/v1/resumes?page=1&page_size=10" "" "$ACCESS_TOKEN"

# 2.3 获取简历详情
if [ -n "$RESUME_ID" ]; then
    echo ""
    echo "### 2.3 获取简历详情 (ID: $RESUME_ID)" | tee -a $RESULTS_FILE
    test_api "获取简历详情" "GET" "/api/v1/resumes/$RESUME_ID" "" "$ACCESS_TOKEN"
    
    # 2.4 更新简历
    echo ""
    echo "### 2.4 更新简历" | tee -a $RESULTS_FILE
    test_api "更新简历" "PUT" "/api/v1/resumes/$RESUME_ID" \
        '{"title":"更新的测试简历"}' "$ACCESS_TOKEN"
fi

# ========================================
# Phase 3: 模板功能测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 3: 模板功能测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 3.1 获取模板列表
echo ""
echo "### 3.1 获取模板列表" | tee -a $RESULTS_FILE
test_api "获取模板列表" "GET" "/api/v1/templates?page=1&page_size=10" "" "$ACCESS_TOKEN"

# 3.2 获取模板分类
echo ""
echo "### 3.2 获取模板分类" | tee -a $RESULTS_FILE
test_api "获取模板分类" "GET" "/api/v1/templates/categories" "" "$ACCESS_TOKEN"

# ========================================
# Phase 4: 邮箱验证测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 4: 邮箱验证测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 4.1 发送验证码
echo ""
echo "### 4.1 发送验证码" | tee -a $RESULTS_FILE
test_api "发送验证码" "POST" "/api/v1/email/send-code" \
    '{"email":"verification@test.com"}' ""

# ========================================
# 测试总结
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "========================================" | tee -a $RESULTS_FILE
echo "测试完成" | tee -a $RESULTS_FILE
echo "========================================" | tee -a $RESULTS_FILE
echo "结果文件: $RESULTS_FILE" | tee -a $RESULTS_FILE

# 统计通过/失败
total=$(grep -c "测试:" $RESULTS_FILE || echo 0)
passed=$(grep -c "✅ 通过" $RESULTS_FILE || echo 0)
failed=$(grep -c "❌ 失败" $RESULTS_FILE || echo 0)

echo "" | tee -a $RESULTS_FILE
echo "📊 测试统计:" | tee -a $RESULTS_FILE
echo "  总测试数: $total" | tee -a $RESULTS_FILE
echo "  通过: $passed" | tee -a $RESULTS_FILE
echo "  失败: $failed" | tee -a $RESULTS_FILE
echo "  通过率: $(awk "BEGIN {printf \"%.1f\", $passed*100/$total}")%" | tee -a $RESULTS_FILE

echo ""
echo "测试完成！查看详细结果: cat $RESULTS_FILE"

