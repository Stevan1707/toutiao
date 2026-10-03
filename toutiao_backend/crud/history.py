from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History


async def add_history(db_session : AsyncSession, user_id : int, news_id : int):
    """添加收藏"""
    history = History(user_id=user_id, news_id=news_id)
    db_session.add(history)
    await db_session.commit()
    return history
