# 体脂秤报告自动化处理_项目代码编写计划

## 一、项目总体说明
### 1. 项目目标与背景
    a. 本项目旨在实现"体脂秤报告自动化结构化处理系统"的开发与落地。
    b. 核心目标是通过集成 **PaddleOCR PP-StructureV3** 模型，实现体脂秤报告的结构化解析与关键数据提取。
    c. 系统最终将与 **Label Studio** 对接，实现自动预标注功能。
    d. 部署环境以 **Windows 11 + RTX 2080（8GB）** 为主要开发与测试平台。
    e. 基于实际环境验证经验，建立完整的Windows环境部署方案。
### 2. 项目总体架构
    a. 系统采用"四模块分离架构"：
        * i. **项目1：paddleocr项目（OCR推理引擎）**
            - (1) 封装 PP-StructureV3 的推理能力，支持文档结构化识别。
            - (2) 负责调用 OCR 模型并输出版面结构结果(JSON)。
            - (3) 集成环境检查与GPU状态监控功能。
            - (4) 提供HTTP REST API接口供其他模块调用。
            - (5) **run_paddleocr.py功能**：启动HTTP REST API服务(端口8080)
        * ii. **模块2：ML Backend接口服务 (ml_backend_server.py)**
            - (1) 作为Label Studio的机器学习后端，提供HTTP REST API接口。
            - (2) 接收Label Studio的推理请求，调用PaddleOCR进行OCR处理。
            - (3) 将OCR结果转换为Label Studio兼容的标注格式返回。
            - (4) 基于FastAPI框架，确保高性能与稳定性。
            - (5) **run_ml_backend.py功能**：启动ML Backend服务(端口8081)
        * iii. **项目3：mybci项目 (run_mybci.py)**
            - (1) 利用Label Studio与ML Backend构建的HTTP REST API服务接口，完成一次性的版面标注。
            - (2) 利用PaddleOCR从照片提取文本，按配置结构化，然后输出成Excel。
            - (3) 提供Web前端界面，支持文件上传、任务监控、结果展示。
            - (4) 负责流程编排、任务调度及结果存储。
            - (5) 提供批量任务处理与导出接口（CSV/Excel）。
            - (6) 集成环境诊断与监控机制。
            - (7) **run_mybci.py功能**：启动mybci前端Web服务(端口8000)
        * iv. **模块4：MCP服务 (mcp_service.py) - 独立模块**
            - (1) 基于Model Communication Protocol的AI工具服务。
            - (2) 供AI模型或AI agent调用，不与Label Studio直接交互。
            - (3) 提供标准化的OCR工具接口。
            - (4) 独立运行，可被其他AI系统集成使用。
    b. 整体结构遵循高内聚、低耦合原则，便于扩展与后续部署容器化。
    c. **新增：环境检查与诊断模块**
        - (1) 环境检查脚本套件
        - (2) 一键安装工具
        - (3) 故障诊断与自动修复机制
### 3. 完整OCR处理流程设计
    a. **第一阶段：标注配置生成**
        * i. 使用Label Studio进行初始标注。
        * ii. 导出标注数据为JSON格式（Is_export.json）。
        * iii. 通过`convert_ls_to_config.py`脚本转换为OCR配置文件（config_ocr_bci.json）。
        * iv. **配置存储**：生成的配置文件存储在mybci项目的config/目录
    b. **第二阶段：OCR识别处理**
        * i. mybci项目启动时加载指定的标注配置文件（从mybci/config/目录）。
        * ii. mybci项目接收用户上传的图片文件。
        * iii. mybci项目通过paddleocr客户端调用paddleocr项目进行结构化识别。
        * iv. 解析识别结果并按配置文件定义的字段结构化数据。
    c. **第三阶段：结果输出**
        * i. mybci项目生成结构化数据表格。
        * ii. 按配置输出到Excel/CSV文件（如bci_report_2025-11-08.xlsx）。
        * iii. 前端界面展示结果并提供下载链接。
---
## 二、开发环境规划
### 1. 硬件与系统要求
    a. 主机环境：Windows 11 专业版
    b. GPU：NVIDIA RTX 2080 (8GB VRAM)
    c. 内存：≥16GB
    d. 存储空间：≥100GB
    e. **新增要求**：
        - (1) 确保NVIDIA驱动为最新版本
        - (2) 启用WSL2支持（可选，便于Docker部署）
