from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_category, set_cached_category, set_cached_news_list, get_cached_news_list
from models.news import Category, News
from sqlalchemy import select, func, update

from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    """ 获取所有分类列表 """

    # 尝试从缓存中读取：
    cached_category = await get_cached_category()
    print(f"[DEBUG] 读取缓存结果: {cached_category}")
    if cached_category:
        print("[DEBUG] 命中缓存，直接返回")
        return cached_category
    # 如果缓存中没有，从数据库中读取
    stmt = select(Category).order_by(Category.sort_order).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    print(f"[DEBUG] 数据库查询到 {len(categories)} 条分类")

    # 写入缓存：
    if categories:
        categories = jsonable_encoder(categories)
        print(f"[DEBUG] jsonable_encoder 后类型: {type(categories)}, 内容: {categories}")
        result_cache = await set_cached_category(categories)
        print(f"[DEBUG] 缓存写入结果: {result_cache}")

    # 返回分类列表
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 先尝试从缓存获取新闻列表
    # 跳过的数量skip = (页码 -1) * 每页数量 → 页码 = 跳过的数量 // 每页数量 + 1
    # await get_cache_news_list(分类id, 页码, 每页数量)
    page = skip // limit + 1
    cached_list = await get_cached_news_list(category_id, page, limit)  # 缓存数据 json
    if cached_list:
        # return cached_list  # 要的是 ORM
        return [News(**item) for item in cached_list]

    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        # 先把 ORM 数据 转换 字典才能写入缓存
        # ORM 转成 Pydantic，再转为 字典
        # by_alias=False 不适用别名，保存 Python 风格，因为 Redis 数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cached_news_list(category_id, page, limit, news_data)

    return news_list


async def get_news_total(db: AsyncSession, category_id: int):
    """ 获取指定分类下的新闻总数 """
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 仅返回一个值否则报错

async def get_news_detail(db: AsyncSession, news_id: int):
    """ 获取指定新闻详情 """
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_news_views(db_session, news_id:int):
    """ 更新新闻点击量 """
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db_session.execute(stmt)
    await db_session.commit()  # 以防万一这里再次提交事务

    # 强化逻辑，防止出现浏览量并没有增加的问题，检查数据库是否真的命中了数据，有没有行被更新
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5 ):
    """ 获取指定新闻下的相关新闻列表 """
    stmt = (select(News)
            .where(News.category_id == category_id)
            .order_by(News.views.desc(),News.publish_time.desc())
            .limit(limit))
    result = await db.execute(stmt)
    # return result.scalars().all()
    # 使用列表推导式来返回想要的参数
    related_news_list = [{
        "id": i.id,
        "title": i.title,
        "content": i.content,
        "image": i.image,
        "author": i.author,
        "publishTime": i.publish_time,
        "categoryId": i.category_id,
        "views": i.views,
    } for i in result.scalars().all()]
    return related_news_list