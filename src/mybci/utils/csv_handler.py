#/src/mybci/utils/csv_handler.py
"""
CSV 输出工具模块
------------------
功能：
  - 将 OCR 结果（list[dict]）保存为 CSV 文件
  - 支持自定义输出列
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional, Any


def save_to_csv(
    result: List[Dict[str, Any]],
    columns: Optional[List[str]],
    output_dir: str,
    base_name: str
) -> str:
    """
    保存 OCR 结果为 CSV 文件。

    参数：
        result: OCR 识别结果（list[dict]）
        columns: 需要输出的字段名列表（None 表示自动取全部）
        output_dir: 输出目录
        base_name: 输出文件基础名（不含扩展名）

    返回：
        csv_path: 生成的 CSV 文件路径
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    csv_path = Path(output_dir) / f"{base_name}_ocr.csv"

    if not result:
        # 空结果时写入空表头
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(columns or ["text", "confidence", "bbox"])
        return str(csv_path)

    # 自动推断字段
    if columns is None:
        columns = list(result[0].keys())

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for item in result:
            filtered = {key: item.get(key, "") for key in columns}
            writer.writerow(filtered)

    return str(csv_path)