### 2. 软件依赖与版本（基于实际验证）
    a. Anaconda 3
    b. Python 3.10 (主控环境)
    c. **PaddlePaddle GPU 版本**：
        - (1) CUDA 11.8: paddlepaddle-gpu==2.6.2.post118
        - (2) CUDA 12.x: paddlepaddle-gpu==3.2.1
    d. PaddleOCR 最新稳定版 (paddleocr[all])
    e. **ML Backend必需包**（新增，基于实际验证）：
        - (1) fastapi: Web API框架
        - (2) uvicorn: ASGI服务器
        - (3) label-studio-ml: Label Studio机器学习后端
        - (4) aiofiles: 异步文件操作
    f. **核心依赖包**（基于实际验证）：
        - (1) opencv-python-headless: 图像处理
        - (2) progressbar2: 进度条
        - (3) attrdict: 属性字典
        - (4) rapidfuzz: 字符串匹配
    g. **数据处理包**：
        - (1) pandas, numpy, pyyaml, shapely, openpyxl
    h. **服务组件**：
        - (1) Redis（用于异步队列）
        - (2) PostgreSQL（用于标注任务存储）
        - (3) Label Studio (Docker 部署)
### 3. 环境划分方案
    a. **环境1：paddleocr**
        * i. 用途：专用于 OCR 模型推理与结构化任务。
        * ii. 包含依赖：
            - (1) paddlepaddle-gpu (匹配CUDA版本)
            - (2) paddleocr[all] (包含PP-StructureV3)
            - (3) opencv-python-headless
            - (4) fastapi, uvicorn, aiofiles
            - (5) 其他核心依赖包
    b. **环境2：mybci**
        * i. 用途：实现智能体脂秤控制系统功能：
            - (1) 利用Label Studio与ML Backend构建的HTTP REST API服务接口，完成一次性的版面标注。
            - (2) 利用PaddleOCR从照片提取文本，按配置结构化，然后输出成Excel。
            - (3) 提供Web前端界面，支持文件上传、任务监控、结果展示。
        * ii. 包含依赖：详见 mybci_dependencies_v5.2.md 文档
---
## 三、项目目录结构设计
### 1. paddleocr项目完整目录结构
```
paddleocr/                             # 项目根目录
├── input/                            # 扁平化的图片上传目录
│   ├── *.jpg
│   ├── *.png
│   └── *.pdf
├── output/                           # 扁平化的结果输出目录
│   ├── *.csv
│   ├── *.xlsx
│   └── logs/
├── src/                              # 核心Python源代码目录
│   └── paddleocr/                    # 可安装的Python包
│       ├── __init__.py
│       ├── ocr_processing/           # OCR核心处理模块
│       │   ├── __init__.py
│       │   ├── ppstructure_engine.py # 底层PaddleOCR封装
│       │   └── ocr_executor.py       # 核心逻辑(被Web和ML共同调用)
│       ├── ml_backend/               # Label Studio机器学习后端
│       │   ├── __init__.py
│       │   ├── model.py              # ML模型入口
│       │   ├── server.py             # FastAPI服务器入口
│       │   └── ocr_adapter.py        # 调用ocr_executor并转换格式
│       ├── utils/                    # 工具函数模块
│       │   ├── __init__.py
│       │   ├── json_handler.py       # JSON文件安全读写
│       │   ├── csv_handler.py        # CSV/Excel输出处理
│       │   └── convert_ls_to_config.py # Label Studio配置转换脚本
│       └── core/                     # 应用全局配置
│           ├── __init__.py
│           └── settings.py           # Pydantic Settings配置
├── run_paddleocr.py                  # PaddleOCR服务启动脚本
├── run_ml_backend.py                 # ML Backend服务启动脚本
├── pyproject.toml                    # 项目配置文件(pip install -e .)
├── requirements.txt                  # 依赖文件
└── environment/                      # 环境检查与诊断工具
    ├── check_paddleocr_env_fixed.bat # 中文版环境检查
    ├── check_paddleocr_env_en_fixed.bat # 英文版环境检查
    ├── install_missing_packages.bat  # 一键安装脚本
    └── validate_environment.py       # Python环境验证脚本
```
### 2. mybci项目完整目录结构
```
mybci/                                # 项目根目录
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
│   ├── upload.py                    # 文件上传相关API
│   ├── monitor.py                   # 任务监控API
│   ├── results.py                   # 结果管理API
│   └── diagnostic.py                # 系统诊断API
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
│   ├── ocr_service.py               # OCR处理服务
│   ├── export_service.py            # 导出服务
│   ├── environment_service.py       # 环境检查服务
│   └── paddleocr_client.py          # paddleocr客户端调用模块
├── data/                            # 数据存储目录
│   ├── uploads/                     # 上传文件存储
│   ├── results/                     # 处理结果存储
│   └── exports/                     # Excel导出存储
├── run_mybci.py                     # mybci项目启动脚本
├── requirements.txt                 # 依赖文件(详见mybci_dependencies_v5.2.md)
├── mybci_dependencies_v5.2.md      # 依赖包详细清单
└── environment/                     # 环境检查工具(与paddleocr共享)
    ├── check_paddleocr_env_fixed.bat
    ├── install_missing_packages.bat
    └── validate_environment.py
```
---
## 四、PaddleOCR 项目实现要点
### 1. 模型加载与配置（基于实际验证经验）
    a. 使用 `PaddleOCR` 官方 API 进行模型加载：
        * i. 调用 `from paddleocr import PPStructureV3` （注意：PP-StructureV3是导入方式，非独立包）。
        * ii. 设置参数 `show_log=False, layout=True`。
        * iii. 模型路径可配置化（通过 config/config.yaml）。
    b. **重要注意事项**（基于实际测试）：
        * i. PP-StructureV3导入成功但实例化可能存在兼容性问题。
        * ii. 建议在检查脚本中只测试导入，不进行实例化验证。
        * iii. 注意paddlepaddle与paddlex的版本兼容性。
