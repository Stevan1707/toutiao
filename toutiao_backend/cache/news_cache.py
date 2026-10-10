# 对新闻的各类属性进行缓存操作
from typing import List, Dict, Any

from config.cache_conf import get_cache_json, set_cache

CATEGORY_KEY = "news.category"

# 获取缓存的新闻列表
async def get_cached_category():
    """获取新闻分类缓存"""
    return await get_cache_json(CATEGORY_KEY)

# 数据越稳定，缓存越持久，过期时间越长
# 新闻分类数据稳定，设置为2小时
async def set_cached_category(data : List[Dict[str,Any]], ex: int = 7200):
    """设置新闻分类缓存"""
    return await set_cache(CATEGORY_KEY, data, ex)

# key = news_list : 分类id: 页码: 每页数量  + 列表数据 + 过期时间
async def set_cached_news_list(category_id : int, page: int, page_size: int, data : List[Dict[str,Any]], ex: int = 3600):
    """设置新闻列表缓存"""
    category_part = category_id if category_id is not None else "all"

    key = f"news_list:{category_part}:{page}:{page_size}"
    return await set_cache(key, data, ex)


async def get_cached_news_list(category_id : int, page: int, page_size: int):
    """获取新闻列表缓存"""
    category_part = category_id if category_id is not None else "all"

    key = f"news_list:{category_part}:{page}:{page_size}"
    return await get_cache_json(key)
