# AI 简历智能生成平台

AI 驱动的简历智能生成平台，支持网页版和桌面版。

## 项目结构

```
ai_resume/
├── PROJECT_MANAGEMENT/   # 项目文档和计划
├── ai-resume-shared/     # 共享代码（类型定义、API 客户端）
├── ai-resume-web/        # React 网页版 (支持响应式移动端视图)
├── ai-resume-desktop/    # Tauri 桌面版
└── start.bat             # Windows 统一启动脚本
```

## 技术栈

### 移动端 (当前)
- 响应式 Web Design (适配 iOS/Android 浏览器)
- 原生 App 迁移计划见 `PROJECT_MANAGEMENT/plans/FLUTTER_MIGRATION_PLAN.md`

### 网页版 / 桌面版
- React 18 + TypeScript
- Vite (构建工具)
- TailwindCSS (样式)
- React Router (路由)
- TanStack Query (数据获取)
- Zustand (状态管理)

### 桌面版额外
- Tauri (桌面应用框架)
- Rust (后端)

## 快速开始

### Docker 部署 (推荐)

我们为网页版提供了 Docker 部署支持，包含 Nginx 服务器。

1. 在项目根目录下构建镜像：
   ```bash
   docker build -f ai-resume-web/Dockerfile -t ai-resume-web .
   ```

2. 运行容器：
   ```bash
   docker run -d -p 3000:80 ai-resume-web
   ```

3. 访问 `http://localhost:3000`

### 手动启动

#### 网页版

```bash
cd ai-resume-web
npm install
npm run dev
```

#### 桌面版

```bash
cd ai-resume-desktop
npm install
npm run tauri:dev
```

## 开发指南

### 共享代码

所有共享的类型定义和 API 客户端位于 `ai-resume-shared/`：

```
ai-resume-shared/
├── src/
│   ├── types/       # TypeScript 类型定义
│   ├── api/         # API 客户端
│   └── utils/       # 工具函数
```

### 添加新功能

1. 在 `ai-resume-shared/src/types/` 添加类型定义
2. 在 `ai-resume-shared/src/api/` 添加 API 方法
3. 在 `ai-resume-web/src/pages/` 实现网页版 UI
4. 桌面版会自动继承网页版的所有功能

## 构建

### 网页版

```bash
cd ai-resume-web
npm run build
```

输出: `ai-resume-web/dist/`

### 桌面版

```bash
cd ai-resume-desktop
npm run tauri:build
```

输出: `ai-resume-desktop/src-tauri/target/release/`

## 测试

本项目包含完整的 E2E 测试套件，覆盖 Web、移动端视图和桌面端逻辑。

```bash
# 运行网页版和移动端视图测试
cd ai-resume-web
npx playwright test
```

## 功能特性

- ✅ 用户注册/登录
- ✅ 简历创建和编辑
- ✅ AI 智能生成简历内容
- ✅ 多种精美模板
- ✅ 简历导出 (PDF/Word/HTML)
- ✅ 个人中心
- ✅ 设置管理
- ✅ 多 AI 提供商支持 (OpenAI/DeepSeek/小米AI)
- ✅ 本地文件存储 (桌面端专属)

## 许可证

MIT License
