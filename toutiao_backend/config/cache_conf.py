# 配置redis配置文件
import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,  # 数据库索引，默认0
    decode_responses=True,
    protocol=2)  # 强制 RESP2 协议，兼容 Windows 上的 Redis 3.x


# 封装读取操作
# 字符串：
async def get_cache(key: str):
#    return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"读取缓存失败: {e}")
        return None


# 列表或者字典：需要序列化
async def get_cache_json(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"读取json缓存失败: {e}")
        return None


# 封装设置缓存：
async def set_cache(key: str, value: Any, ex: int = 3600):
    if isinstance(value, (dict,list)):
        value = json.dumps(value, ensure_ascii= False)  # 防止中文变成乱码，出现编码问题
    try :
        await redis_client.setex(key, ex, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False