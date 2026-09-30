from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite


async def is_favorite(
        db_session: AsyncSession,
        user_id: int,
        news_id: int,
):
    """检查用户是否有收藏这条新闻"""
    stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none() is not None  # 返回布尔值

async def add_favorite(
        db_session: AsyncSession,
        user_id: int,
        news_id: int,
):
    """添加收藏"""
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db_session.add(favorite)
    await db_session.commit()
    await db_session.refresh(favorite)
    return favorite
