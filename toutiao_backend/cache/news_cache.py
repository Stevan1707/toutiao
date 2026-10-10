# 对新闻的各类属性进行缓存操作
from typing import List, Dict, Any

from config.cache_conf import get_cache_json, set_cache

CATEGORY_KEY = "news.category"

# 获取缓存的新闻列表
async def get_cached_category():
    return await get_cache_json(CATEGORY_KEY)

# 数据越稳定，缓存越持久，过期时间越长
# 新闻分类数据稳定，设置为2小时
async def set_cached_category(data : List[Dict[str,Any]], ex: int = 7200):
    return await set_cache(CATEGORY_KEY, data, ex)