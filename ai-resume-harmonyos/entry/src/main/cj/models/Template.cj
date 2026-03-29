// Template.cj - 简历模板数据模型
package models

import std.collection.*

public class Template {
    public var id: Int64 = 0
    public var name: String = ""
    public var description: String = ""
    public var category: String = ""
    public var preview: String = ""
    public var style: TemplateStyle = TemplateStyle()
    public var isPremium: Bool = false
    public var isActive: Bool = true
    public var usageCount: Int64 = 0
    public var createdAt: String = ""

    public init() {}

    public init(
        id: Int64,
        name: String,
        description: String,
        category: String,
        preview: String,
        style: TemplateStyle,
        isPremium: Bool,
        isActive: Bool,
        usageCount: Int64,
        createdAt: String
    ) {
        this.id = id
        this.name = name
        this.description = description
        this.category = category
        this.preview = preview
        this.style = style
        this.isPremium = isPremium
        this.isActive = isActive
        this.usageCount = usageCount
        this.createdAt = createdAt
    }
}

public class TemplateStyle {
    public var primaryColor: String = "#2563eb"
    public var secondaryColor: String = "#64748b"
    public var backgroundColor: String = "#ffffff"
    public var textColor: String = "#1e293b"
    public var fontFamily: String = "HarmonyOS Sans"
    public var fontSize: Int32 = 12
    public var lineHeight: Float32 = 1.5f
    public var margin: Int32 = 20
    public var padding: Int32 = 15

    public init() {}

    public init(
        primaryColor: String,
        secondaryColor: String,
        backgroundColor: String,
        textColor: String,
        fontFamily: String,
        fontSize: Int32,
        lineHeight: Float32,
        margin: Int32,
        padding: Int32
    ) {
        this.primaryColor = primaryColor
        this.secondaryColor = secondaryColor
        this.backgroundColor = backgroundColor
        this.textColor = textColor
        this.fontFamily = fontFamily
        this.fontSize = fontSize
        this.lineHeight = lineHeight
        this.margin = margin
        this.padding = padding
    }
}

public class TemplateCategory {
    public var id: String = ""
    public var name: String = ""
    public var icon: String = ""
    public var count: Int32 = 0

    public init() {}

    public init(id: String, name: String, icon: String, count: Int32) {
        this.id = id
        this.name = name
        this.icon = icon
        this.count = count
    }
}
