from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from sqlalchemy import select, func


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