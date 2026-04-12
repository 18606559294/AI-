# 开发日志 — AI Resume 项目

> 本文档记录所有功能开发、架构变更和技术决策。
> 格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，日期使用 YYYY-MM-DD。

---

## [2026-04-12] 官网修复 + 职业智能融合

### 新增

#### 前端 — 全局导航系统
- `PublicNavbar` 组件 — 固定顶部导航栏，琥珀金+翡翠绿深色主题，滚动毛玻璃效果
- `PublicLayout` 组件 — 包裹所有公开页面的统一布局
- `PublicNavbar.css` — 响应式样式，768px 移动端汉堡菜单
- 导航菜单项：首页、职业智能、关于、帮助、Trae AI、条款、隐私、登录、注册

#### 前端 — 职业智能中心 (`/career`)
- `CareerPage.tsx` — 三合一页面：
  - **JD 智能评估** — 粘贴 JD → 6 维全景分析（直觉判断/职位摘要/简历匹配/等级策略/薪资研究/面试准备）
  - **故事银行** — Polanyi 默会经验挖掘，STAR+R 面试故事
  - **智能定制** — 基于 JD 直觉调整简历叙事角度
- 集成到全局导航和首页 Navbar

#### 前端 — TraePage 导航改造
- 移除 TraePage 的独立 `<nav>` 导航
- 使用 `PublicLayout` 包裹，复用全局导航
- Trae AI 正式进入导航菜单，不再藏在下载区

#### 后端 — 职业智能 API (`/api/v1/career/`)
- `POST /evaluate` — JD 6 维全景评估
  - 输入：resume_id + job_description + user_preferences
  - 输出：intuition(直觉) + blocks(A-F) + overall_score + recommendation + tacit_insight
- `POST /story-bank` — STAR+R 故事挖掘
  - 输入：resume_id + existing_stories + additional_context
  - 输出：stories[] + meta_stories[] + growth_trajectory
- `POST /smart-tailor` — 智能简历定制
  - 输入：resume_id + job_description
  - 输出：tailored_content + changes_made[] + keywords_injected + narrative_angle

#### 后端 — AI Prompt 体系
- `career_intelligence_v1.md` — 系统提示词：20 年经验资深猎头 + Polanyi 默会知识理论
- `career/jd_evaluate.md` — JD 评估任务 prompt，6 块评估 + JSON 输出规范
- `career/story_bank.md` — 故事银行 prompt，默会知识挖掘框架

#### 后端 — 路由注册
- `app/api/v1/__init__.py` 添加 `career_router`
- 新文件 `app/api/v1/career.py`

### 修改

#### 公开页面改造（统一全局导航）
- `AboutPage.tsx` — 移除独立 header，使用 PublicLayout
- `HelpPage.tsx` — 同上
- `TermsPage.tsx` — 同上
- `PrivacyPage.tsx` — 同上
- `TraePage.tsx` — 移除独立 nav，使用 PublicLayout，添加 `paddingTop: 64px`
- `LoginPage.tsx` — 通过 App.tsx 路由级 PublicLayout 包裹
- `RegisterPage.tsx` — 同上
- `ForgotPasswordPage.tsx` — 同上

#### 首页 Navbar 更新
- `Navbar.tsx` — 添加：职业智能、帮助、Trae AI、条款、隐私链接
- 移除旧的"AI 简历"、"模板"、"资源工具"链接

#### App.tsx 路由重构
- 所有公开页面路由添加 `PublicLayout` 包裹
- TraePage 使用 `fullPage` 模式避免 padding-top
- Login/Register 使用条件渲染（未登录显示 PublicLayout，已登录跳转 dashboard）
- 新增 `CareerPage` 懒加载路由

#### 桌面端类型修复
- `ResumeListPage.tsx` — `data?.items` → `data?.data` (PaginatedResponse 类型修正)
- `TemplatesPage.tsx` — 同上

### 部署
- 构建并部署到 https://ndtool.cn/（2026-04-12 14:30 UTC+8）
- 33 个 asset 文件
- 后端新路由需要重启后端服务才能生效

### 待办
- [ ] 重启后端服务激活 `/api/v1/career/` 路由
- [ ] 测试 JD 评估 API 端到端流程
- [ ] Tauri v2 升级（支持 webkit2gtk-4.1，当前 v1 与系统不兼容）
- [ ] Windows/macOS 桌面端编译（需对应平台环境）
- [ ] HarmonyOS/iOS 编译（需对应 SDK）

---

## [2026-04-10 ~ 2026-04-11] 官网建设 + 全站风格统一

### 新增

#### 官网首页 (LandingPage)
- 12 个组件区块：Navbar, Hero, Stats, Features, HowItWorks, Testimonials, Pricing, Download, FAQ, CTA, Footer
- 设计系统：深色 (#050816) + 琥珀金 (#f59e0b) + 翡翠绿 (#10b981)
- 自定义 hooks：`useScrollAnimation`（IntersectionObserver）、`useCountUp`（requestAnimationFrame）
- 玻璃拟态卡片、渐变动画、滚动触发动画
- Scoped CSS：`.landing-page` 前缀隔离样式

#### Trae AI 页面 (`/trae`)
- 从 git 历史 (commit 25915bd) 恢复原始 Trae.ai 推广页
- 独立 CSS：`.trae-page` 前缀
- 路由：`/trae`

#### Android 安装包
- Flutter APK (52MB) → `public/downloads/ai-resume-android.apk`

### 修改

#### 全站颜色统一（13 个页面）
- `tailwind.config.js` — primary: amber, accent: emerald, cyber 色更新
- LoginPage, RegisterPage, ForgotPasswordPage — sky/blue → amber/emerald
- AboutPage, HelpPage, TermsPage, PrivacyPage — 浅色 → 深色
- HomePage, ResumeListPage, TemplatesPage, ProfilePage, SettingsPage — accent 色

#### SEO
- `index.html` — 完整 meta tags, OG tags, Twitter Card, JSON-LD Schema
- 字体：Space Grotesk (标题) + DM Sans (正文)

### 部署
- 2026-04-10 01:08 UTC+8 → https://ndtool.cn/
- Playwright 测试 8/10 通过

### Commit 记录
```
459d3c9 feat: 统一全站设计风格 + 恢复Trae页面 + 提供Android安装包
```

---

## 项目状态

| 模块 | 状态 | 备注 |
|------|------|------|
| 官网首页 | ✅ 已上线 | https://ndtool.cn/ |
| 全局导航 | ✅ 已上线 | 所有公开页面统一菜单 |
| 职业智能中心 | ⚠️ 前端已部署，后端待重启 | https://ndtool.cn/career |
| Trae AI 页面 | ✅ 已上线 | https://ndtool.cn/trae |
| Android APK | ✅ 已提供 | 52MB Flutter |
| Linux 桌面端 | ❌ 阻塞 | Tauri v1 与 webkit2gtk-4.1 不兼容 |
| Windows 桌面端 | ❌ 待做 | 需 Windows 环境交叉编译 |
| macOS 桌面端 | ❌ 待做 | 需 macOS 环境 |
| iOS | ❌ 待做 | 需 macOS + Xcode |
| HarmonyOS | ❌ 待做 | 需 HarmonyOS SDK |
