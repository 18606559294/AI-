# AI Resume - HarmonyOS Version (仓颉语言)

基于仓颉(Cangjie)语言开发的鸿蒙原生简历生成应用。

## 项目结构

```
ai-resume-harmonyos/
├── entry/                    # 主入口模块
│   └── src/
│       └── main/
│           ├── cj/           # 仓颉源代码
│           │   ├── entry/
│           │   │   └── EntryStage.cj
│           │   ├── models/   # 数据模型
│           │   ├── views/    # UI视图
│           │   ├── viewmodels/ # 视图模型
│           │   ├── services/ # 服务层
│           │   └── utils/    # 工具类
│           ├── resources/    # 资源文件
│           └── module.json5  # 模块配置
├── build-profile.json5       # 构建配置
├── hvigorfile.ts            # 构建脚本
└── oh-package.json5         # 依赖配置
```

## 功能特性

- AI智能简历生成
- 多模板支持
- 富文本编辑器
- 多格式导出 (PDF/Word)
- 用户认证
- 离线缓存

## 技术栈

- **语言**: 仓颉 (Cangjie)
- **框架**: HarmonyOS Next SDK
- **UI**: ArkUI 声明式UI
- **网络**: HTTP Client
- **存储**: Preferences, RDB

## 开发环境要求

- DevEco Studio 4.0+
- HarmonyOS SDK API 10+
- Node.js 16+

## 快速开始

1. 使用 DevEco Studio 打开项目
2. 同步项目依赖
3. 连接鸿蒙设备或启动模拟器
4. 点击运行

## 后端API

应用连接到 AI Resume 后端服务:
- 开发环境: http://localhost:8000
- 生产环境: 配置在 `services/ApiConfig.cj`

## 许可证

MIT License
