import datetime
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_database_session
from models.users import User, UserToken
from schemas.users import UserRequest
from utils.encryption import get_password_hash


async def get_user_by_username( db_session: AsyncSession, username: str):
    """根据用户名查询用户"""
    stmt = select(User).where(User.username == username)
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    return user

async def create_user(db_session: AsyncSession, user: UserRequest):
    """创建用户，先将密码加密之后再创建用户"""
    # 1.将密码加密
    hashed_password = get_password_hash(user.password)
    # 2.创建用户

    new_user = User(username=user.username, password=hashed_password)
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user) # 刷新用户信息，确保返回的是最新的用户数据
    return new_user

async def create_token(db_session: AsyncSession, user: User):
    """使用uuid来创建token"""
    token = str(uuid.uuid4())

    # 将token导入到user_token表里面
    expires_at = datetime.datetime.now() + datetime.timedelta(days=7)  # 7天过期

    query = select(UserToken).where(UserToken.user_id == user.id)
    result = await db_session.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at  # 更新过期时间
    else:
        user_token = UserToken(user_id=user.id, token=token, expires_at=expires_at)
        db_session.add(user_token)
    await db_session.commit()
    await db_session.refresh(user_token)

    return token