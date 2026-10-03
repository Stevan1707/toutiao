from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_database_session
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
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


@router.get("/list")
async def get_history_list(
        page : int = 1,
        page_size : int = Query(10, ge=1, le=100, alias="pageSize"),
        user : User = Depends(get_current_user),
        db_session : AsyncSession = Depends(get_database_session)
):
    """获取历史记录列表"""
    total, news_list = await history.get_history_list(db_session, user.id, page, page_size)
    history_list = [{**news.__dict__, "viewTime": vt} for news, vt in news_list]
    has_more = total > page * page_size
    data = HistoryListResponse(list=history_list, total=total, hasMore=has_more)
    return success_response(message="获取浏览历史成功", data=data)

@router.delete("/delete/{history_id}")
async def delete_history(
        history_id : int,
        user : User = Depends(get_current_user),
        db_session : AsyncSession = Depends(get_database_session)
):
    """删除历史记录"""
    await history.delete_history(db_session, user.id, history_id)
    return success_response(message="删除浏览历史成功")

@router.delete("/clear")
async def clear_history(
        user : User = Depends(get_current_user),
        db_session : AsyncSession = Depends(get_database_session)
):
    """清空历史记录"""
    count = await history.clear_history(db_session, user.id)
    return success_response(message=f"清空了{count}条浏览历史")
