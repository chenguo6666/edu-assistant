from functools import lru_cache
import hashlib
import json

class RAGCache:
    """简单的文档检索缓存"""
    
    def __init__(self, maxsize: int = 128):
        self.cache = {}
        self.maxsize = maxsize
    
    def get_cache_key(self, query: str, user_id: int, k: int) -> str:
        """生成缓存键"""
        content = f"{query}_{user_id}_{k}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value: str):
        if len(self.cache) >= self.maxsize:
            # 简单移除第一个键
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value