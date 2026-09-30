from fastapi import FastAPI, APIRouter
from fastapi import Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_database_session
from models.users import User
from schemas.favorite import FavoriteCheckResponse
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
