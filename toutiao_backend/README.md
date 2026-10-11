# 头条新闻后端服务 (Toutiao Backend)

基于 **FastAPI** 构建的新闻资讯类 App 后端服务，提供新闻浏览、用户系统、收藏管理、浏览历史、缓存加速等功能。

---

## 项目概览

### 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| ORM | SQLAlchemy (异步) |
| 数据库 | MySQL |
| 缓存 | Redis |
| 认证 | JWT Token |
| 异步驱动 | aiomysql |

### 项目结构

```
toutiao_backend/
├── main.py                    # 应用入口，路由挂载
├── config/
│   ├── db_conf.py             # MySQL 数据库配置
│   └── cache_conf.py          # Redis 缓存配置
├── models/                    # SQLAlchemy 数据模型
│   ├── news.py                # 新闻、分类模型
│   ├── users.py               # 用户模型
│   ├── favorite.py            # 收藏模型
│   └── history.py             # 浏览历史模型
├── routers/                   # API 路由层
│   ├── news.py                # 新闻相关接口
│   ├── users.py               # 用户相关接口
│   ├── favorite.py            # 收藏相关接口
│   └── history.py             # 浏览历史接口
├── crud/                      # 数据库操作层
│   ├── news.py                # 新闻 CRUD
│   ├── users.py               # 用户 CRUD
│   ├── favorite.py            # 收藏 CRUD
│   └── history.py             # 浏览历史 CRUD
├── schemas/                   # Pydantic 数据校验
│   ├── base.py                # 基础 Schema
│   ├── users.py               # 用户 Schema
│   ├── favorite.py            # 收藏 Schema
│   └── history.py             # 浏览历史 Schema
├── cache/                     # 缓存层
│   └── news_cache.py          # 新闻分类/列表缓存
└── utils/                     # 工具模块
    ├── auth.py                # JWT 认证依赖
    ├── response.py            # 统一响应格式
    ├── encryption.py          # 密码加密
    ├── exception.py           # 异常处理函数
    └── exception_handlers.py  # 全局异常注册
```

---

## 快速启动

### 环境要求

- Python 3.11+
- MySQL 8.0+
- Redis 3.x+

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd toutiao_backend
```

### 2. 创建虚拟环境 & 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux

pip install fastapi uvicorn sqlalchemy aiomysql redis pydantic bcrypt
```

### 3. 配置数据库

确保 MySQL 已启动，创建数据库：

```sql
CREATE DATABASE news_app DEFAULT CHARSET utf8mb4;
```

