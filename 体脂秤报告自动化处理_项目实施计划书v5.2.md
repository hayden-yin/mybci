# 体脂秤报告自动化处理_项目实施计划书

## 一、项目概述与目标
**版本**: v5.2 (2025-11-08 17:18:53)
**更新内容**: 
- 修正项目目录结构设计（配置文件归属优化）
- 明确各模块职责描述和启动脚本功能
- 添加mybci项目依赖包详细清单
- 完善paddleocr客户端调用模块设计
---
**版本**: v5.2 (2025-11-08 17:18:53)
**更新内容**: 
- 修正项目目录结构设计（配置文件归属优化）
- 明确各模块职责描述和启动脚本功能
- 添加mybci项目依赖包详细清单
- 完善paddleocr客户端调用模块设计
---
### 1. 项目背景
    a. 当前体脂秤检测报告格式多样，人工整理效率低、错误率高。
    b. 项目目标是利用 **PaddleOCR PP-StructureV3** 模型，实现体脂秤报告内容的自动结构化与关键信息提取。
    c. 同时，系统需与 **Label Studio** 标注平台进行对接，实现预标注与人工校正闭环。
### 2. 项目总体目标
    a. 实现自动化OCR结构化解析：自动识别报告图像中的表格、文字、字段区域。
    b. 构建mybci项目，实现任务调度与导出Excel功能。
    c. 建立Label Studio对接模块，实现预标注功能。
    d. 形成可复用的本地自动化系统，支持后续扩展与模型替换。
    e. 基于实际环境验证，建立完整的Windows 11 + Anaconda部署方案。
---
## 二、总体架构与模块设计
### 1. 系统架构概述
    a. 项目采用"四层分离"架构设计：
        * i. **项目1：paddleocr项目（OCR推理引擎）**
            - (1) 提供文字识别与结构化推理能力。
            - (2) 输出版面结构与字段内容。
            - (3) 支持PP-StructureV3最新功能。
            - (4) 提供HTTP REST API接口供其他模块调用。
            - (5) **run_paddleocr.py功能**：启动HTTP REST API服务(端口8080)
        * ii. **模块2：ML Backend接口服务**
            - (1) 作为Label Studio的机器学习后端，提供HTTP REST API接口。
            - (2) 接收Label Studio的推理请求，调用PaddleOCR进行OCR处理。
            - (3) 将OCR结果转换为Label Studio兼容的标注格式返回。
            - (4) 基于FastAPI框架，确保高性能与稳定性。
            - (5) **run_ml_backend.py功能**：启动ML Backend服务(端口8081)
        * iii. **项目3：mybci项目（智能体脂秤控制系统）**
            - (1) 利用Label Studio与ML Backend构建的HTTP REST API服务接口，完成一次性的版面标注。
            - (2) 利用PaddleOCR从照片提取文本，按配置结构化，然后输出成Excel。
            - (3) 提供Web前端界面，支持文件上传、任务监控、结果展示。
            - (4) 负责任务调度、批量处理与结果导出。
            - (5) 集成环境检查与诊断功能。
            - (6) **run_mybci.py功能**：启动mybci前端Web服务(端口8000)
        * iv. **模块4：MCP服务（独立模块）**
            - (1) 基于Model Communication Protocol的AI工具服务。
            - (2) 供AI模型或AI agent调用，不与Label Studio直接交互。
            - (3) 提供标准化的OCR工具接口（8082端口）。
            - (4) 独立运行，可被其他AI系统集成使用。
    b. 各模块间通过HTTP/REST接口通信，采用轻量化部署方式。
    c. 支持GPU/CPU双模式，确保在不同硬件环境下的兼容性。
