from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from sqlalchemy import select, func, update


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    """ 获取所有分类列表 """
    stmt = select(Category).order_by(Category.sort_order).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db: AsyncSession,category_id: int, skip: int = 0, limit: int = 10):
    """ 获取指定分类下的新闻列表 """
    stmt = select(News).where(News.category_id == category_id).order_by(News.id.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


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
