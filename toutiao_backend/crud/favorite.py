from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


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


async def remove_favorite(
        db_session: AsyncSession,
        user_id: int,
        news_id: int,
):
    """删除收藏"""
    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db_session.execute(stmt)
    await db_session.commit()
    return result


async def get_favorite_list(db_session : AsyncSession,
                      user_id: int ,
                      page: int = 1,
                      page_size: int = 10):
    """获取收藏列表"""

    count_stmt = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
    total_result = await db_session.execute(count_stmt)
    total = total_result.scalar_one_or_none()

    offset = (page - 1) * page_size

    query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
             .join(News, Favorite.news_id == News.id)
             .where(Favorite.user_id == user_id)
             .order_by(Favorite.created_at.desc())
             .offset(offset)
             .limit(page_size)
             )
    result = await db_session.execute(query)
    favorite_list = result.all()
    return total, favorite_list




