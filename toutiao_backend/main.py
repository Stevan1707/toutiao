from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 通过全局配置cors来解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 默认允许所有源，生产需要配置源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 将路由挂载
app.include_router(news.router)