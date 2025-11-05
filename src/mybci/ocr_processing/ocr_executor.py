#/src/mybci/ocr_processing/ocr_executor.py
"""
OCR 执行器模块
------------------
封装了对 PPStructureEngine 的调用逻辑。

功能：
  - 接收输入图片路径与配置参数
  - 调用 PaddleOCR 引擎进行识别
  - 生成标准化结果文件（JSON / CSV）
  - 返回运行状态与输出路径
"""

from pathlib import Path
from typing import Dict, Any
from .ppstructure_engine import PPStructureEngine
from ..utils.csv_handler import save_to_csv


class OCRExecutor:
    """
    OCR 执行控制器。
    用于封装一整次 OCR 任务的执行流程。
    """

    def __init__(self, use_gpu: bool = False):
        self.engine = PPStructureEngine(use_gpu=use_gpu)

    def run(self, image_path: str, output_dir: str = "output", config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行 OCR 流程。
        返回：
            {
                "image": "input/sample.jpg",
                "json_output": "output/sample_ocr.json",
                "csv_output": "output/sample_ocr.csv",
                "num_lines": 12
            }
        """
        image_path = Path(image_path)
        base_name = image_path.stem
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Step 1: OCR 识别
        result = self.engine.process_image(str(image_path))

        # Step 2: 保存 JSON
        json_path = self.engine.save_result(result, output_dir, base_name)

        # Step 3: 保存 CSV（根据 config 的字段列）
        csv_path = None
        if config and "output_columns" in config:
            csv_path = save_to_csv(result, config["output_columns"], output_dir, base_name)
        else:
            csv_path = save_to_csv(result, None, output_dir, base_name)

        # Step 4: 汇总结果
        return {
            "image": str(image_path),
            "json_output": json_path,
            "csv_output": csv_path,
            "num_lines": len(result)
        }


if __name__ == "__main__":
    # 手动测试
    sample_img = "input/sample.jpg"
    executor = OCRExecutor(use_gpu=False)
    cfg = {"output_columns": ["text", "confidence"]}
    summary = executor.run(sample_img, "output", cfg)
    print(summary)