### 2. 模块功能说明
    a. **paddleocr项目**
        * i. 封装PaddleOCR模型加载、识别与结构化输出。
        * ii. 输出格式为标准化JSON（包含文字、坐标、表格、层级信息）。
        * iii. 支持GPU推理与批量识别，内置环境检查工具。
        * iv. 集成 `check_paddleocr_env` 系列脚本进行环境验证。
        * v. **配置归属修正**：配置文件移至mybci项目，paddleocr项目专注于OCR引擎本身
    b. **ML Backend接口服务**
        * i. 提供Label Studio的机器学习后端接口（`/predict`、`/health`）。
        * ii. 接收Label Studio的OCR推理请求。
        * iii. 调用PaddleOCR服务进行图像识别。
        * iv. 将OCR结果转换为Label Studio兼容的标注格式返回。
    c. **MCP服务（独立模块）**
        * i. 基于Model Communication Protocol的AI工具服务。
        * ii. 供AI模型或AI agent调用，不与Label Studio直接交互。
        * iii. 提供标准化的OCR工具接口（8082端口）。
        * iv. 独立运行，可被其他AI系统集成使用。
    d. **mybci项目前端界面**
        * i. **文件上传界面**：支持批量上传体脂秤报告图片。
        * ii. **任务监控面板**：显示处理进度、GPU状态、任务队列。
        * iii. **结果展示页面**：预览OCR结果、结构化数据、Excel导出。
        * iv. **配置管理页面**：OCR参数调整、输出格式配置。
        * v. **系统诊断页面**：环境检查、日志查看、状态监控。
    e. **mybci项目后端服务**
        * i. 调度OCR任务，管理任务状态。
        * ii. 实现结果导出功能（Excel/CSV）。
        * iii. 记录日志与监控GPU状态，集成系统诊断功能。
        * iv. 提供Web API服务，支持前端交互。
        * v. **新增：paddleocr客户端调用模块** - 专门负责与paddleocr项目的API通信
### 3. 完整OCR处理流程设计
    a. **第一阶段：标注配置生成**
        * i. 使用Label Studio进行初始标注。
        * ii. 导出标注数据为JSON格式。
        * iii. 通过`convert_ls_to_config.py`脚本转换为OCR配置文件。
        * iv. **配置存储**：生成的配置文件存储在mybci项目的config/目录
    b. **第二阶段：OCR识别处理**
        * i. mybci项目加载标注配置文件（从mybci/config/目录）。
        * ii. 通过paddleocr客户端调用paddleocr项目进行结构化识别。
        * iii. 解析识别结果并按配置结构化数据。
    c. **第三阶段：结果输出**
        * i. 生成结构化数据表格。
        * ii. 按配置输出到Excel/CSV文件。
        * iii. 前端界面展示结果并提供下载。
---
## 三、项目目录结构设计
### 1. paddleocr项目目录结构
```
paddleocr/                             # 项目根目录 - 专用于OCR推理引擎
├── input/                            # 图片输入目录
│   └── *.jpg                         # 上传的待处理图片
├── output/                           # 结果输出目录
│   ├── *.csv / *.xlsx               # OCR处理结果
│   └── logs/                         # 日志文件
├── src/                              # 核心Python源代码目录
│   └── paddleocr/                    # 可安装的Python包
│       ├── __init__.py
│       ├── ocr_processing/           # OCR核心处理模块
│       │   ├── __init__.py
│       │   ├── ppstructure_engine.py # PaddleOCR封装
│       │   └── ocr_executor.py       # 核心OCR处理逻辑
│       ├── ml_backend/               # Label Studio机器学习后端
│       │   ├── __init__.py
│       │   ├── model.py              # ML模型入口
│       │   ├── server.py             # FastAPI服务器入口
│       │   └── ocr_adapter.py        # Label Studio适配器
│       ├── utils/                    # 工具函数模块
│       │   ├── __init__.py
│       │   ├── json_handler.py       # JSON文件安全读写
│       │   └── convert_ls_to_config.py # Label Studio配置转换脚本
│       └── core/                     # 应用全局配置
│           ├── __init__.py
│           └── settings.py           # Pydantic Settings配置
├── run_paddleocr.py                  # 启动脚本 - 启动HTTP REST API服务(端口8080)
├── run_ml_backend.py                 # 启动ML Backend服务(端口8081)
├── pyproject.toml                    # 项目配置
└── requirements.txt                  # 依赖文件
```
### 2. mybci项目目录结构
```
mybci/                                # 项目根目录 - 智能体脂秤控制系统
├── templates/                        # HTML模板文件(Jinja2)
│   ├── index.html                   # 主页 - 系统概览和快捷操作
│   ├── upload.html                  # 文件上传页 - 拖拽上传和参数配置
│   ├── monitor.html                 # 任务监控页 - 实时状态和性能监控
│   ├── results.html                 # 结果管理页 - 结果展示和导出
│   └── diagnostic.html              # 系统诊断页 - 环境检查和故障排除
├── static/                           # 静态资源文件
│   ├── css/
│   │   ├── style.css                # 主要样式文件
│   │   └── bootstrap.min.css        # Bootstrap 5样式
│   ├── js/
│   │   ├── app.js                   # 前端交互逻辑
│   │   ├── monitor.js               # 监控页面专用脚本
│   │   └── websocket.js             # WebSocket通信
│   ├── images/
│   │   ├── logo.png                 # 系统logo
│   │   └── icons/                   # 图标资源
│   └── fonts/                       # 字体文件
├── api/                             # API路由模块 - 存放所有API路由定义
│   ├── __init__.py
│   ├── routes.py                    # 主要API路由 - 页面路由和基础API配置
│   ├── upload.py                    # 文件上传相关API - /api/upload, /api/upload/status
│   ├── monitor.py                   # 任务监控API - /api/tasks, /api/tasks/{id}
│   ├── results.py                   # 结果管理API - /api/results, /api/results/{id}/download
│   └── diagnostic.py                # 系统诊断API - /api/diagnostic/gpu, /api/diagnostic/services
├── config/                          # mybci项目配置和业务配置文件
│   ├── __init__.py
│   ├── settings.py                  # mybci配置设置
│   ├── database.py                  # 数据库配置
│   ├── logging.py                   # 日志配置
│   ├── ocr_config.json              # BCI报告配置(由Label Studio转换生成)
│   ├── config_ocr_blood.json        # 血液报告配置(示例)
│   └── template_config.json         # 配置文件模板
├── models/                          # 数据模型
│   ├── __init__.py
│   ├── task.py                      # 任务模型
│   ├── result.py                    # 结果模型
│   └── config.py                    # 配置模型
├── services/                        # 业务逻辑服务
│   ├── __init__.py
│   ├── task_service.py              # 任务管理服务
│   ├── ocr_service.py               # OCR处理服务 - 调用paddleocr项目接口
│   ├── export_service.py            # 导出服务
│   ├── environment_service.py       # 环境检查服务
│   └── paddleocr_client.py          # paddleocr客户端调用模块
├── data/                            # 数据存储目录
│   ├── uploads/                     # 上传文件存储
│   ├── results/                     # 处理结果存储
│   └── exports/                     # Excel导出存储
├── run_mybci.py                     # 启动脚本 - 启动mybci前端Web服务(端口8000)
├── requirements.txt                 # 依赖文件(详见mybci_dependencies_v5.2.md)
├── mybci_dependencies_v5.2.md      # 依赖包详细清单
└── environment/                     # 环境检查工具(与paddleocr共享)
    ├── check_paddleocr_env_fixed.bat
    ├── install_missing_packages.bat
    └── validate_environment.py
```
---
## 四、mybci项目依赖包详细清单
### 1. 核心框架与Web服务
- **FastAPI** (0.121.0): Web API框架，提供高性能的RESTful接口
- **Uvicorn** (0.38.0): ASGI服务器，用于运行FastAPI应用
- **Jinja2** (3.0.3): 模板引擎，用于HTML页面渲染
### 2. 数据处理与文件操作
- **Pandas** (2.3.3): 数据分析和结构化处理
- **OpenPyXL** (3.1.5): Excel文件读写操作
- **Python-Multipart** (0.0.9): 文件上传支持
- **Aiofiles** (23.2.1): 异步文件操作
### 3. 数据库与异步任务
- **SQLAlchemy** (2.0.44): ORM数据库操作
- **Psycopg2-binary** (2.9.9): PostgreSQL数据库驱动
- **Redis** (5.2.0): 缓存和消息队列
- **Celery** (5.3.6): 分布式任务队列
### 4. HTTP客户端与通信
- **Requests** (2.31.0): HTTP客户端
- **Aiohttp** (3.9.5): 异步HTTP客户端
### 5. 配置与工具
- **Pydantic** (2.5.3): 数据验证和设置管理
- **Python-YAML** (6.0.1): YAML配置文件处理
- **Loguru** (0.7.2): 日志记录
### 6. 监控与健康检查
- **APScheduler** (3.10.4): 任务调度器
- **Psutil** (5.9.6): 系统和进程监控
### 7. 完整依赖清单
详见 `mybci_dependencies_v5.2.md` 文件，包含：
- 所有包的最新版本信息
- Python版本兼容性矩阵
- 详细的功能分类说明
- 安装指南和验证方法
---
## 五、开发与实施阶段划分
### 1. 阶段一：环境准备与模型验证
    a. 环境配置
        * i. 创建 `paddleocr`（用于OCR推理，基于实际验证经验）。
        * ii. 创建 `mybci`（用于mybci项目服务）。
        * iii. 安装依赖：paddlepaddle-gpu、paddleocr[all]、以及mybci项目所有依赖包(详见依赖清单)。
        * iv. 验证ML Backend必需包：fastapi、uvicorn、label-studio-ml、aiofiles。
    b. GPU验证
        * i. 使用环境检查脚本验证Paddle GPU支持：
            - (1) 运行 `check_paddleocr_env_fixed.bat` 进行全面环境检查。
            - (2) 验证 CUDA 版本兼容性（推荐 CUDA 11.8 或 12.x）。
        * ii. 确认GPU识别正常、设备可用。
    c. 模型测试
        * i. 加载PP-StructureV3模型（注意版本兼容性）。
        * ii. 使用样例报告图片进行结构化识别验证。
        * iii. 测试PP-StructureV3导入功能（避免实例化兼容性问题）。
### 2. 阶段二：paddleocr项目核心功能开发
    a. 开发 `src/paddleocr/ocr_processing/ppstructure_engine.py`
        * i. 封装OCR推理逻辑与PPStructure加载。
        * ii. 提供`analyze_document()`函数返回结构化结果。
        * iii. 集成环境检查与GPU状态监控。
    b. 开发 `src/paddleocr/ml_backend/ocr_adapter.py`
        * i. 提供REST接口供Label Studio调用。
        * ii. 定义`/predict`、`/health`接口，确保ML Backend兼容性。
    c. 开发 `src/paddleocr/utils/convert_ls_to_config.py`
        * i. 实现Label Studio JSON到OCR配置的转换。
        * ii. 支持多种标注格式的解析。
### 3. 阶段三：mybci项目开发
    a. 开发 `run_mybci.py`
        * i. 集成任务调度与结果导出逻辑。
        * ii. 实现日志与异常处理机制。
        * iii. 集成环境自动检查与诊断功能。
    b. 开发前端界面
        * i. 设计5个核心页面：主页、文件上传、任务监控、结果管理、系统诊断。
        * ii. 实现响应式设计与实时状态更新。
        * iii. 集成WebSocket接口支持。
    c. 实现API接口
        * i. RESTful API设计：/api/upload, /api/tasks, /api/results等。
        * ii. WebSocket接口：/ws/status, /ws/progress, /ws/logs。
    d. **新增：开发paddleocr客户端调用模块**
        * i. 开发`services/paddleocr_client.py`
        * ii. 实现与paddleocr项目的HTTP API通信
        * iii. 处理OCR请求和响应数据
        * iv. 集成配置管理和错误处理
### 4. 阶段四：Label Studio集成
    a. Label Studio容器部署
        * i. 运行命令：
            - (1) `docker run -it -p 8080:8080 heartexlabs/label-studio`
        * ii. 确认界面可访问。
    b. PaddleOCR ML Backend配置
        * i. 启动PaddleOCR HTTP服务（如http://localhost:8080）。
        * ii. 配置Label Studio中的ML Backend地址指向PaddleOCR服务。
        * iii. 设置模型路径和OCR参数配置。
        * iv. 测试API连接与模型加载状态。
    c. 完整流程测试
        * i. 标注配置生成 → OCR识别 → Excel输出。
        * ii. 验证整个工作流的完整性。
---
## 六、启动脚本功能说明
### 1. run_paddleocr.py
- **功能**: 启动HTTP REST API服务
- **端口**: 8080
- **职责**: 
  - 封装PaddleOCR模型加载和推理逻辑
  - 提供OCR识别API接口 (/ocr/analyze)
  - 处理图像输入和结构化输出
  - 集成环境检查和GPU状态监控
### 2. run_ml_backend.py
- **功能**: 启动ML Backend服务
- **端口**: 8081
- **职责**:
  - 作为Label Studio的机器学习后端
  - 提供 /predict 和 /health 接口
  - 调用paddleocr服务进行OCR处理
  - 转换OCR结果为Label Studio格式
### 3. run_mybci.py
- **功能**: 启动mybci前端Web服务
- **端口**: 8000
- **职责**:
  - 启动FastAPI主服务
  - 提供Web前端界面
  - 管理任务调度和结果导出
  - 集成环境检查功能
  - 调用paddleocr客户端模块
---
## 七、API路由模块设计
### 1. api/routes.py
- **主要职责**: 存放主要API路由配置和页面路由
- **功能**:
  - 页面路由: /, /upload, /monitor, /results, /diagnostic
  - 基础API配置
  - 中间件配置
  - 全局异常处理
### 2. api/upload.py
- **功能**: 文件上传相关API
- **接口**:
  - POST /api/upload - 上传文件
  - GET /api/upload/status/{task_id} - 获取上传状态
  - DELETE /api/upload/{file_id} - 删除文件
### 3. api/monitor.py
- **功能**: 任务监控API
- **接口**:
  - GET /api/tasks - 获取任务列表
  - GET /api/tasks/{task_id} - 获取任务详情
  - PUT /api/tasks/{task_id} - 更新任务状态
  - DELETE /api/tasks/{task_id} - 删除任务
### 4. api/results.py
- **功能**: 结果管理API
- **接口**:
  - GET /api/results - 获取结果列表
  - GET /api/results/{task_id} - 获取具体结果
  - GET /api/results/{task_id}/download - 下载Excel文件
  - POST /api/export - 批量导出
### 5. api/diagnostic.py
- **功能**: 系统诊断API
- **接口**:
  - GET /api/diagnostic/gpu - GPU状态
  - GET /api/diagnostic/services - 服务健康检查
  - GET /api/diagnostic/logs - 获取日志
  - POST /api/diagnose - 触发环境检查
---
## 八、配置归属优化
### 1. paddleocr项目配置职责
- **专注于OCR引擎本身**
- **不包含业务配置文件**
- **仅包含引擎运行时配置**（模型路径、推理参数等）
### 2. mybci项目配置职责
- **包含所有业务配置文件**:
  - ocr_config.json (BCI报告配置)
  - config_ocr_blood.json (血液报告配置)
  - template_config.json (配置模板)
- **mybci项目配置**:
  - settings.py (应用设置)
  - database.py (数据库配置)
  - logging.py (日志配置)
### 3. 配置流程优化
- Label Studio标注 → 导出JSON → convert_ls_to_config.py转换 → **存储到mybci/config/**
- mybci启动时加载配置 → 通过paddleocr_client调用paddleocr服务 → **使用配置进行OCR识别**
---
## 九、验收标准与指标体系
### 1. 功能性指标
    a. OCR结构化识别正确率 ≥ 95%。
    b. Label Studio预标注正确率 ≥ 90%。
    c. Excel导出字段完整率 ≥ 98%。
    d. 环境检查脚本显示所有必需包为[已安装]状态。
    e. **新增：paddleocr客户端调用成功率 ≥ 99%**
### 2. 性能指标
    a. 单图平均响应时延 < 2秒（RTX 2080环境）。
    b. 并发请求（10并发）稳定无异常。
    c. 系统长时间运行（≥72小时）无故障。
    d. 环境检查耗时 < 10秒。
    e. **新增：mybci前端响应时间 < 1秒**
### 3. 可用性指标
    a. 界面交互流程清晰，标注任务可追溯。
    b. 支持异常自动恢复与日志追踪。
    c. 环境检查脚本提供清晰的安装指导。
    d. **新增：配置管理功能完整，文件组织清晰**
---
## 十、风险分析与应对策略
### 1. 技术风险
    a. **GPU兼容性问题**
        * i. 应对策略：统一CUDA版本；提供CPU备用模式。
        * ii. 使用环境检查脚本提前识别兼容性问题。
    b. **模型版本更新导致接口变化**
        * i. 应对策略：固定依赖版本并测试更新兼容性。
        * ii. 特别关注PP-StructureV3的导入与实例化差异。
    c. **PaddleOCR输出结构变化**
        * i. 应对策略：定义中间转换层（paddleocr_client）。
        * ii. 建立版本兼容性测试流程。
    d. **新增：配置文件归属混乱风险**
        * i. 应对策略：明确配置职责分离，建立配置管理规范
        * ii. 通过自动化脚本验证配置文件位置
### 2. 系统风险
    a. Label Studio版本不兼容
        * i. 应对策略：锁定Docker镜像版本。
    b. Redis或数据库故障
        * i. 应对策略：增加自动重连与任务重试机制。
    c. **ML Backend包缺失风险**
        * i. 应对策略：建立环境检查机制，确保必需包完整性。
        * ii. 提供一键安装脚本 `install_missing_packages.bat`。
    d. **新增：mybci-paddleocr通信风险**
        * i. 应对策略：实现重试机制、超时处理、错误恢复
        * ii. 建立服务健康检查和自动重启机制
---
## 十一、部署方案与维护策略
### 1. 本地部署
    a. 操作系统：Windows 11 + WSL2（可选）。
    b. 启动命令：
        * i. `python run_paddleocr.py` (paddleocr项目)
        * ii. `python run_ml_backend.py` (ML Backend服务)
        * iii. `python run_mybci.py` (mybci项目)
    c. 环境验证：
        * i. 运行 `check_paddleocr_env_fixed.bat` 确认环境状态。
        * ii. 使用 `install_missing_packages.bat` 安装缺失依赖。
### 2. 服务化运行
    a. 可注册为Windows服务或通过Task Scheduler定时运行。
    b. 使用监控脚本 `monitor_system.py` 检测状态与重启异常。
    c. 集成环境检查作为启动前验证步骤。
### 3. 日志与监控
    a. 所有模块统一写入 `logs/` 目录。
    b. 每日滚动日志、异常自动标记。
    c. GPU监控脚本实时检测显存占用。
    d. 环境状态监控与自动诊断。
### 4. 依赖包管理
    a. mybci项目采用统一的依赖管理策略
    b. 详细的依赖清单文档 `mybci_dependencies_v5.2.md`
    c. 版本兼容性测试和自动验证机制
---
## 十二、成果交付与验收方式
### 1. 交付内容
    a. **paddleocr项目完整源码与配置文件**。
    b. **mybci项目完整源码与前端界面**。
    c. **mybci项目依赖包详细清单** (mybci_dependencies_v5.2.md)。
    d. 可执行脚本与启动说明文档。
    e. 测试样例与输出结果（Excel/JSON）。
    f. **环境检查与安装脚本套件**：
        - (1) `check_paddleocr_env_fixed.bat`（中文版环境检查）
        - (2) `install_missing_packages.bat`（一键安装脚本）
        - (3) 完整的环境配置与故障排除文档。
### 2. 验收流程
    a. paddleocr项目验证 → mybci项目验证 → Label Studio对接 → 性能测试 → 报告生成。
    b. 验收测试记录完整保存至`/outputs/validation_log/`。
    c. **完整OCR流程验收**：
        - (1) Label Studio标注 → 配置转换 → OCR识别 → Excel输出
        - (2) 验证整个工作流的端到端可用性
        - (3) 确认mybci前端界面功能完整
        - (4) **新增：验证配置管理功能和paddleocr客户端调用**
### 3. 验收判定标准
    a. 功能通过率 ≥ 95%。
    b. 无严重错误或系统崩溃。
    c. 报告输出格式与示例一致。
    d. **环境检查通过率 100%**：所有必需包检查显示[已安装]状态。
    e. **新增：配置归属验证通过**：配置文件正确存储在指定位置
    f. **新增：API模块功能验证**：所有API路由功能正常
---
## 十三、项目后续扩展方向
### 1. 模型扩展
    a. 增加 MinerU / Donut 模型接口，以支持多模态结构化任务。
    b. 增加自训练接口，允许本地微调与定制模板。
    c. 支持多版本PaddleOCR模型切换与A/B测试。
### 2. 功能扩展
    a. 增加智能字段匹配算法。
    b. 支持自动分章节、分页识别。
    c. 集成更多文档格式支持（PDF、扫描件等）。
    d. **扩展：支持多种配置模板和自动配置推荐**
### 3. 平台化方向
    a. 后续可封装为本地 KIE 平台模块。
    b. 结合文档分析、表格识别、知识抽取，实现统一报表结构化服务。
    c. 发展为可插拔的文档处理微服务架构。
    d. **发展方向：支持多租户配置管理和分布式部署**
---
## 十四、附录
### 1. 服务端口分配表
    a. PaddleOCR HTTP服务: 8080
    b. ML Backend接口服务: 8081
    c. MCP服务: 8082
    d. mybci项目服务: 8000
    e. Label Studio: 8080（独立容器）
    f. Redis: 6379
    g. PostgreSQL: 5432（可选）
### 2. 项目参与角色
    a. 项目负责人：总体协调与技术评审。
    b. 开发工程师：模块开发与接口实现。
    c. 测试工程师：性能与功能验证。
    d. 运维工程师：环境部署与监控。
### 3. 环境检查与诊断工具
    a. **Windows环境检查脚本系列**：
        - (1) `check_paddleocr_env_fixed.bat` - 中文版环境检查
        - (2) `install_missing_packages.bat` - 一键安装脚本
    b. **诊断功能**：
        - (1) GPU/CUDA兼容性检查
        - (2) PP-StructureV3导入验证
        - (3) ML Backend包完整性检查
        - (4) 依赖版本冲突检测
        - (5) **新增：配置文件位置和权限检查**
### 4. 版本信息
    a. 文档名称：体脂秤报告自动化处理_项目实施计划书
    b. 版本号：v5.2
    c. 最后更新时间：2025-11-08
    d. 更新内容：
        - (1) 修正项目目录结构设计（配置文件归属优化）
        - (2) 明确各模块职责描述和启动脚本功能
        - (3) 添加mybci项目依赖包详细清单
        - (4) 完善paddleocr客户端调用模块设计
        - (5) 优化API路由模块设计
        - (6) 增强配置管理和风险控制
    e. 格式标准：完全遵循用户提供的Markdown分级缩进规范（v1.0-20251107）