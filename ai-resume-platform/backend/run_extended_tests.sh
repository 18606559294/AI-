#!/bin/bash

# AI简历应用 - 扩展功能测试脚本
# 测试错误处理、边界情况、高级功能

BASE_URL="http://127.0.0.1:8000"
RESULTS_FILE="extended_test_results_$(date +%Y%m%d_%H%M%S).txt"

echo "========================================" | tee $RESULTS_FILE
echo "AI简历应用 - 扩展功能测试" | tee -a $RESULTS_FILE
echo "测试时间: $(date)" | tee -a $RESULTS_FILE
echo "========================================" | tee -a $RESULTS_FILE

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 测试函数
test_api() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local token="$5"
    local expected="${6:-200}"
    
    echo "" | tee -a $RESULTS_FILE
    echo "测试: $name" | tee -a $RESULTS_FILE
    echo "----------------------------------------" | tee -a $RESULTS_FILE
    
    if [ -z "$token" ]; then
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" -w "\n%{http_code}")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            -d "$data" -w "\n%{http_code}")
    fi
    
    # 提取body和status
    body=$(echo "$response" | head -n -1)
    status=$(echo "$response" | tail -n 1)
    
    # 检查响应
    if echo "$body" | jq -e '.code' 2>/dev/null | grep -q "$expected"; then
        echo -e "${GREEN}✅ 通过${NC}" | tee -a $RESULTS_FILE
        echo "响应: $(echo "$body" | jq -r '.message' 2>/dev/null || echo "$body" | head -c 100)" | tee -a $RESULTS_FILE
        return 0
    else
        echo -e "${RED}❌ 失败${NC}" | tee -a $RESULTS_FILE
        echo "状态码: $status (期望: $expected)" | tee -a $RESULTS_FILE
        echo "响应: $body" | tee -a $RESULTS_FILE
        return 1
    fi
}

# 先创建测试用户并获取Token
echo ""
echo "## 准备测试环境" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

curl -s -X POST "$BASE_URL/api/v1/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"email":"extendedtest@example.com","password":"abc123","username":"ExtendedTest"}' > /dev/null

response=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=extendedtest@example.com&password=abc123")

ACCESS_TOKEN=$(echo "$response" | jq -r '.data.access_token')
echo "测试Token: ${ACCESS_TOKEN:0:20}..." | tee -a $RESULTS_FILE

# ========================================
# Phase 1: 简历CRUD完整测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 1: 简历CRUD完整测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 1.1 创建多个简历
echo ""
echo "### 1.1 创建多个简历" | tee -a $RESULTS_FILE
test_api "创建简历1" "POST" "/api/v1/resumes" \
    '{"title":"软件工程师简历","description":"申请后端开发岗位"}' "$ACCESS_TOKEN"

test_api "创建简历2" "POST" "/api/v1/resumes" \
    '{"title":"产品经理简历","description":"申请产品经理岗位"}' "$ACCESS_TOKEN"

# 1.2 获取简历列表（分页）
echo ""
echo "### 1.2 分页查询简历" | tee -a $RESULTS_FILE
test_api "获取第1页简历" "GET" "/api/v1/resumes?page=1&page_size=1" "" "$ACCESS_TOKEN"

# 1.3 获取简历详情（不存在）
echo ""
echo "### 1.3 获取不存在的简历详情" | tee -a $RESULTS_FILE
test_api "获取不存在的简历" "GET" "/api/v1/resumes/99999" "" "$ACCESS_TOKEN" "404"

# 1.4 更新简历
echo ""
echo "### 1.4 更新简历内容" | tee -a $RESULTS_FILE
test_api "更新简历" "PUT" "/api/v1/resumes/1" \
    '{"title":"更新的简历标题","content":{"basics":{"name":"测试用户","email":"test@example.com"}}}' "$ACCESS_TOKEN"

# 1.5 删除简历
echo ""
echo "### 1.5 删除简历" | tee -a $RESULTS_FILE
test_api "删除简历2" "DELETE" "/api/v1/resumes/2" "" "$ACCESS_TOKEN"