数据库连接配置在 [config/db_conf.py](file:///D:/Code/toutiao/toutiao_backend/config/db_conf.py#L6)，按需修改：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://用户名:密码@localhost:3306/news_app?charset=utf8"
```

### 4. 配置 Redis

确保 Redis 服务已启动，默认连接 `localhost:6379`，可在 [config/cache_conf.py](file:///D:/Code/toutiao/toutiao_backend/config/cache_conf.py) 中修改。

### 5. 启动服务

```bash
uvicorn main:app --reload --port 8000
```

服务默认运行在 `http://127.0.0.1:8000`。

### 6. 访问接口文档

- Swagger UI：`http://127.0.0.1:8000/docs`
- ReDoc：`http://127.0.0.1:8000/redoc`

---

## API 接口一览

| 模块 | 接口 | 说明 |
|------|------|------|
| **News** | `GET /api/news/categories` | 获取新闻分类列表 |
| | `GET /api/news/list` | 获取指定分类新闻列表（分页） |
| | `GET /api/news/detail` | 获取新闻详情（含相关推荐） |
| **User** | `POST /api/user/register` | 用户注册 |
| | `POST /api/user/login` | 用户登录 |
| | `GET /api/user/info` | 获取当前用户信息 |
| | `PUT /api/user/update` | 更新个人信息 |
| | `PUT /api/user/password` | 修改密码 |
| **Favorite** | `GET /api/favorite/check` | 检查新闻是否已收藏 |
| | `POST /api/favorite/add` | 添加收藏 |
| | `DELETE /api/favorite/remove` | 删除收藏 |
| | `GET /api/favorite/list` | 获取收藏列表（分页） |
| | `DELETE /api/favorite/clear` | 清空所有收藏 |
| **History** | `POST /api/history/add` | 添加浏览记录 |
| | `GET /api/history/list` | 获取浏览历史列表（分页） |
| | `DELETE /api/history/delete/{id}` | 删除单条浏览记录 |
| | `DELETE /api/history/clear` | 清空所有浏览记录 |

---

## 提交记录 & 功能清单

以下是本项目从零到一的完整开发历程：

### 🎬 项目初始

| 提交 | 说明 |
|------|------|
| `529ac67` | **first commit** — 项目初始化 |

### 🌐 基础设施

| 提交 | 说明 |
|------|------|
| `1547791` | **跨域 CORS 配置** — 解决前后端分离的跨域问题，支持 `allow_credentials=True` |
| `c83dfd1` | **全局异常处理** — 封装 HTTPException、IntegrityError、SQLAlchemyError 等异常的统一处理逻辑 |

### 📰 新闻模块

| 提交 | 说明 |
|------|------|
| `fdc74e2` | **新闻列表接口** — 支持按分类分页查询新闻列表，返回 `hasMore` 分页状态 |
| `193f6b0` | **新闻详情接口** — 返回新闻完整内容，自动更新浏览量，附带相关新闻推荐 |

### 👤 用户模块

| 提交 | 说明 |
|------|------|
| `574bdb3` | **用户注册接口** — 支持用户名/密码注册，返回 JWT Token |
| `526a7cb` | **统一响应格式** — 封装 `success_response` 统一 API 返回结构 |
| `f8cedf6` | **用户登录接口** — 密码验证 + Token 签发 |
| `6e784ad` | **用户信息验证** — 根据 Token 获取当前用户信息（`GET /info`） |
| `4db979e` | **更新个人信息** — 支持修改用户昵称等个人资料 |
| `d5e1a67` | **修改密码** — 验证旧密码后更新为新密码 |

### ⭐ 收藏模块

| 提交 | 说明 |
|------|------|
| `69ecc76` | **检查收藏状态** — 判断某条新闻是否已被当前用户收藏 |
| `7b685e1` | **添加收藏** — 将新闻加入用户收藏列表 |
| `9f6ae7c` | **删除收藏** — 从收藏列表中移除指定新闻 |
| `84af160` | **获取收藏列表** — 分页查询用户收藏，关联新闻详情 |
| `717a5bc` | **清空收藏列表** — 一键清空所有收藏记录 |

### 📝 浏览历史模块

| 提交 | 说明 |
|------|------|
| `786e0aa` | **添加浏览记录** — 用户查看新闻时自动记录浏览历史 |
| `48784e7` | **获取浏览历史列表** — 分页查询浏览历史，关联新闻信息 |
| `9c4e6f3` | **获取浏览记录列表**（补充优化） |
| `ba6d371` | **清空所有浏览记录** — 支持一键清除 |

### ⚡ 缓存加速

| 提交 | 说明 |
|------|------|
| `30ba337` | **Redis 缓存基础组件** — 封装 `get_cache` / `set_cache`，支持字符串和 JSON 格式 |
| `0a993da` | **新闻分类缓存** — 分类数据（稳定性高）缓存 2 小时 |
| `2b406f1` | **新闻列表缓存** — 按分类+分页维度缓存新闻列表数据 |
| `83a37fd` | **千问模型聊天功能** — 调用通义千问 AI 模型的聊天对话能力 |

---

## 技术亮点

- **异步全链路**：FastAPI + SQLAlchemy Async + aiomysql，充分利用异步 IO 提升并发性能
- **多级缓存策略**：Redis 缓存新闻分类（长周期）和新闻列表（短周期），大幅减少数据库压力
- **统一异常处理**：全局注册各类异常处理器，接口层无需重复 try-catch
- **JWT 认证**：Header 中携带 Token，通过 `Depends(get_current_user)` 依赖注入方式保护接口
- **分层架构**：Router → CRUD → Model 清晰的三层架构，职责分离，易于维护