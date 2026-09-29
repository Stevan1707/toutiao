import datetime
import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_database_session
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import encryption
from utils.encryption import get_password_hash, verify_password


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

async def authenticate_user( user: UserRequest, db_session: AsyncSession):
    """验证用户登录信息"""
    user = await get_user_by_username(db_session, user.username)
    if not user:
        return None

    if not verify_password(user.password, user.password):
        return None

    return user

async def get_user_by_token(user_token: str, db_session: AsyncSession):
    """根据token查询用户"""
    query = select(UserToken).where(UserToken.token == user_token)
    result = await db_session.execute(query)
    token = result.scalar_one_or_none()
    if not token or token.expires_at < datetime.datetime.now():
        return None

    stmt = select(User).where(User.id == token.user_id)
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


# 更新用户信息: update更新 → 检查是否命中 → 获取更新后的用户返回
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    """更新用户信息"""
    # update(User).where(User.username == username).values(字段=值, 字段=值)
    # user_data 是一个Pydantic类型，得到字典 → ** 解包
    # 没有设置值的不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取一下更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user

# 修改密码: 验证旧密码 → 新密码加密 → 修改密码
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    """修改密码"""
    if not encryption.verify_password(old_password, user.password):
        return False

    hashed_new_pwd = encryption.get_password_hash(new_password)
    user.password = hashed_new_pwd
    # 更新: 由SQLAlchemy真正接管这个 User 对象，确保可以 commit
    # 规避 session 过期或关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True