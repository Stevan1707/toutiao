# 头条新闻 (Toutiao)

> 本项目为**黑马程序员**指导项目。

基于 FastAPI + Vue 3 构建的新闻资讯 App 全栈项目。后端提供新闻浏览、用户系统、收藏管理、浏览历史、缓存加速等 API；前端基于 Vue 3 + Vant 4 构建移动端界面。

---

## 项目概览

### 整体架构

```
toutiao/
├── toutiao_frontend/     # Vue3 前端（有少量修改）
└── toutiao_backend/      # FastAPI 后端
```

### 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| ORM | SQLAlchemy (异步) |
| 数据库 | MySQL |
| 缓存 | Redis |
| 认证 | JWT Token |
| 异步驱动 | aiomysql |

> 配套前端：Vue 3 + Vite + Vue Router + Pinia + Vant 4 + Axios + vue-i18n

### 项目结构

**后端** `toutiao_backend/`

```
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

**前端** `toutiao_frontend/`（简要）

```
├── src/
│   ├── components/       # TabBar、NewsItem 等公共组件
│   ├── views/            # Home、Category、NewsDetail、Login、My 等页面
│   ├── store/            # Pinia 状态管理（news、user、favorite、history）
│   ├── router/           # 路由配置
│   ├── config/           # API 地址 & 千问配置
│   └── i18n/             # 中英文国际化
├── vite.config.js
└── package.json
```

---

## 快速启动

### 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Redis 3.x+

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd toutiao
```

### 2. 启动后端

```bash
cd toutiao_backend

# 创建虚拟环境 & 安装依赖
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux

pip install fastapi uvicorn sqlalchemy aiomysql redis pydantic bcrypt

# 创建数据库
# mysql -u root -p -e "CREATE DATABASE news_app DEFAULT CHARSET utf8mb4;"

# 启动服务（默认 8000 端口）
uvicorn main:app --reload --port 8000
```

### 3. 启动前端

```bash
cd toutiao_frontend

# 安装依赖
npm install

# 启动开发服务器（默认 5173 端口）
npm run dev
```

### 4. 访问

- 前端页面：`http://localhost:5173`
- 后端接口文档：`http://localhost:8000/docs`

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

## 主要工作

- **项目初始化**：搭建 FastAPI 项目骨架，配置 CORS 跨域支持
- **新闻模块**：实现新闻分类列表、新闻列表分页查询、新闻详情（含浏览量统计与相关推荐）
- **用户模块**：实现注册/登录、JWT Token 认证、个人信息修改、密码修改，封装统一响应格式与全局异常处理
- **收藏模块**：实现收藏的增删查改与一键清空
- **浏览历史**：实现浏览记录的自动添加、分页查询、单条删除与一键清空
- **缓存加速**：引入 Redis，对新闻分类和列表做多级缓存，并集成通义千问 AI 聊天功能

---

## 技术亮点

- **异步全链路**：FastAPI + SQLAlchemy Async + aiomysql，充分利用异步 IO 提升并发性能
- **多级缓存策略**：Redis 缓存新闻分类（长周期）和新闻列表（短周期），大幅减少数据库压力
- **统一异常处理**：全局注册各类异常处理器，接口层无需重复 try-catch
- **JWT 认证**：Header Token + Depends 依赖注入方式保护接口
- **分层架构**：Router → CRUD → Model 清晰的三层架构，职责分离，易于维护