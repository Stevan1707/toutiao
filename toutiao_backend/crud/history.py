from fastapi import HTTPException
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_history(db_session : AsyncSession, user_id : int, news_id : int):
    """添加收藏"""
    history = History(user_id=user_id, news_id=news_id)
    db_session.add(history)
    await db_session.commit()
    return history


async def get_history_list(
        db_session: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    """获取历史记录列表"""
    count_stmt = select(func.count(History.id)).where(History.user_id == user_id)
    count = await db_session.execute(count_stmt)
    total = count.scalar_one_or_none()

    offset = (page - 1) * page_size
    query = (
        select(News, History.id.label("historyId"), History.view_time.label("viewTime"))
        .join(History, News.id == History.news_id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )
    news = await db_session.execute(query)
    news_list = news.all()

    # 如果select里面有两个表的东西则不能用scalars_all(),仅能用all()

    return total, news_list


async def delete_history(db: AsyncSession, user_id: int, news_id: int):
    """删除单条历史记录"""
    query = delete(History).where(History.user_id == user_id, History.news_id == news_id)  # 删的是新闻不是存储在History表格内的id

    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0

async def clear_history(db_session: AsyncSession, user_id: int):
    """清空全部历史记录"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db_session.execute(stmt)
    await db_session.commit()
    count = result.rowcount

    return count or 0

