import config
from index_builder import get_or_build_index
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def main():
    print("1")
    print("--- RAG流程开始 ---")
    
    # 第1步：从config.py加载并设置模型
    config.setup_models()
    
    # 第2步：从index_builder.py获取或构建索引
    index = get_or_build_index(
        data_path=config.JSON_DATA_PATH,
        index_save_path=config.INDEX_SAVE_PATH
    )
    
    # 第3步：创建查询引擎
    print("创建查询引擎...")
    query_engine = index.as_query_engine(similarity_top_k=3)
    print("查询引擎已就绪！")
    
    # 第4步：执行查询
    test_query = "How is cake different from other food in Minecraft?"
    print(f"\n执行查询: {test_query}")
    
    response = query_engine.query(test_query)
    
    print("\n--- 生成的回答 ---")
    print(response)

    print("\n--- 检索到的来源信息 ---")
    for i, node in enumerate(response.source_nodes):
        print(f"来源 {i+1} (相似度: {node.score:.4f}):")
        print(f"  原始问题: {node.metadata.get('question', 'N/A')}")
        print(f"  来源链接: {node.metadata.get('source', 'N/A')}")
        print("-" * 20)

    print("\n--- RAG流程结束 ---")


if __name__ == "__main__":
    main()
