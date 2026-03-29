// HomePage.cj - 主页
package views

import ohos.arkui.*
import ohos.arkui.state.*
import ohos.arkui.node.*
import services.*
import models.*
import std.collection.*

@Entry
@Component
public struct HomePage {
    @State private var resumes: ArrayList<Resume> = ArrayList<Resume>()
    @State private var isLoading: Bool = true
    @State private var currentTab: Int32 = 0

    private let resumeService: ResumeService
    private let authService: AuthService = AuthService()

    public init() {
        let httpClient = HttpClient(ApiConfig.BASE_URL + ApiConfig.API_VERSION)
        let token = authService.getCurrentToken()
        if (token.accessToken != "") {
            httpClient.setAuthToken(token.accessToken)
        }
        this.resumeService = ResumeService(httpClient)
    }

    public func aboutToAppear(): void {
        this.loadResumes()
    }

    public func build(): void {
        Column() {
            // 顶部栏
            this.buildHeader()

            // 标签页
            this.buildTabs()

            // 内容区域
            if (isLoading) {
                this.buildLoading()
            } else {
                this.buildContent()
            }

            // 底部导航
            this.buildBottomNav()
        }
        .width("100%")
        .height("100%")
        .backgroundColor("#f5f5f5")
    }

    @Builder
    private func buildHeader(): void {
        Row() {
            Text("AI 简历")
                .fontSize(20)
                .fontWeight(FontWeight.Bold)
                .fontColor("#1e293b")

            Blank()

            // 用户头像
            Image($r("app.media.avatar_default"))
                .width(36)
                .height(36)
                .borderRadius(18)
                .onClick {
                    Router.push({ url: "pages/ProfilePage" })
                }
        }
        .width("100%")
        .height(56)
        .padding({ left: 16, right: 16 })
        .backgroundColor("#ffffff")
        .shadow({ radius: 2, color: "#1e293b", offsetX: 0, offsetY: 2 })
    }

    @Builder
    private func buildTabs(): void {
        Row() {
            ForEach(["我的简历", "模板", "AI助手"], { (item: String, index: Int32) =>
                Text(item)
                    .fontSize(14)
                    .fontColor(currentTab == index ? "#2563eb" : "#64748b")
                    .fontWeight(currentTab == index ? FontWeight.Bold : FontWeight.Normal)
                    .padding({ left: 16, right: 16, top: 12, bottom: 12 })
                    .onClick {
                        currentTab = index
                    }
            })
        }
        .width("100%")
        .backgroundColor("#ffffff")
        .justifyContent(FlexAlign.SpaceAround)
    }

    @Builder
    private func buildLoading(): void {
        Column() {
            LoadingProgress()
                .width(48)
                .height(48)
                .color("#2563eb")

            Text("加载中...")
                .fontSize(14)
                .fontColor("#64748b")
                .margin({ top: 16 })
        }
        .width("100%")
        .height("100%")
        .justifyContent(FlexAlign.Center)
    }

    @Builder
    private func buildContent(): void {
        if (currentTab == 0) {
            this.buildResumeList()
        } else if (currentTab == 1) {
            this.buildTemplateList()
        } else {
            this.buildAIAssistant()
        }
    }

    @Builder
    private func buildResumeList(): void {
        Column() {
            if (resumes.size() == 0) {
                this.buildEmptyState()
            } else {
                List() {
                    ForEach(resumes, { (resume: Resume) =>
                        ListItem() {
                            this.buildResumeItem(resume)
                        }
                    })
                }
                .width("100%")
                .layoutWeight(1)
            }

            // 创建按钮
            this.buildCreateButton()
        }
        .width("100%")
        .layoutWeight(1)
    }

    @Builder
    private func buildEmptyState(): void {
        Column() {
            Image($r("app.media.empty_resume"))
                .width(120)
                .height(120)

            Text("还没有简历")
                .fontSize(16)
                .fontColor("#1e293b")
                .margin({ top: 16 })

            Text("点击下方按钮创建第一份简历")
                .fontSize(14)
                .fontColor("#64748b")
                .margin({ top: 8 })
        }
        .width("100%")
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
    }

    @Builder
    private func buildResumeItem(resume: Resume): void {
        Row() {
            Column() {
                Text(resume.title)
                    .fontSize(16)
                    .fontWeight(FontWeight.Bold)
                    .fontColor("#1e293b")

                Text(resume.templateName)
                    .fontSize(12)
                    .fontColor("#64748b")
                    .margin({ top: 4 })

                Row() {
                    Text(resume.status == "draft" ? "草稿" : "已完成")
                        .fontSize(10)
                        .fontColor("#ffffff")
                        .backgroundColor(resume.status == "draft" ? "#f59e0b" : "#10b981")
                        .borderRadius(4)
                        .padding({ left: 6, right: 6, top: 2, bottom: 2 })

                    Text("版本 ${resume.version}")
                        .fontSize(10)
                        .fontColor("#64748b")
                        .margin({ left: 8 })
                }
                .margin({ top: 8 })
            }
            .alignItems(HorizontalAlign.Start)
            .layoutWeight(1)

            Image($r("app.media.ic_arrow_right"))
                .width(24)
                .height(24)
        }
        .width("100%")
        .padding(16)
        .backgroundColor("#ffffff")
        .margin({ top: 8 })
        .borderRadius(8)
        .onClick {
            Router.push({ url: "pages/ResumeEditorPage", params: { "resumeId": resume.id } })
        }
    }

    @Builder
    private func buildCreateButton(): void {
        Button("创建新简历")
            .width("90%")
            .height(48)
            .fontSize(16)
            .fontColor("#ffffff")
            .backgroundColor("#2563eb")
            .borderRadius(8)
            .margin({ top: 16, bottom: 16 })
            .onClick {
                Router.push({ url: "pages/TemplateSelectPage" })
            }
    }

    @Builder
    private func buildTemplateList(): void {
        Column() {
            Text("模板列表")
                .fontSize(16)
                .fontColor("#1e293b")
        }
        .width("100%")
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
    }

    @Builder
    private func buildAIAssistant(): void {
        Column() {
            Text("AI助手")
                .fontSize(16)
                .fontColor("#1e293b")
        }
        .width("100%")
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
    }

    @Builder
    private func buildBottomNav(): void {
        Row() {
            this.buildNavItem("首页", $r("app.media.ic_home"), 0)
            this.buildNavItem("模板", $r("app.media.ic_template"), 1)
            this.buildNavItem("AI", $r("app.media.ic_ai"), 2)
            this.buildNavItem("我的", $r("app.media.ic_profile"), 3)
        }
        .width("100%")
        .height(56)
        .backgroundColor("#ffffff")
        .justifyContent(FlexAlign.SpaceAround)
        .shadow({ radius: 4, color: "#1e293b", offsetX: 0, offsetY: -2 })
    }

    @Builder
    private func buildNavItem(label: String, icon: Resource, index: Int32): void {
        Column() {
            Image(icon)
                .width(24)
                .height(24)
                .color(currentTab == index ? "#2563eb" : "#64748b")

            Text(label)
                .fontSize(10)
                .fontColor(currentTab == index ? "#2563eb" : "#64748b")
                .margin({ top: 4 })
        }
        .onClick {
            currentTab = index
        }
    }

    private func loadResumes(): void {
        isLoading = true
        let result = resumeService.getResumes()
        isLoading = false

        if (result.isSuccess()) {
            let value = result.getValue()
            if (value is Some<ArrayList<Resume>>) {
                resumes = value.get()
            }
        }
    }
}
