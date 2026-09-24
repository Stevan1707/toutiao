# schemas 目录下的文件就是拿来做类型校验的，有点类似DTO
from typing import Optional

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """
     ⽤户信息基础数据模型
     """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = {
        "from_attributes": True,  # 允许从ORM对象中取值
    }

class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias = "userInfo")

    model_config = {
        "from_attributes": True, # 允许从ORM对象中取值
        "populate_by_name": True  # 别名、字段名兼容
    }

