from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_database_session
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags = ["history"])

@router.post("/add")
async def add_history(
        data : HistoryAddRequest,
        user : User = Depends(get_current_user),
        db_session : AsyncSession = Depends(get_database_session)
):
    """添加历史记录"""
    result = await history.add_history(db_session, user.id, data.news_id)
    return success_response(message="添加浏览历史成功", data=result)


