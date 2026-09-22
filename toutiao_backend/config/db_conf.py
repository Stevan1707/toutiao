# 配置异步引擎数据库
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# 导入数据库地址
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True, # 输出sql日志
    pool_size = 10,
    max_overflow = 20
)

# 将查询数据库功能封装到路由查询当中：
# 方法：查询 → 依赖注入：创建依赖项获取数据库会话， + Depends注入依赖项从而注入到路由处理函数
# 依赖项是多个端口都要用到的共同组件
# 从sqlalchemy.ext.asyncio中导入AsyncSession和async_sessionmaker来处理事务逻辑
# session会话：会话是操作数据库的工具，我们在会话内去操作数据库

AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,   #绑定数据库引擎
    class_ = AsyncSession ,  # 指定会话类
    expire_on_commit= False  # 提交会话不会过期，不会重新查询数据库
)

# 依赖项
async def get_database_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 如果失败则事务回滚
            raise
        finally:
            await session.close()   # 最后关闭会话

