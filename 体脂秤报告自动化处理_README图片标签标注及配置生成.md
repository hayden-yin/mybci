## 创建 OCR 标注配置文件操作指南

### 准备工作：启动所需服务

1. 启动 Label Studio (Docker)
    * 在您的终端中运行（确保 Docker 正在运行）：
        ```bash
        docker run -p 8080:8080 heartexlabs/label-studio
        ```

2. 启动 ML 辅助标注后端
    * 在您的 mybci Conda 环境中，从项目根目录启动 ML 后端服务（它将为 Label Studio 提供预标注）：
        ```bash
        # 激活环境
        conda activate mybci

        # 确保已安装依赖
        # pip install -e .

        # 启动 ML 后端服务 (假设它运行在 8001 端口)
        python run_ml_backend.py
        ```
    * 请检查 `run_ml_backend.py` 或 `src/mybci/ml_backend/server.py` 以确认其运行的端口，这里我们假设为 `8001`。

### 详细步骤

#### 步骤 1：登录并创建 Label Studio 项目

1. 在浏览器中打开 http://localhost:8080。
2. 注册或登录 Label Studio。
3. 点击 "Create Project"，为项目命名（例如：BCI Report OCR）。

#### 步骤 2：配置标注界面 (Labeling Interface)

1. 这是最关键的一步，您需要在这里定义您想提取的"字段"。
    * 在项目创建页面，找到 "Labeling Interface"（标注界面）板块。
    * 点击 "Browse Templates"（浏览模板），选择 "OCR" 类别下的 "Transcribe text from images"（从图像转录文本）模板。
    * 您会看到一个 XML 配置。
    * 请删除默认内容，并将其替换为以下专用于"区域提取"的配置：
        ```xml
        <View>
          <Image name="image" value="$image"/>
          
          <RectangleLabels name="label" toName="image">
            <Label value="Patient_Name" background="#FF0000" />
            <Label value="Report_ID" background="#00FF00" />
            <Label value="Result_A" background="#0000FF" />
            <Label value="Result_B" background="#FFFF00" />
            </RectangleLabels>
          
          <TextArea name="transcription" toName="image" 
                    editable="true" 
                    perRegion="true" 
                    required="true" 
                    maxSubmissions="1" 
                    rows="5" 
                    placeholder="校对 OCR 识别结果..." />
        </View>
        ```
    * 点击 **"Save"** 保存界面配置。

#### 步骤 3：连接 ML 辅助标注后端

1. 在项目页面顶部，点击 "Settings"（设置）。
2. 选择左侧菜单的 "Machine Learning"（机器学习）。
3. 点击 "Add Model"（添加模型）。
4. URL：填入您在"准备工作"中启动的 ML 后端地址。
    * 重要提示： 由于 Label Studio 在 Docker 容器中运行，它不能直接访问 localhost。您需要使用 Docker 的特殊地址来访问宿主机：
    * URL 应填： http://host.docker.internal:8001 (假设 ML 后端在 8001 端口)
5. 勾选 "Use for pre-annotation"（用于预标注）。
6. 点击 "Validate and Save"。
7. 连接成功后，返回 "Machine Learning" 页面，确保新添加的模型旁边有一个绿色的对勾，表示连接正常。

#### 步骤 4：上传示例图片 (方案二)

1. 返回项目的主仪表板（点击左上角的项目名称）。
2. 点击 "Import"（导入）按钮。
3. 直接拖拽或点击上传 5 到 10 张具有代表性的报告图片（JPG 或 PNG）。
4. 等待上传和处理完成。

#### 步骤 5：开始标注与校正

1. 点击项目仪表板上的 "Label All Tasks"（标注所有任务）按钮。
2. 当第一张图片加载时，请稍等片刻。
    * 您会看到 ML 后端（ml_backend）自动运行 PaddleOCR 并在图片上绘制了**"预标注"**的识别框。
3. 您的核心工作：
    * 检查预标注： 检查 ML 后端返回的识别框（它们可能不包含您在步骤 2 中定义的标签）。
    * 删除无效框： 删除所有您不关心的识别框。
    * 绘制目标框：
        - 从右侧选择您定义的标签（例如 Patient_Name）。
        - 在图片上精确框出"患者姓名"所在的区域。
        - （可选）在框体弹出的 transcription 文本框中，检查 OCR 识别的文本是否正确，如果不正确，请手动修正它。
    * 确保完整： 确保您在步骤 2 中定义的每一个 Label（Patient_Name, Report_ID 等），在这张图片上都有且仅有一个对应的标注框。
4. 完成后，点击 "Submit"（提交）进入下一张图片。
5. 重复此过程，直到所有示例图片都标注完毕。

#### 步骤 6：导出标注数据

1. 完成所有标注后，返回项目仪表板。
2. 点击 "Export"（导出）按钮。
3. 在弹出的窗口中，选择 "JSON" 格式。
4. 导出的文件（例如 project-1-at-....json），请将其重命名为 ls_export.json。
5. 将这个 ls_export.json 文件移动到您 mybci/ 项目的根目录下（与 src/ 和 config/ 目录同级）。

#### 步骤 7：生成最终的 config_ocr.json

1. 确保您仍在 mybci Conda 环境中。
2. 在项目根目录（mybci/）下，运行计划书中设计的转换脚本：
    ```bash
    python src/mybci/utils/convert_ls_to_config.py
    ```
    * 脚本会读取 `ls_export.json`，分析您在 Label Studio 中标注的区域和标签，并自动生成 `config/config_ocr_bci.json` 文件。

### 配置完成

1. 恭喜！您已经成功创建了自动化 OCR 所需的核心配置文件。
2. 您现在可以按 Ctrl+C 关闭 run_ml_backend.py 服务（日常运行时不再需要它），并启动 run_web_app.py 来开始您的日常自动化处理工作了。