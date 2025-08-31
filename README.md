# RAG_Qwen_Minevraft
## ⚠️因BGE以及QWEN-7B模型较大，而GitHub仅允许25MB以下文件的上传，故暂不上传，若有需要可联系sunjx1009@163.com
## 项目概览
  这是一个基于RAG（检索增强生成）技术的Minecraft游戏知识问答系统，使用了Qwen2.5-7B-Instruct大语言模型和BGE嵌入模型，通过Flask提供Web界面。
### RAG对话示例
<img width="451" height="607" alt="image" src="https://github.com/user-attachments/assets/33c7e63f-70f7-43de-98eb-b25838387deb" />

### 服务启动示例
<img width="735" height="481" alt="2025-08-31 21-12-02屏幕截图" src="https://github.com/user-attachments/assets/3bc63cf1-a6de-414f-a06c-3a4f2b9bba51" />

## 项目结构
<img width="526" height="635" alt="image" src="https://github.com/user-attachments/assets/510197aa-5926-48d0-a296-159aabbed845" />

## 数据集（minecraft-question-answer-700k）
  介绍最大的Minecraft问答数据集，涵盖了Minecraft中的每个主题、游戏机制、物品和制作方法。该数据集是通过提取超过18000个Minecraft Wiki页面，并使用glaive.ai的合成数据生成的。
- 行数 - 694,814
- 令牌数 - 47,133,624
- 来源 - https://minecraft.wiki/
```
{
        "question": "What is the first statistic to decrease when a player performs energy-intensive actions in Minecraft?",
        "answer": "Saturation is the first statistic to decrease when a player performs energy-intensive actions, and it must be completely depleted before the visible hunger meter begins decreasing.",
        "source": "https://minecraft.wiki/w/Food#Nourishment_value"
    },
    {
        "question": "How does the game handle the consumption of cake when compared to eating other types of food?",
        "answer": "Eating cake is distinct from other foods, as it must be placed and then right-clicked on to consume, whereas other foods can be eaten directly by the player. Additionally, cake has 7 edible slices, which become thinner as each slice is removed, whereas other foods typically restore a set amount of hunger and saturation points without any slice-based consumption mechanism.",
        "source": "https://minecraft.wiki/w/Food#Nourishment_value"
    },
    {
        "question": "What is the average hunger restoration value of wheat in Minecraft?",
        "answer": "The average hunger restoration value of wheat in Minecraft is 5. This means that consuming wheat will restore 5 hunger points, while also providing a moderate amount of saturation.",
        "source": "https://minecraft.wiki/w/Food#Nourishment_value"
    }
```

## RAG实现流程
### 1. 数据准备和加载
- 使用 data_loader.py 从JSON文件加载Minecraft问答数据
- 数据格式包含问题、答案和来源URL
- 将数据转换为Document对象，便于后续处理
### 2. 模型初始化
在 config.py 中完成以下配置：

- 加载 Qwen2.5-7B-Instruct 作为生成模型
  - 配置上下文窗口大小为8192
  - 设置最大生成token数为2048
  - 使用bfloat16数据类型优化内存使用
- 加载 BGE-base-en-v1.5 作为嵌入模型
  - 用于文本向量化
  - 自动检测并使用GPU加速
### 3. 索引构建
index_builder.py 负责向量索引的管理：

- 检查 /media/sdb1/sjx/ragMinecraft/saved_index/ 是否存在现有索引
- 如果存在，直接加载已有索引
- 如果不存在：
  1. 使用BGE模型将所有文档转换为向量
  2. 构建新的VectorStoreIndex
  3. 将索引保存到磁盘
### 4. 查询处理流程
#### 4.1 用户输入处理
- 通过Web界面接收用户问题
- Flask后端接收POST请求到 /api/query 端点
#### 4.2 检索增强
1. 向量化查询
   - 使用BGE模型将用户问题转换为向量
2. 相似度检索
   - 在向量索引中检索最相似的3个文档
   - 计算相似度分数
3. 上下文组装
   - 将检索到的文档作为上下文
   - 保留原始问题和来源信息
#### 4.3 答案生成
- 使用Qwen2.5-7B-Instruct模型：
  - 输入：用户问题 + 检索到的上下文
  - 使用特定的prompt模板格式化输入
  - 生成针对性的回答
#### 4.4 结果返回
返回JSON格式的响应：

```
{
    "answer": "生成的回答",
    "sources": [
        {
            "question": "原始问题",
            "source": "来源URL",
            "score": "相似度分数"
        }
    ]
}
```

## 数据流程
1. 用户在Web界面输入Minecraft相关问题
2. 前端JavaScript发送请求到Flask API
3. Flask应用调用RAG系统处理查询：
   - 使用BGE嵌入模型将查询转换为向量
   - 从向量索引中检索相关文档
   - 使用Qwen2.5-7B模型生成回答
4. 返回结果和参考来源到前端
5. 前端显示回答和相关来源

## 技术栈
- 后端 : Python, Flask, llama_index
- 模型 : Qwen2.5-7B-Instruct (LLM), BGE-base-en-v1.5 (嵌入模型)
- 前端 : HTML, CSS, JavaScript
- 数据 : Minecraft问答数据集 (约70万问答对)