# ========================================
# Phase 2: 模板功能完整测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 2: 模板功能完整测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 2.1 获取不同分类的模板
echo ""
echo "### 2.1 按分类筛选模板" | tee -a $RESULTS_FILE
test_api "获取技术类模板" "GET" "/api/v1/templates?category=技术" "" "$ACCESS_TOKEN"

# 2.2 获取模板详情
echo ""
echo "### 2.2 获取模板详情" | tee -a $RESULTS_FILE
test_api "获取模板详情" "GET" "/api/v1/templates/1" "" "$ACCESS_TOKEN"

# 2.3 收藏模板
echo ""
echo "### 2.3 收藏模板" | tee -a $RESULTS_FILE
test_api "收藏模板" "POST" "/api/v1/templates/1/favorite" "" "$ACCESS_TOKEN"

# 2.4 取消收藏
echo ""
echo "### 2.4 取消收藏" | tee -a $RESULTS_FILE
test_api "取消收藏" "DELETE" "/api/v1/templates/1/favorite" "" "$ACCESS_TOKEN"

# ========================================
# Phase 3: 错误处理测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 3: 错误处理测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 3.1 重复注册
echo ""
echo "### 3.1 重复注册测试" | tee -a $RESULTS_FILE
test_api "重复注册" "POST" "/api/v1/auth/register" \
    '{"email":"extendedtest@example.com","password":"abc123"}' "" "$ACCESS_TOKEN" "400"

# 3.2 错误的密码登录
echo ""
echo "### 3.2 错误密码登录" | tee -a $RESULTS_FILE
test_api "错误密码登录" "POST" "/api/v1/auth/login" \
    "" "" "" "401"

# 3.3 无效的Token
echo ""
echo "### 3.3 无效Token访问" | tee -a $RESULTS_FILE
test_api "无效Token" "GET" "/api/v1/auth/me" "" "invalid_token_12345" "401"

# 3.4 无效的邮箱格式
echo ""
echo "### 3.4 无效邮箱格式" | tee -a $RESULTS_FILE
test_api "无效邮箱" "POST" "/api/v1/auth/register" \
    '{"email":"invalid-email","password":"abc123"}' "" "" "422"

# 3.5 弱密码
echo ""
echo "### 3.5 弱密码测试" | tee -a $RESULTS_FILE
test_api "弱密码" "POST" "/api/v1/auth/register" \
    '{"email":"weak@test.com","password":"123"}' "" "" "422"

# ========================================
# Phase 4: 数据验证测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 4: 数据验证测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 4.1 空标题创建简历
echo ""
echo "### 4.1 空标题创建简历" | tee -a $RESULTS_FILE
test_api "空标题简历" "POST" "/api/v1/resumes" \
    '{"title":"","description":"测试"}' "$ACCESS_TOKEN" "422"

# 4.2 超长标题
echo ""
echo "### 4.2 超长标题" | tee -a $RESULTS_FILE
LONG_TITLE=$(printf 'A%.0s' {1..300})
test_api "超长标题" "POST" "/api/v1/resumes" \
    "{\"title\":\"$LONG_TITLE\",\"description\":\"测试\"}" "$ACCESS_TOKEN" "422"

# ========================================
# Phase 5: 边界情况测试
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "## Phase 5: 边界情况测试" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE

# 5.1 大页码查询
echo ""
echo "### 5.1 查询第999页" | tee -a $RESULTS_FILE
test_api "大页码" "GET" "/api/v1/resumes?page=999&page_size=10" "" "$ACCESS_TOKEN"

# 5.2 超大页大小
echo ""
echo "### 5.2 超大页大小" | tee -a $RESULTS_FILE
test_api "超大页大小" "GET" "/api/v1/resumes?page=1&page_size=999" "" "$ACCESS_TOKEN"

# ========================================
# 测试总结
# ========================================
echo "" | tee -a $RESULTS_FILE
echo "========================================" | tee -a $RESULTS_FILE
echo "扩展测试完成" | tee -a $RESULTS_FILE
echo "========================================" | tee -a $RESULTS_FILE
echo "结果文件: $RESULTS_FILE" | tee -a $RESULTS_FILE

# 统计
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

