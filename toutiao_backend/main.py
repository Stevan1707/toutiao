from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

# 通过全局配置cors来解决跨域问题
# allow_credentials=True 时不能使用 allow_origins=["*"]，需要用 allow_origin_regex 来匹配所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # 允许所有来源（支持 allow_credentials=True）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 将路由挂载
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
