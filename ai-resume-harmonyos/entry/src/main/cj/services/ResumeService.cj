// ResumeService.cj - 简历服务
package services

import models.*
import std.collection.*
import std.json.*

public class ResumeService {
    private let httpClient: HttpClient

    public init(httpClient: HttpClient) {
        this.httpClient = httpClient
    }

    // 获取所有简历
    public func getResumes(): Result<ArrayList<Resume>> {
        let response = httpClient.get(ApiConfig.RESUMES)

        if (response.isSuccess()) {
            let resumes = parseResumeList(response.body)
            return Result<ArrayList<Resume>>.success(resumes)
        }

        return Result<ArrayList<Resume>>.failure(response.error)
    }

    // 获取单个简历
    public func getResume(id: Int64): Result<Resume> {
        let endpoint = ApiConfig.RESUME_BY_ID.replace("{id}", id.toString())
        let response = httpClient.get(endpoint)

        if (response.isSuccess()) {
            let resume = parseResume(response.body)
            return Result<Resume>.success(resume)
        }

        return Result<Resume>.failure(response.error)
    }

    // 创建简历
    public func createResume(title: String, templateId: Int64): Result<Resume> {
        let body = "{\"title\": \"${title}\", \"template_id\": ${templateId}}"
        let response = httpClient.post(ApiConfig.RESUMES, body)

        if (response.isSuccess()) {
            let resume = parseResume(response.body)
            return Result<Resume>.success(resume)
        }

        return Result<Resume>.failure(response.error)
    }

    // 更新简历
    public func updateResume(id: Int64, resume: Resume): Result<Resume> {
        let endpoint = ApiConfig.RESUME_BY_ID.replace("{id}", id.toString())
        let body = serializeResume(resume)
        let response = httpClient.put(endpoint, body)

        if (response.isSuccess()) {
            let updated = parseResume(response.body)
            return Result<Resume>.success(updated)
        }

        return Result<Resume>.failure(response.error)
    }

    // 删除简历
    public func deleteResume(id: Int64): Result<Bool> {
        let endpoint = ApiConfig.RESUME_BY_ID.replace("{id}", id.toString())
        let response = httpClient.delete(endpoint)

        if (response.isSuccess()) {
            return Result<Bool>.success(true)
        }

        return Result<Bool>.failure(response.error)
    }

    // AI生成简历内容
    public func generateResume(request: AIGenerateRequest): Result<AIGenerateResponse> {
        let body = serializeAIGenerateRequest(request)
        let response = httpClient.post(ApiConfig.RESUME_GENERATE, body)

        if (response.isSuccess()) {
            let aiResponse = parseAIGenerateResponse(response.body)
            return Result<AIGenerateResponse>.success(aiResponse)
        }

        return Result<AIGenerateResponse>.failure(response.error)
    }

    // 解析简历列表
    private func parseResumeList(json: String): ArrayList<Resume> {
        let resumes = ArrayList<Resume>()
        try {
            let arr = JsonParser.parseArray(json)
            for (i in 0..arr.size()) {
                let obj = arr.getObject(i)
                resumes.add(parseResumeFromObject(obj))
            }
        } catch (e: Exception) {
            println("Failed to parse resume list: ${e.message}")
        }
        return resumes
    }

    // 解析单个简历
    private func parseResume(json: String): Resume {
        try {
            let obj = JsonParser.parse(json)
            return parseResumeFromObject(obj)
        } catch (e: Exception) {
            println("Failed to parse resume: ${e.message}")
            return Resume()
        }
    }

    // 从JSON对象解析简历
    private func parseResumeFromObject(obj: JsonObject): Resume {
        let resume = Resume()
        resume.id = obj.getInt64("id", 0)
        resume.userId = obj.getInt64("user_id", 0)
        resume.title = obj.getString("title", "")
        resume.content = obj.getString("content", "")
        resume.templateId = obj.getInt64("template_id", 0)
        resume.templateName = obj.getString("template_name", "")
        resume.status = obj.getString("status", "draft")
        resume.version = obj.getInt32("version", 1)
        resume.createdAt = obj.getString("created_at", "")
        resume.updatedAt = obj.getString("updated_at", "")

        // 解析标签
        let tagsArr = obj.getArray("tags")
        for (i in 0..tagsArr.size()) {
            resume.tags.add(tagsArr.getString(i))
        }

        return resume
    }

    // 序列化简历 - 使用安全的 JSON 序列化
    private func serializeResume(resume: Resume): String {
        let obj = JsonObject()
        obj.put("title", resume.title)
        obj.put("content", resume.content)
        obj.put("template_id", resume.templateId)
        obj.put("status", resume.status)
        return obj.toJson()
    }

    // 序列化AI生成请求 - 使用安全的 JSON 序列化
    private func serializeAIGenerateRequest(request: AIGenerateRequest): String {
        let obj = JsonObject()
        obj.put("resume_id", request.resumeId)
        obj.put("section", request.section)
        obj.put("prompt", request.prompt)
        obj.put("context", request.context)
        obj.put("template_id", request.templateId)
        return obj.toJson()
    }

    // 解析AI生成响应
    private func parseAIGenerateResponse(json: String): AIGenerateResponse {
        let response = AIGenerateResponse()
        try {
            let obj = JsonParser.parse(json)
            response.content = obj.getString("content", "")
            response.tokens = obj.getInt64("tokens", 0)
            response.provider = obj.getString("provider", "")
            response.model = obj.getString("model", "")
        } catch (e: Exception) {
            println("Failed to parse AI response: ${e.message}")
        }
        return response
    }
}
