# data_loader.py

import json
from llama_index.core import Document
from typing import List

def load_minecraft_qa(file_path: str) -> List[Document]:
    """从指定的JSON文件加载问答数据并转换为Document对象列表"""
    print(f"从 {file_path} 加载数据...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        documents = []
        for item in json_data:
            doc = Document(
                text=item['answer'],
                metadata={
                    'question': item['question'],
                    'source': item['source']
                }
            )
            documents.append(doc)
        
        print(f"数据加载成功！共解析了 {len(documents)} 个文档。")
        return documents
    except FileNotFoundError:
        print(f"错误: 文件未找到 at '{file_path}'")
        return []
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        return []