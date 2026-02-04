# AI 简历智能生成平台

AI 驱动的简历智能生成平台，支持网页版和桌面版。

## 项目结构

```
ai_resume/
├── AI-ai-resume-platform/    # Flutter 移动端应用
├── ai-resume-shared/         # 共享代码（类型定义、API 客户端）
├── ai-resume-web/            # React 网页版
├── ai-resume-desktop/        # Tauri 桌面版
└── start.bat                 # Windows 统一启动脚本
```

## 技术栈

### 移动端 (Flutter)
- Flutter 3.x
- Riverpod (状态管理)
- Go Router (路由)
- Dio (网络请求)

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

### Windows 用户

双击运行 `start.bat` 选择对应操作：

1. 网页版开发
2. 桌面版开发
3. 网页版构建
4. 桌面版构建
5. 安装依赖

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

## 功能特性

- ✅ 用户注册/登录
- ✅ 简历创建和编辑
- ✅ AI 智能生成简历内容
- ✅ 多种精美模板
- ✅ 简历导出 (PDF/Word/HTML)
- ✅ 个人中心
- ✅ 设置管理
- ✅ 多 AI 提供商支持 (OpenAI/DeepSeek/小米AI)

## 许可证

MIT License
