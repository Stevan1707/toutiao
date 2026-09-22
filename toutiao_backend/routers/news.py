
from fastapi import APIRouter, Depends, Query, HTTPException
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

@router.get("/detail")
async def get_news_detail(
        news_id: int = Query(...,alias = "id"),
        db_session: AsyncSession = Depends(get_database_session)):
    """ 获取指定新闻详情 """
    news_detail = await news.get_news_detail(db_session, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 更新浏览量
    view_response = await news.update_news_views(db_session, news_id)
    # 检查是否更新成功
    if not view_response:
        raise HTTPException(status_code=404, detail="更新浏览量失败")

    related_news = await news.get_related_news(db_session, news_id, news_detail.category_id)

    news_title = news_detail.title
    news_content = news_detail.content
    news_image = news_detail.image
    news_author = news_detail.author
    news_publish_time = news_detail.publish_time
    news_category_id = news_detail.category_id
    news_views = news_detail.views

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_id,
            "title": news_title,
            "content": news_content,
            "image": news_image,
            "author": news_author,
            "publishTime": news_publish_time,
            "categoryId": news_category_id,
            "views": news_views,
            "relatedNews": related_news
        }
    }
