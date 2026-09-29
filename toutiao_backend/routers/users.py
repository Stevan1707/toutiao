from docs.conf import author
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_database_session
from crud.users import get_user_by_username, create_user, create_token, authenticate_user
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"] )

@router.post("/register")
async def register(user_data : UserRequest, db_session : AsyncSession = Depends(get_database_session)):
    """用户注册"""
    # 注册逻辑： 1.验证用户是否存在 2.将用户信息存储到数据库 3.返回token 4.返回用户数据
    # 1.验证用户是否存在
    existing_user = await get_user_by_username(db_session, user_data.username)
    if existing_user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    # 2.将用户信息存储到数据库
    new_user = await create_user(db_session, user_data)

    # 3.返回token 4.返回用户数据
    token = await create_token(db_session, new_user)

    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data":{
    #         "token": token ,
    #         "user_name": user_data.username,
    #         "user_password" : user_data.password
    #     }
    # }

    response_data = UserAuthResponse(token=token, userInfo = UserInfoResponse.model_validate(new_user))
    return success_response( message="注册成功" , data=response_data)


@router.post("/login")
async def login(user_data : UserRequest, db_session : AsyncSession = Depends(get_database_session)):
    """用户登录"""
    # 登录逻辑： 1.验证用户是否存在 2.验证密码是否正确 3.返回token 4.返回用户数据
    user = await get_user_by_username(db_session, user_data.username)
    if not user:
        return None
    if not authenticate_user(user,db_session):
        return None
    token = await create_token(db_session, user)

    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response( message="登录成功" , data=response_data)

@router.get("/info")
async def get_user_info(user = Depends(get_current_user)):
    """获取用户信息"""
    return_data = UserInfoResponse.model_validate(user)
    return success_response( message="获取用户信息成功" , data=return_data)
