
from fastapi import APIRouter,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_database_session
from crud import news
# 创建API路由实例

# prefix：前缀  tags：到时候显示在接口文档里的分组
router = APIRouter(prefix="/api/news", tags= ["news"])

# 核心思路是先将路由模块化，再在main.py里面挂载

# 接口实现流程：1. 模块化路由，参照api接口文档
# 2. 定义模型类，根据数据库表格
# 3.在crud目录下创建方法来实现对数据库的操作
# 4.在路由处理里调用crud目录的封装好的方法
@router.get("/categories")
async def get_categories(db_session : AsyncSession = Depends(get_database_session),skip: int = 0, limit: int = 10):
    """ 获取所有分类列表 """
    news_categories = await news.get_categories(db_session, skip, limit)

    return {
        "code" : 200,
        "message" : "成功返回信息" ,
        "data" : news_categories
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(...,alias = "categoryId"),
        page: int = 1,
        page_size: int = Query(10,alias = "pageSize",lt=100),
        db_session: AsyncSession = Depends(get_database_session)):
    """ 获取指定分类下的新闻列表 """
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db_session, category_id, offset, page_size)

    total = await news.get_news_total(db_session, category_id)

    # 跳过的加上当前列表里的数量小于总量则has_more == true
    has_more = total > offset + len(news_list)

    return {
        "code": 200 ,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }
