# mybci项目依赖包详细清单
## 📋 概述
本文档详细列出mybci项目所需的所有Python库和包，包括最新版本、Python兼容性、用途说明和功能分类。
---
## 🎯 核心框架与Web服务
### 1. FastAPI
- **最新版本**: 0.121.0 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10)
- **用途**: Web API框架，提供高性能的RESTful接口
- **功能**: 异步HTTP服务器、类型提示、OpenAPI文档生成
- **安装**: `pip install fastapi==0.121.0`
### 2. Uvicorn
- **最新版本**: 0.38.0 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: ASGI服务器，用于运行FastAPI应用
- **功能**: 高性能异步服务器，支持WebSocket
- **安装**: `pip install uvicorn[standard]==0.38.0`
### 3. Jinja2
- **最新版本**: 3.0.3 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: 模板引擎，用于HTML页面渲染
- **功能**: 变量替换、模板继承、过滤器
- **安装**: `pip install jinja2==3.0.3`
---
## 📊 数据处理与文件操作
### 4. Pandas
- **最新版本**: 2.3.3 (2025年)
- **Python兼容性**: 3.9+ (推荐3.10+)
- **用途**: 数据分析和结构化处理
- **功能**: DataFrame操作、数据清洗、统计分析
- **安装**: `pip install pandas==2.3.3`
### 5. OpenPyXL
- **最新版本**: 3.1.5 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: Excel文件读写操作
- **功能**: 读取/写入Excel文件、格式设置、图表操作
- **安装**: `pip install openpyxl==3.1.5`
### 6. Python-Multipart
- **最新版本**: 0.0.9 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: 文件上传支持
- **功能**: 多部分表单数据处理、文件流操作
- **安装**: `pip install python-multipart==0.0.9`
### 7. Aiofiles
- **最新版本**: 23.2.1 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 异步文件操作
- **功能**: 异步文件读写、文件流处理
- **安装**: `pip install aiofiles==23.2.1`
---
## 🗄️ 数据库与异步任务
### 8. SQLAlchemy
- **最新版本**: 2.0.44 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: ORM数据库操作
- **功能**: 对象关系映射、数据库连接池、事务管理
- **安装**: `pip install sqlalchemy==2.0.44`
### 9. Psycopg2-binary
- **最新版本**: 2.9.9 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: PostgreSQL数据库驱动
- **功能**: 数据库连接、SQL执行、事务控制
- **安装**: `pip install psycopg2-binary==2.9.9`
### 10. Redis
- **最新版本**: 5.2.0 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 缓存和消息队列
- **功能**: 键值存储、会话管理、任务队列
- **安装**: `pip install redis==5.2.0`
### 11. Celery
- **最新版本**: 5.3.6 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 分布式任务队列
- **功能**: 异步任务执行、任务调度、结果存储
- **安装**: `pip install celery==5.3.6`
---
## 🌐 HTTP客户端与通信
### 12. Requests
- **最新版本**: 2.31.0 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: HTTP客户端
- **功能**: HTTP请求、API调用、文件下载
- **安装**: `pip install requests==2.31.0`
### 13. Aiohttp
- **最新版本**: 3.9.5 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 异步HTTP客户端
- **功能**: 异步HTTP请求、连接池管理
- **安装**: `pip install aiohttp==3.9.5`
---
## 🔧 配置与工具
### 14. Pydantic
- **最新版本**: 2.5.3 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 数据验证和设置管理
- **功能**: 数据模型、类型验证、配置管理
- **安装**: `pip install pydantic==2.5.3`
### 15. Python-YAML
- **最新版本**: 6.0.1 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: YAML配置文件处理
- **功能**: 配置文件解析、参数管理
- **安装**: `pip install pyyaml==6.0.1`
### 16. Loguru
- **最新版本**: 0.7.2 (2025年)
- **Python兼容性**: 3.5+ (推荐3.10+)
- **用途**: 日志记录
- **功能**: 结构化日志、日志轮转、错误追踪
- **安装**: `pip install loguru==0.7.2`
---
## 🔐 认证与安全
### 17. Passlib
- **最新版本**: 1.7.4 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: 密码哈希
- **功能**: 密码加密、验证、bcrypt支持
- **安装**: `pip install passlib==1.7.4`
### 18. Python-Jose
- **最新版本**: 3.3.0 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: JWT令牌处理
- **功能**: JWT生成、验证、加密
- **安装**: `pip install python-jose[cryptography]==3.3.0`
---
## 📈 监控与健康检查
### 19. APScheduler
- **最新版本**: 3.10.4 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: 任务调度器
- **功能**: 定时任务、任务监控、健康检查
- **安装**: `pip install apscheduler==3.10.4`
### 20. Psutil
- **最新版本**: 5.9.6 (2025年)
- **Python兼容性**: 3.6+ (推荐3.10+)
- **用途**: 系统和进程监控
- **功能**: CPU/内存使用率、进程管理、网络监控
- **安装**: `pip install psutil==5.9.6`
---
## 🧪 开发与测试工具
### 21. Pytest
- **最新版本**: 7.4.4 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 测试框架
- **功能**: 单元测试、集成测试、测试报告
- **安装**: `pip install pytest==7.4.4`
### 22. Black
- **最新版本**: 23.12.1 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 代码格式化
- **功能**: 自动代码格式化、风格统一
- **安装**: `pip install black==23.12.1`
### 23. MyPy
- **最新版本**: 1.8.0 (2025年)
- **Python兼容性**: 3.7+ (推荐3.10+)
- **用途**: 类型检查
- **功能**: 静态类型检查、类型推断
- **安装**: `pip install mypy==1.8.0`
---
## 📦 完整的requirements.txt格式
```text
# Web框架
fastapi==0.121.0
uvicorn[standard]==0.38.0
jinja2==3.0.3
# 数据处理
pandas==2.3.3
openpyxl==3.1.5
python-multipart==0.0.9
aiofiles==23.2.1
# 数据库与任务队列
sqlalchemy==2.0.44
psycopg2-binary==2.9.9
redis==5.2.0
celery==5.3.6
# HTTP客户端
requests==2.31.0
aiohttp==3.9.5
# 配置与工具
pydantic==2.5.3
pyyaml==6.0.1
loguru==0.7.2
# 安全
passlib==1.7.4
python-jose[cryptography]==3.3.0
# 监控
apscheduler==3.10.4
psutil==5.9.6
# 开发工具
pytest==7.4.4
black==23.12.1
mypy==1.8.0
```
---
## 🖥️ 前端静态资源（CDN版本）
### 1. Bootstrap 5
- **版本**: 5.3.2 (2025年)
- **用途**: CSS框架
- **CDN**: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css`
### 2. Chart.js
- **版本**: 4.4.1 (2025年)
- **用途**: 图表库
- **CDN**: `https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.min.js`
### 3. Font Awesome
- **版本**: 6.5.0 (2025年)
- **用途**: 图标库
- **CDN**: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css`
### 4. jQuery
- **版本**: 3.7.1 (2025年)
- **用途**: JavaScript库
- **CDN**: `https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js`
---
## ⚡ 性能优化建议
### 1. 缓存策略
- **Redis**: 用于会话和结果缓存
- **内存缓存**: 使用functools.lru_cache装饰器
### 2. 异步优化
- **FastAPI**: 利用异步函数提升并发性能
- **Aiofiles**: 异步文件I/O操作
- **Aiohttp**: 异步HTTP客户端请求
### 3. 数据库优化
- **连接池**: 使用SQLAlchemy连接池
- **索引优化**: 为查询字段建立数据库索引
- **分页查询**: 避免大数据量一次性查询
---
## 🐍 Python版本兼容性矩阵
| 包名 | Python 3.7 | Python 3.8 | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|------|------------|------------|------------|-------------|-------------|-------------|
| FastAPI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Uvicorn | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Jinja2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pandas | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| SQLAlchemy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Celery | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Redis | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Aiohttp | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
---
## 📝 安装指南
### 1. 创建Conda环境
```bash
conda create -n mybci python=3.10 -y
conda activate mybci
```
### 2. 安装核心依赖
```bash
# 核心Web框架
pip install fastapi==0.121.0 uvicorn[standard]==0.38.0 jinja2==3.0.3
# 数据处理
pip install pandas==2.3.3 openpyxl==3.1.5 python-multipart==0.0.9 aiofiles==23.2.1
# 数据库
pip install sqlalchemy==2.0.44 psycopg2-binary==2.9.9 redis==5.2.0 celery==5.3.6
# HTTP客户端
pip install requests==2.31.0 aiohttp==3.9.5
# 工具
pip install pydantic==2.5.3 pyyaml==6.0.1 loguru==0.7.2
# 监控
pip install apscheduler==3.10.4 psutil==5.9.6
```
### 3. 验证安装
```python
# 验证关键包导入
import fastapi
import pandas
import sqlalchemy
import redis
import celery
print("所有依赖包安装成功！")
```
---
## 🔍 依赖包功能分类
### 🚀 核心服务类
- **FastAPI**: Web服务框架
- **Uvicorn**: ASGI服务器
- **Jinja2**: 模板引擎
### 📊 数据处理类
- **Pandas**: 数据分析
- **OpenPyXL**: Excel操作
- **PyYAML**: 配置文件
### 🗄️ 存储类
- **SQLAlchemy**: ORM框架
- **Psycopg2-binary**: PostgreSQL驱动
- **Redis**: 缓存/消息队列
### 🔄 任务队列类
- **Celery**: 分布式任务队列
- **APScheduler**: 任务调度器
### 🌐 通信类
- **Requests**: HTTP客户端
- **Aiohttp**: 异步HTTP客户端
- **Python-multipart**: 文件上传
### 🛡️ 安全类
- **Passlib**: 密码哈希
- **Python-jose**: JWT处理
### 📈 监控类
- **Psutil**: 系统监控
- **Loguru**: 日志记录
---
**文档版本**: v5.2  
**创建日期**: 2025-11-08  
**更新内容**: 详细列出所有依赖包版本、Python兼容性、功能分类