#/src/mybci/ocr_processing/ppstructure_engine.py
"""
PaddleOCR / PaddleStructure 引擎封装
----------------------------------
负责对图像进行版面分析与文本提取，返回结构化结果。

依赖：
    pip install paddleocr pillow

后续可扩展：
    - 增加 layoutparser 支持
    - 增加自定义字段抽取逻辑
    - 增加 GPU / CPU 选项
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from paddleocr import PaddleOCR
from PIL import Image


class PPStructureEngine:
    """
    PaddleOCR 结构化识别封装类。
    """

    def __init__(self, lang: str = "ch", use_angle_cls: bool = True, use_gpu: bool = False):
        """
        初始化 PaddleOCR 引擎。
        """
        self.lang = lang
        self.ocr = PaddleOCR(
            lang=lang,
            use_angle_cls=use_angle_cls,
            use_gpu=use_gpu,
            show_log=False
        )

    def process_image(self, image_path: str) -> List[Dict[str, Any]]:
        """
        对单张图片进行 OCR 识别。
        返回结构化的行列表，每行包含文本与置信度。
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        result = self.ocr.ocr(image_path, cls=True)
        structured_data = []

        for line in result[0]:
            bbox, (text, confidence) = line
            structured_data.append({
                "text": text,
                "confidence": float(confidence),
                "bbox": bbox
            })

        return structured_data

    def save_result(self, result: List[Dict[str, Any]], output_dir: str, base_name: str):
        """
        将识别结果保存为 JSON 文件。
        """
        import json
