from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

# 通过全局配置cors来解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],   # allow_credentials=True 时不能使用通配符 *
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