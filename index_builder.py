# index_builder.py

import os
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from data_loader import load_minecraft_qa

def get_or_build_index(data_path: str, index_save_path: str) -> VectorStoreIndex:
    """
    如果索引存在于磁盘，则加载它；否则，从数据构建一个新的索引。
    """
    if os.path.exists(index_save_path):
        print(f"从 {index_save_path} 加载现有索引...")
        storage_context = StorageContext.from_defaults(persist_dir=index_save_path)
        index = load_index_from_storage(storage_context)
        print("索引加载成功！")
    else:
        print("未找到现有索引，开始构建新索引...")
        # 1. 加载文档
        documents = load_minecraft_qa(data_path)
        if not documents:
            raise ValueError("未能加载任何文档，无法构建索引。")
        
        # 2. 构建索引
        index = VectorStoreIndex.from_documents(documents,show_progress=True)
        
        # 3. 保存索引到磁盘
        print(f"正在将索引保存到 {index_save_path}...")
        index.storage_context.persist(persist_dir=index_save_path)
        print("索引构建并保存成功！")
        
    return index