### 2. 核心功能函数定义
    a. **ocr_executor.py 核心函数**：
        * i. `load_ppstructure_model()` - 模型加载
        * ii. `analyze_document(image_path: str, config_name: str) -> dict` - 文档分析
        * iii. `load_config(config_name: str) -> dict` - 加载配置文件
        * iv. `export_to_excel(json_data, output_path)` - Excel导出
        * v. **新增：`check_environment_status()` - 环境状态检查**
    b. **辅助函数**：
        * i. `check_gpu_status()` - GPU状态检查
        * ii. `init_logger()` - 日志初始化
        * iii. **新增：`validate_dependencies() - 依赖包验证**
        * iv. **新增：`test_ppstructure_import() - PP-StructureV3导入测试**
### 3. 配置转换脚本设计 (convert_ls_to_config.py)
    a. **输入格式**：Label Studio导出的JSON数据
    b. **输出格式**：OCR配置文件（config_ocr_bci.json）
    c. **转换逻辑**：
        * i. 解析Label Studio标注结果
        * ii. 提取字段名称、位置信息、类型定义
        * iii. 生成结构化的OCR配置格式
        * iv. 支持多种字段类型：文本、数字、表格、日期等
    d. **存储位置**：生成的配置文件存储到 mybci/config/ 目录
### 4. 性能优化要点
    a. GPU 优先，必要时可切换 CPU 模式。
    b. 对批量任务采用多进程/异步任务（FastAPI BackgroundTasks 或 Celery）。
    c. 支持结果缓存（Redis），避免重复推理。
    d. **新增优化点**：
        - (1) 环境检查结果缓存
        - (2) 依赖包状态批量检查
        - (3) 智能环境问题诊断与建议
---
## 五、Label Studio 对接设计
### 1. 对接目标
    a. 使 Label Studio 可调用本地 PaddleOCR 推理服务，实现自动预标注。
    b. 支持 Label Studio 的 ML Backend 模式，通过 REST API 对接。
    c. **增强目标**：提供完整的环境兼容性保障。
### 2. 接口交互说明
    a. Label Studio 调用 `/predict` 接口时，本地服务接收请求 → 调用 PaddleOCR → 返回结构化预测结果。
    b. 核心字段映射：
        * i. OCR 文本结果 → Label Studio "Text" 标签。
        * ii. 坐标框信息 → `result` 字段中的 bbox。
        * iii. 文档结构（表格/段落） → 自定义标签类型。
    c. **新增交互**：
        - (1) `/env/validate` - 环境状态验证接口
        - (2) `/health` - 增强健康检查（包含环境状态）
