# schemas 目录下的文件就是拿来做类型校验的，有点类似DTO

from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str


