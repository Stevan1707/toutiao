# 整合根据token获取用户信息的代码块
from fastapi import HTTPException

from fastapi import Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_database_session
from crud.users import get_user_by_token


async def get_current_user(authentication: str = Header(..., alias="Authorization"),
                           db_session: AsyncSession = Depends(get_database_session)):
    """根据token查找用户信息，并且返回用户"""
    # 根据前端返回的Token格式预处理token
    # 支持 "Bearer <token>" 和纯 token 两种格式
    parts = authentication.split(" ")
    token = parts[1] if len(parts) > 1 else parts[0]

    user = await get_user_by_token(token, db_session)

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="token无效")

    return user