from fastapi import FastAPI, APIRouter, HTTPException
from fastapi import Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_database_session
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(

        news_id :int = Query(..., alias= "newsId"),
        user : User = Depends(get_current_user) ,
        db_session : AsyncSession = Depends(get_database_session)
):
    """检查收藏是否被用户收藏"""
    is_favorited = await favorite.is_favorite(db_session, user.id, news_id)
    return success_response(message= "检查收藏成功", data= FavoriteCheckResponse(isFavorite=is_favorited))

@router.post("/add")
async def add_favorite(
        data: FavoriteAddRequest,
        user : User = Depends(get_current_user) ,
        db_session : AsyncSession = Depends(get_database_session)
):
    """添加收藏"""
    result = await favorite.add_favorite(db_session, user.id, data.news_id)
    return success_response(message= "添加收藏成功", data= result)

@router.delete("/remove")
async def remove_favorite(
        news_id :int = Query(..., alias= "newsId"),
        user : User = Depends(get_current_user) ,
        db_session : AsyncSession = Depends(get_database_session)
):
    """删除收藏"""
    result = await favorite.remove_favorite(db_session, user.id, news_id)
    if not result:
        raise HTTPException(status_code=404, detail="收藏不存在")

    return success_response(message= "删除收藏成功", data= result)

@router.get("/list")
async def get_favorite_list(
        page : int = Query(1, ge = 1),
        page_size : int = Query(10, ge=1, le = 100,alias="pageSize"),
        user : User = Depends(get_current_user) ,
        db_session : AsyncSession = Depends(get_database_session)
):
    """获取收藏列表"""
    total, favorite_list = await favorite.get_favorite_list(db_session, user.id, page, page_size)
    result_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news, favorite_time, favorite_id in favorite_list]
    has_more = total > page * page_size

    data = FavoriteListResponse(list=result_list, total=total, has_more=has_more)
    return success_response(message= "获取收藏列表成功", data= data)

@router.delete("/clear")
async def clear_favorite(
        user : User = Depends(get_current_user) ,
        db_session : AsyncSession = Depends(get_database_session)
):
    """清空收藏"""
    result = await favorite.clear_favorite(db_session, user.id)
    return success_response(message= f"清空了{result}条收藏")
