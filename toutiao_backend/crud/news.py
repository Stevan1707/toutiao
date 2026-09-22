from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category
from sqlalchemy import select

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Category).order_by(Category.sort_order).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
