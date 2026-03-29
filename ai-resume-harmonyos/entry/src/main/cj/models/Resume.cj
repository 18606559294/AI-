// Resume.cj - 简历数据模型
package models

import std.collection.*

public class Resume {
    public var id: Int64 = 0
    public var userId: Int64 = 0
    public var title: String = ""
    public var content: String = ""
    public var templateId: Int64 = 0
    public var templateName: String = ""
    public var status: String = "draft"
    public var version: Int32 = 1
    public var tags: ArrayList<String> = ArrayList<String>()
    public var createdAt: String = ""
    public var updatedAt: String = ""

    public init() {}

    public init(
        id: Int64,
        userId: Int64,
        title: String,
        content: String,
        templateId: Int64,
        templateName: String,
        status: String,
        version: Int32,
        tags: ArrayList<String>,
        createdAt: String,
        updatedAt: String
    ) {
        this.id = id
        this.userId = userId
        this.title = title
        this.content = content
        this.templateId = templateId
        this.templateName = templateName
        this.status = status
        this.version = version
        this.tags = tags
        this.createdAt = createdAt
        this.updatedAt = updatedAt
    }
}

public class ResumeSection {
    public var id: String = ""
    public var type: String = ""
    public var title: String = ""
    public var content: String = ""
    public var order: Int32 = 0

    public init() {}

    public init(id: String, type: String, title: String, content: String, order: Int32) {
        this.id = id
        this.type = type
        this.title = title
        this.content = content
        this.order = order
    }
}

public class PersonalInfo {
    public var name: String = ""
    public var email: String = ""
    public var phone: String = ""
    public var location: String = ""
    public var website: String = ""
    public var summary: String = ""

    public init() {}

    public init(name: String, email: String, phone: String, location: String, website: String, summary: String) {
        this.name = name
        this.email = email
        this.phone = phone
        this.location = location
        this.website = website
        this.summary = summary
    }
}

public class Education {
    public var school: String = ""
    public var degree: String = ""
    public var field: String = ""
    public var startDate: String = ""
    public var endDate: String = ""
    public var description: String = ""

    public init() {}

    public init(school: String, degree: String, field: String, startDate: String, endDate: String, description: String) {
        this.school = school
        this.degree = degree
        this.field = field
        this.startDate = startDate
        this.endDate = endDate
        this.description = description
    }
}

public class Experience {
    public var company: String = ""
    public var position: String = ""
    public var startDate: String = ""
    public var endDate: String = ""
    public var location: String = ""
    public var description: String = ""
    public var achievements: ArrayList<String> = ArrayList<String>()

    public init() {}

    public init(
        company: String,
        position: String,
        startDate: String,
        endDate: String,
        location: String,
        description: String,
        achievements: ArrayList<String>
    ) {
        this.company = company
        this.position = position
        this.startDate = startDate
        this.endDate = endDate
        this.location = location
        this.description = description
        this.achievements = achievements
    }
}

public class Skill {
    public var name: String = ""
    public var level: String = ""
    public var category: String = ""

    public init() {}

    public init(name: String, level: String, category: String) {
        this.name = name
        this.level = level
        this.category = category
    }
}

public class ResumeData {
    public var personalInfo: PersonalInfo = PersonalInfo()
    public var education: ArrayList<Education> = ArrayList<Education>()
    public var experience: ArrayList<Experience> = ArrayList<Experience>()
    public var skills: ArrayList<Skill> = ArrayList<Skill>()
    public var projects: ArrayList<Project> = ArrayList<Project>()
    public var certifications: ArrayList<Certification> = ArrayList<Certification>()

    public init() {}
}

public class Project {
    public var name: String = ""
    public var description: String = ""
    public var technologies: ArrayList<String> = ArrayList<String>()
    public var url: String = ""
    public var startDate: String = ""
    public var endDate: String = ""

    public init() {}

    public init(
        name: String,
        description: String,
        technologies: ArrayList<String>,
        url: String,
        startDate: String,
        endDate: String
    ) {
        this.name = name
        this.description = description
        this.technologies = technologies
        this.url = url
        this.startDate = startDate
        this.endDate = endDate
    }
}

public class Certification {
    public var name: String = ""
    public var issuer: String = ""
    public var date: String = ""
    public var url: String = ""

    public init() {}

    public init(name: String, issuer: String, date: String, url: String) {
        this.name = name
        this.issuer = issuer
        this.date = date
        this.url = url
    }
}
