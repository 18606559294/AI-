# 测试体系文档

## 概述

本项目采用三层测试金字塔结构：
- 70% 单元测试 - 测试独立函数和组件
- 20% 集成测试 - 测试 API 端点和模块交互
- 10% E2E 测试 - 测试完整用户流程

---

## 后端测试 (pytest + FastAPI)

### 测试框架
- **pytest**: 测试运行器
- **pytest-asyncio**: 异步测试支持
- **httpx**: HTTP 客户端用于 API 测试

### 测试文件结构
```
backend/tests/
├── conftest.py              # 测试配置和 fixtures
├── test_api.py              # 基础单元测试
├── test_auth_api.py         # 认证 API 集成测试
└── test_resume_api.py       # 简历 API 集成测试
```

### 运行后端测试
```bash
cd ~/ai-resume/backend
source venv/bin/activate
pip install pytest pytest-asyncio httpx
pytest tests/ -v
pytest tests/ -v --cov=app --cov-report=html
```

### 测试覆盖
- ✅ 用户注册/登录/登出
- ✅ JWT 令牌验证
- ✅ 密码修改
- ✅ 简历 CRUD 操作
- ✅ 简历版本管理
- ✅ 分页查询
- ✅ 输入验证
- ✅ 安全检查 (XSS, SQL注入)

---

## 前端测试 (vitest + Testing Library)

### 测试框架
- **vitest**: 快速单元测试框架
- **@testing-library/react**: React 组件测试
- **@testing-library/user-event**: 用户交互模拟

### 测试文件结构
```
ai-resume-web/src/
├── test/
│   └── setup.ts             # 测试设置
├── components/
│   └── ResumePreview.test.tsx  # 组件测试
├── store/
│   └── auth.test.ts         # 状态管理测试
└── utils/
    └── __tests__/
        └── cn.test.ts       # 工具函数测试
```

### 运行前端测试
```bash
cd ~/ai-resume/ai-resume-web
npm run test              # 运行所有测试
npm run test:watch        # 监听模式
npm run test:coverage     # 覆盖率报告
npm run test:ui           # UI 界面
```

### 测试覆盖
- ✅ 组件渲染测试
- ✅ 用户交互测试
- ✅ 状态管理 (Zustand)
- ✅ 工具函数
- ✅ 表单验证

---

## E2E 测试 (Playwright)

### 测试框架
- **@playwright/test**: 跨浏览器 E2E 测试

### 测试文件结构
```
ai-resume-web/tests/e2e/
├── auth.spec.ts             # 认证流程测试
├── mobile.spec.ts           # 移动端测试
└── mobile-full-flow.spec.ts # 完整业务流程测试
```

### 运行 E2E 测试
```bash
cd ~/ai-resume/ai-resume-web
npm run test:e2e            # 运行 E2E 测试
npm run test:e2e:ui         # UI 模式
npm run test:e2e:headed     # 有头模式
```

### E2E 测试场景
- ✅ 用户注册流程
- ✅ 用户登录流程
- ✅ 表单验证
- ✅ 响应式布局
- ✅ 页面导航
- ✅ 可访问性测试

---

## CI/CD 集成

所有测试已集成到 CI/CD 工作流：

### .github/workflows/ci.yml
- 前端代码检查 (ESLint, TypeScript)
- 前端单元测试
- 前端 E2E 测试
- 后端代码检查 (Black, Flake8, MyPy)
- 后端单元测试
- 安全扫描 (CodeQL, Trivy)

---

## 测试覆盖率目标

| 类型 | 目标 | 当前状态 |
|------|------|----------|
| 后端单元测试 | 80%+ | ✅ |
| 前端单元测试 | 70%+ | ✅ |
| E2E 测试 | 关键流程 | ✅ |

---

## 待添加测试

### 后端
- [ ] AI 服务 Mock 测试
- [ ] 邮件服务测试
- [ ] 文件上传测试
- [ ] 导出功能测试

### 前端
- [ ] 富文本编辑器测试
- [ ] 拖拽功能测试
- [ ] 撤销/重做测试
- [ ] 更多组件测试

### E2E
- [ ] AI 生成流程
- [ ] 简历导出流程
- [ ] 简历模板切换
- [ ] 支付流程 (如适用)

---

## Mock 数据

测试使用内存 SQLite 数据库，无需外部依赖。
所有 API 调用在测试环境中使用 Mock 响应。
