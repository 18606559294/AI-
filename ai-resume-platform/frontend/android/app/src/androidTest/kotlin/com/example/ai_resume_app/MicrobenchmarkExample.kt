package com.example.ai_resume_app

import androidx.benchmark.junit4.BenchmarkRule
import androidx.benchmark.junit4.measureRepeated
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import kotlin.random.Random

/**
 * Microbenchmark性能测试示例
 * 用于测试特定代码片段的性能
 * 
 * 使用方法：
 * 1. 在Android Studio中运行测试
 * 2. 确保使用release构建（benchmark需要在非debug环境下运行）
 * 3. 测试结果会显示在控制台和报告中
 */
@RunWith(AndroidJUnit4::class)
class MicrobenchmarkExample {

    @get:Rule
    val benchmarkRule = BenchmarkRule()

    /**
     * 测试列表操作性能
     */
    @Test
    fun benchmarkListOperations() {
        benchmarkRule.measureRepeated {
            val list = mutableListOf<Int>()
            repeat(1000) {
                list.add(it)
            }
            list.sort()
        }
    }

    /**
     * 测试字符串操作性能
     */
    @Test
    fun benchmarkStringOperations() {
        benchmarkRule.measureRepeated {
            val result = StringBuilder()
            repeat(100) {
                result.append("测试文本")
            }
            result.toString()
        }
    }

    /**
     * 测试JSON解析性能
     */
    @Test
    fun benchmarkJsonParsing() {
        val jsonString = """
        {
            "name": "张三",
            "age": 30,
            "email": "zhangsan@example.com",
            "skills": ["Java", "Kotlin", "Flutter"]
        }
        """.trimIndent()

        benchmarkRule.measureRepeated {
            // 实际项目中这里会使用JSON解析库
            jsonString.contains("张三")
        }
    }

    /**
     * 测试数据计算性能
     */
    @Test
    fun benchmarkDataCalculation() {
        benchmarkRule.measureRepeated {
            var sum = 0
            for (i in 0 until 10000) {
                sum += i * i
            }
            sum
        }
    }

    /**
     * 测试数据库查询性能模拟
     */
    @Test
    fun benchmarkDatabaseQuery() {
        val data = List(1000) { 
            mapOf("id" to it, "name" to "User$it", "score" to Random.nextInt(100))
        }

        benchmarkRule.measureRepeated {
            data.filter { it["score"] as Int > 50 }
                .sortedByDescending { it["score"] }
                .take(10)
        }
    }

    // 更多性能测试示例：
    /*
    @Test
    fun benchmarkRecyclerViewUpdate() {
        // 测试RecyclerView数据更新性能
        benchmarkRule.measureRepeated {
            val adapter = createTestAdapter()
            adapter.submitList(createTestList(100))
        }
    }
    
    @Test
    fun benchmarkImageLoading() {
        // 测试图片加载性能
        benchmarkRule.measureRepeated {
            loadImageFromUrl("https://example.com/image.jpg")
        }
    }
    
    @Test
    fun benchmarkNetworkRequest() {
        // 测试网络请求性能（使用mock数据）
        benchmarkRule.measureRepeated {
            val mockResponse = createMockResponse()
            parseResponse(mockResponse)
        }
    }
    */
}

/*
运行Microbenchmark的步骤：
1. 确保使用Android Studio最新版本
2. 创建benchmark运行配置
3. 设置build variant为release
4. 运行测试

注意事项：
- Benchmark测试必须在release或benchmark构建类型下运行
- 测试结果会受到设备性能影响，建议在真机上测试
- 避免在benchmark测试中调用耗时操作（如网络请求）
- 每个benchmark至少运行10次以获得稳定结果
*/