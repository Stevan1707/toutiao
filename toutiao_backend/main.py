from fastapi import FastAPI
from routers import news
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 将路由挂载
app.include_router(news.router)