### 3. Label Studio 侧配置
    a. 进入 ML Backend 配置：
        * i. 启用本地模式。
        * ii. `MODEL_DIR` 指向 PaddleOCR HTTP 服务地址（如 http://localhost:8080）。
        * iii. 启动命令：
            - (1) `label-studio-ml start ./ml_backend --port 8081`
    b. **配置增强**：
        - (1) 验证ML Backend必需包安装状态
        - (2) 检查服务健康状态（环境检查通过后启动）
        - (3) 提供配置诊断与自动修复建议
---
## 六、mybci项目依赖包详细清单
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
### 7. 完整的依赖清单
**详细版本信息、安装指南、Python兼容性矩阵请参考：** `mybci_dependencies_v5.2.md` 文档
---
## 七、mybci项目前端界面设计
### 1. 前端架构概述
    a. **技术栈**：
        - (1) 后端：FastAPI + Jinja2模板引擎
        - (2) 前端：HTML5 + CSS3 + JavaScript (原生)
        - (3) UI框架：Bootstrap 5 (响应式设计)
        - (4) 图标：Font Awesome
    b. **项目结构**：
        - (1) `templates/` - HTML模板文件
        - (2) `static/css/` - 样式文件
        - (3) `static/js/` - JavaScript脚本
        - (4) `static/images/` - 图片资源
    c. **设计原则**：
        - (1) 简洁易用的用户界面
        - (2) 响应式设计，支持多设备访问
        - (3) 实时状态反馈与进度显示
        - (4) 一键操作，减少学习成本
### 2. 页面设计详解
    a. **主页 (index.html)**
        * i. **顶部导航栏**：
            - (1) Logo：mybci智能体脂秤控制系统
            - (2) 导航菜单：文件上传、任务监控、结果管理、系统诊断
            - (3) 状态指示器：在线服务状态、GPU使用率
        * ii. **欢迎区域**：
            - (1) 项目介绍与功能说明
            - (2) 快速开始指南
            - (3) 系统状态概览（服务运行状态、环境检查结果）
        * iii. **快捷操作区域**：
            - (1) 一键上传文件按钮
            - (2) 批量处理按钮
            - (3) 导出结果按钮
    
    b. **文件上传页面 (upload.html)**
        * i. **拖拽上传区域**：
            - (1) 支持多文件同时上传（PNG、JPG、PDF）
            - (2) 拖拽或点击选择文件
            - (3) 文件预览缩略图
            - (4) 文件大小与格式验证
        * ii. **上传设置**：
            - (1) OCR参数配置（语言、模型精度）
            - (2) 输出格式选择（Excel、CSV、JSON）
            - (3) 结构化模板选择（如BCI报告、血压报告等）
        * iii. **上传进度**：
            - (1) 实时上传进度条
            - (2) 队列状态显示
            - (3) 错误处理与重试机制
    c. **任务监控页面 (monitor.html)**
        * i. **任务队列面板**：
            - (1) 实时任务列表（待处理、处理中、已完成、失败）
            - (2) 任务详情（文件名、开始时间、预计完成时间）
            - (3) 任务操作（暂停、取消、重新开始）
        * ii. **系统性能监控**：
            - (1) GPU使用率图表（CPU、内存、显存）
            - (2) 服务响应时间统计
            - (3) 处理速度指标（图片/分钟）
        * iii. **日志查看器**：
            - (1) 实时日志流
            - (2) 日志级别过滤（INFO、WARNING、ERROR）
            - (3) 日志搜索与下载功能
    d. **结果管理页面 (results.html)**
        * i. **结果列表**：
            - (1) 任务结果表格（文件名称、处理时间、结果状态）
            - (2) 结果预览功能
            - (3) 批量操作（下载、删除、重新处理）
        * ii. **结果详情**：
            - (1) OCR结果展示（原图 + 识别结果）
            - (2) 结构化数据表格
            - (3) 识别置信度显示
            - (4) 错误标记与人工校正
        * iii. **导出功能**：
            - (1) Excel格式导出（支持自定义模板）
            - (2) CSV格式导出
            - (3) 批量导出与打包下载
    e. **系统诊断页面 (diagnostic.html)**
        * i. **环境检查**：
            - (1) Python环境与依赖包版本
            - (2) GPU驱动与CUDA版本
            - (3) PaddleOCR模型下载状态
            - (4) 网络连接与端口状态
        * ii. **服务状态**：
            - (1) 各服务模块运行状态
            - (2) API接口健康检查
            - (3) 数据库连接状态（Redis、PostgreSQL）
        * iii. **性能统计**：
            - (1) 系统资源使用历史
            - (2) 处理任务成功率统计
            - (3) 错误日志分析
### 3. 前端交互设计
    a. **实时更新机制**：
        - (1) WebSocket连接实现实时状态更新
        - (2) AJAX异步请求处理用户操作
        - (3) 前端状态管理（原生JavaScript状态管理）
    b. **用户体验优化**：
        - (1) 加载动画与进度提示
        - (2) 操作确认与撤销机制
        - (3) 错误提示与帮助信息
        - (4) 键盘快捷键支持
    c. **响应式设计**：
        - (1) 移动端适配（iPhone、Android）
        - (2) 平板端优化（iPad、Android Tablet）
        - (3) 桌面端完整功能
    d. **无障碍设计**：
        - (1) 键盘导航支持
        - (2) 屏幕阅读器兼容
        - (3) 高对比度模式
        - (4) 字体大小调节
---
## 八、mybci项目API路由模块设计
### 1. API模块整体架构
    a. **模块化设计原则**：
        - 每个API功能模块独立文件
        - 统一错误处理和响应格式
        - 清晰的职责分离
    b. **技术实现**：
        - FastAPI 路由装饰器
        - Pydantic 数据模型验证
        - 异步处理支持
### 2. api/routes.py - 主要API路由
    a. **职责描述**：存放主要API路由配置和页面路由
    b. **功能内容**：
        * i. **页面路由**：
            - GET / - 主页 (index.html)
            - GET /upload - 文件上传页 (upload.html)
            - GET /monitor - 任务监控页 (monitor.html)
            - GET /results - 结果管理页 (results.html)
            - GET /diagnostic - 系统诊断页 (diagnostic.html)
        * ii. **基础API配置**：
            - 跨域设置 (CORS)
            - 中间件配置
            - 全局异常处理
        * iii. **系统状态接口**：
            - GET /api/status - 系统运行状态
            - GET /api/health - 健康检查
    c. **代码示例**：
        ```python
        from fastapi import APIRouter, Request
        from fastapi.responses import HTMLResponse
        from fastapi.templating import Jinja2Templates
        
        router = APIRouter()
        templates = Jinja2Templates(directory="templates")
        
        # 页面路由
        @router.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            return templates.TemplateResponse("index.html", {"request": request})
        
        # 系统状态
        @router.get("/api/status")
        async def get_system_status():
            return {"status": "running", "timestamp": datetime.now()}
        ```
### 3. api/upload.py - 文件上传相关API
    a. **职责描述**：处理文件上传、验证、存储相关功能
    b. **主要接口**：
        * i. POST /api/upload
            - 功能：上传文件
            - 参数：files (multipart/form-data)
            - 返回：{task_id, filename, status, message}
        * ii. GET /api/upload/status/{task_id}
            - 功能：获取上传进度
            - 参数：task_id
            - 返回：{task_id, status, progress, message}
        * iii. DELETE /api/upload/{file_id}
            - 功能：删除已上传文件
            - 参数：file_id
            - 返回：{success, message}
    c. **实现要点**：
        - 文件类型验证 (PNG, JPG, PDF)
        - 文件大小限制 (默认10MB)
        - 异步上传处理
        - 上传进度追踪
### 4. api/monitor.py - 任务监控API
    a. **职责描述**：任务管理、状态监控、性能统计
    b. **主要接口**：
        * i. GET /api/tasks
            - 功能：获取任务列表
            - 参数：page, limit, status (可选)
            - 返回：{tasks, total, page, limit}
        * ii. GET /api/tasks/{task_id}
            - 功能：获取任务详情
            - 参数：task_id
            - 返回：{task_id, status, progress, result, error}
        * iii. PUT /api/tasks/{task_id}
            - 功能：更新任务状态
            - 参数：task_id, action (pause, resume, cancel)
            - 返回：{success, message}
        * iv. DELETE /api/tasks/{task_id}
            - 功能：删除任务
            - 参数：task_id
            - 返回：{success, message}
    c. **WebSocket接口**：
        * i. WS /ws/monitor
            - 功能：实时任务状态推送
            - 推送：任务进度、状态变更、系统指标
### 5. api/results.py - 结果管理API
    a. **职责描述**：结果查询、展示、下载、导出
    b. **主要接口**：
        * i. GET /api/results
            - 功能：获取结果列表
            - 参数：page, limit, date_range (可选)
            - 返回：{results, total, summary}
        * ii. GET /api/results/{task_id}
            - 功能：获取具体结果
            - 参数：task_id
            - 返回：{task_id, ocr_result, structured_data, confidence}
        * iii. GET /api/results/{task_id}/download
            - 功能：下载Excel文件
            - 参数：task_id, format (xlsx, csv)
            - 返回：文件下载流
        * iv. POST /api/export
            - 功能：批量导出
            - 参数：{task_ids, format, template}
            - 返回：{export_id, download_url}
    c. **结果格式**：
        ```json
        {
            "task_id": "uuid",
            "filename": "report.jpg",
            "ocr_result": {
                "text_regions": [...],
                "tables": [...],
                "fields": [...]
            },
            "structured_data": {
                "patient_name": "张三",
                "age": 45,
                "weight": 70.5,
                "body_fat": 15.2
            },
            "confidence": 0.95,
            "processing_time": 2.3
        }
        ```
### 6. api/diagnostic.py - 系统诊断API
    a. **职责描述**：环境检查、服务健康、性能诊断
    b. **主要接口**：
        * i. GET /api/diagnostic/gpu
            - 功能：GPU状态检查
            - 返回：{gpu_available, memory_usage, temperature, driver_version}
        * ii. GET /api/diagnostic/services
            - 功能：服务健康检查
            - 返回：{paddleocr: status, ml_backend: status, redis: status}
        * iii. GET /api/diagnostic/logs
            - 功能：获取日志
            - 参数：level, lines, service
            - 返回：{logs, total}
        * iv. POST /api/diagnose
            - 功能：触发环境检查
            - 参数：{check_type: "full|quick|gpu"}
            - 返回：{check_id, status, results}
    c. **诊断结果格式**：
        ```json
        {
            "check_id": "uuid",
            "timestamp": "2025-11-08T17:18:53",
            "results": {
                "python_version": "3.10.0",
                "dependencies": {
                    "fastapi": "0.121.0 [OK]",
                    "pandas": "2.3.3 [OK]",
                    "paddleocr": "Not Installed [ERROR]"
                },
                "gpu": {
                    "available": true,
                    "memory_used": "2.1GB/8.0GB",
                    "temperature": "65°C"
                },
                "disk_space": "45GB/100GB",
                "recommendations": [
                    "安装缺失的依赖包: pip install paddleocr",
                    "清理临时文件释放磁盘空间"
                ]
            }
        }
        ```
---
## 九、mybci项目流程设计
### 1. 核心功能模块
    a. 启动 FastAPI 主服务，管理任务调度与结果导出。
    b. **调用 paddleocr 项目接口**完成推理（通过paddleocr_client模块）。
    c. 提供 Excel 导出接口。
    d. **新增核心功能**：
        - (1) 环境检查集成到服务启动流程
        - (2) 任务执行前的环境状态验证
        - (3) 环境异常时的优雅降级与用户提示
        - (4) **paddleocr客户端自动重连和错误恢复**
### 2. 主要端点定义
    a. **页面路由端点**：
        - GET / - 主页
        - GET /upload - 文件上传页
        - GET /monitor - 任务监控页
        - GET /results - 结果管理页
        - GET /diagnostic - 系统诊断页
    b. **API端点**：
        - POST /api/upload - 文件上传
        - GET /api/tasks - 获取任务列表
        - PUT /api/tasks/{id} - 更新任务状态
        - GET /api/results - 获取结果列表
        - GET /api/results/{id} - 获取具体结果
        - POST /api/export - 导出结果
        - GET /api/status - 系统状态
        - POST /api/diagnose - 触发环境检查
    c. **WebSocket端点**：
        - WS /ws/monitor - 实时状态推送
        - WS /ws/progress - 进度更新推送
        - WS /ws/logs - 日志流推送
    d. **新增端点**：
        - (1) `/api/paddleocr/ping` - paddleocr服务健康检查
        - (2) `/api/paddleocr/test` - 连接测试接口
        - (3) `/api/config/validate` - 配置文件验证
### 3. 异步处理机制
    a. 使用 Redis 作为任务队列。
    b. 后端采用 FastAPI BackgroundTask 或 Celery worker 实现并行推理。
    c. **增强机制**：
        - (1) 环境状态作为任务元数据
        - (2) 环境异常时自动暂停任务队列
        - (3) 依赖包状态监控与自动告警
        - (4) **paddleocr服务重试机制和熔断器模式**
### 4. paddleocr客户端调用模块
    a. **模块位置**：services/paddleocr_client.py
    b. **核心功能**：
        * i. **HTTP客户端封装**：
            - 统一的paddleocr API调用接口
            - 请求重试和超时处理
            - 响应数据解析和错误处理
        * ii. **连接管理**：
            - 连接池管理
            - 健康检查和自动重连
            - 服务发现和负载均衡
        * iii. **数据处理**：
            - 请求数据序列化
            - 响应数据反序列化
            - 文件上传和下载处理
    c. **接口设计**：
        ```python
        class PaddleOCRClient:
            def __init__(self, base_url: str, timeout: int = 30):
                self.base_url = base_url
                self.timeout = timeout
                self.session = httpx.AsyncClient()
            
            async def analyze_document(self, image_path: str, config: dict) -> dict:
                """调用paddleocr文档分析接口"""
                pass
            
            async def health_check(self) -> bool:
                """paddleocr服务健康检查"""
                pass
            
            async def get_config(self, config_name: str) -> dict:
                """获取OCR配置"""
                pass
        ```
---
## 十、部署与启动方案
### 1. 开发环境部署步骤
    a. 创建 Conda 环境：
        * i. `conda create -n paddleocr python=3.10 -y`
        * ii. `conda activate paddleocr`
    b. **安装 PaddleOCR（基于实际验证）**：
        * i. GPU版本（CUDA 11.8）：
            - (1) `pip install paddlepaddle-gpu==2.6.2.post118 -f https://www.paddlepaddle.org.cn/whle/windows/mkl/avx/stable.html`
        * ii. GPU版本（CUDA 12.x）：
            - (1) `pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu129/`
        * iii. PaddleOCR完整版：
            - (1) `pip install "paddleocr[all]"`
    c. **安装ML Backend必需包**（新增，基于实际验证）：
        * i. `pip install fastapi uvicorn label-studio-ml aiofiles`
    d. **安装核心依赖包**（基于实际验证）：
        * i. `pip install opencv-python-headless progressbar2 attrdict rapidfuzz`
    e. **安装mybci项目依赖**：
        * i. 创建 mybci 环境：`conda create -n mybci python=3.10 -y`
        * ii. 安装依赖：`pip install -r requirements.txt`
    f. 验证 GPU：
        * i. `python -c "import paddle; print(paddle.is_compiled_with_cuda()); print(paddle.device.get_device())"`
### 2. 启动流程（集成环境检查）
    a. **启动前环境验证**：
        * i. 运行 `check_paddleocr_env_fixed.bat` 确认环境状态。
        * ii. 验证所有[已安装]状态后方可启动服务。
    b. 启动 paddleocr 项目：
        * i. `python run_paddleocr.py`
        * ii. 验证环境检查功能正常
    c. 启动 ML Backend接口服务：
        * i. `python run_ml_backend.py`
        * ii. 确认 `/predict` 端点可用
    d. 启动 MCP服务：
        * i. `python mcp_service.py`
        * ii. 确认MCP工具接口可用
    e. 启动 mybci项目服务：
        * i. `python run_mybci.py`
        * ii. 验证前端界面可访问
    f. 启动 Label Studio：
        * i. `docker run -it -p 8080:8080 heartexlabs/label-studio`
    g. **启动验证**：
        - (1) 确认所有服务健康检查通过
        - (2) 验证ML Backend连接正常
        - (3) 测试环境检查功能可用
        - (4) **验证paddleocr客户端连接正常**
### 3. 启动脚本详细说明
    a. **run_paddleocr.py**：
        * i. 启动HTTP服务器 (端口8080)
        * ii. 加载PaddleOCR模型
        * iii. 注册API路由：/ocr/analyze, /health, /env/validate
        * iv. 启动日志记录
    b. **run_ml_backend.py**：
        * i. 启动ML Backend服务 (端口8081)
        * ii. 注册Label Studio接口：/predict, /health
        * iii. 连接paddleocr服务
        * iv. 格式转换适配
    c. **run_mybci.py**：
        * i. 启动FastAPI应用 (端口8000)
        * ii. 注册所有API路由模块
        * iii. 启动WebSocket服务
        * iv. 初始化数据库连接
        * v. **初始化paddleocr客户端连接**
---
## 十一、测试与验证
### 1. 单图测试
    a. 调用 `/ocr/single` 接口，上传单张图片。
    b. 返回 JSON 结构应包含文字块、位置坐标、层级关系。
    c. **环境测试**：
        - (1) 运行环境检查脚本验证测试环境
        - (2) 确认PP-StructureV3导入成功
### 2. 批量测试
    a. 提供图片目录路径。
    b. 输出结构化 Excel 文件，字段包含：
        * i. 图片文件名
        * ii. 文本内容
        * iii. 类别标签
    c. **批量环境测试**：
        - (1) 大量任务时的环境稳定性
        - (2) 依赖包状态持续监控
### 3. 对接验证
    a. 在 Label Studio 中选择任务 → 点击"自动标注" → 应正确加载 OCR 结果。
    b. **完整对接验证**：
        - (1) ML Backend包完整性检查
        - (2) 环境检查接口可用性验证
        - (3) 异常环境下的降级处理验证
### 4. 端到端流程测试
    a. **完整OCR工作流测试**：
        * i. Label Studio标注 → JSON导出 → 配置转换 → 存储到mybci/config
        * ii. mybci加载配置 → paddleocr客户端调用 → OCR识别 → Excel输出
    b. **环境检查验证**：
        - (1) 运行环境检查脚本系列验证
        - (2) 模拟环境问题测试检测能力
        - (3) 一键安装功能有效性测试
    c. **新增测试项目**：
        - (1) paddleocr客户端连接稳定性测试
        - (2) API路由模块功能完整性测试
        - (3) 配置文件归属正确性验证
---
## 十二、后续计划与扩展
### 1. 后续功能扩展
    a. 增加版面自适应模板匹配算法。
    b. 支持更多类型文档（发票、化验单）。
    c. 增强与 MinerU、Donut 等模型的可替换性接口。
    d. **环境管理扩展**：
        - (1) 自动环境健康检查
        - (2) 智能依赖包版本管理
        - (3) 环境迁移与备份工具
    e. **系统扩展**：
        - (1) 支持多租户配置管理
        - (2) API版本管理和向后兼容
        - (3) 分布式部署支持
### 2. 容器化与部署规划
    a. 将paddleocr和mybci项目分别封装为 Docker 容器。
    b. 使用 Docker Compose 编排：
        * i. `labelstudio`
        * ii. `paddleocr_engine`
        * iii. `mybci_app`
    c. **容器化增强**：
        - (1) 集成环境检查到容器启动流程
        - (2) 提供环境状态监控容器
        - (3) 自动化环境配置容器
### 3. 日志与监控
    a. 每个服务均输出日志至 logs 目录。
    b. 提供监控脚本 monitor_system.py：
        * i. 检测 GPU 占用
        * ii. 检测服务存活状态
        * iii. 定时重启异常进程
    c. **监控增强**：
        - (1) 环境状态监控
        - (2) 依赖包健康检查
        - (3) 自动环境诊断与报告
        - (4) **paddleocr服务连接监控**
---
## 十三、故障排除指南
### 1. 常见问题与解决方案
    a. **配置文件归属问题**：
        - 问题：配置文件存储位置混乱
        - 解决：明确配置文件存储在mybci/config/目录，建立配置管理规范
    b. **API路由模块问题**：
        - 问题：API功能分散，难以维护
        - 解决：采用模块化设计，每个功能独立API文件
    c. **paddleocr客户端连接问题**：
        - 问题：服务间通信失败
        - 解决：实现重试机制、健康检查、自动重连
### 2. 调试和诊断工具
    a. **环境检查套件**：
        - check_paddleocr_env_fixed.bat - 全面环境检查
        - install_missing_packages.bat - 一键安装缺失包
    b. **API测试工具**：
        - 集成Swagger UI自动生成的API文档
        - 提供API测试脚本
    c. **服务连接诊断**：
        - paddleocr服务ping接口
        - 服务间连接状态监控
---
**文档名称**：体脂秤报告自动化处理_项目代码编写计划
**版本号**：v5.2
**最后更新**：2025-11-08
**更新内容**：
- (1) 修正项目目录结构设计（配置文件归属优化）
- (2) 明确API路由模块职责和启动脚本功能
- (3) 添加mybci项目依赖包详细清单
- (4) 完善paddleocr客户端调用模块设计
- (5) 增强配置管理和风险控制
- (6) 完善故障排除指南和诊断工具
**格式规范**：完全遵循用户提供的 Markdown 层级缩进规范（v1.0-20251107）