#/src/mybci/utils/path_helper.py
"""
路径与文件工具模块
------------------
功能：
  - 统一管理 OCR、标注、输出等目录结构
  - 自动创建缺失的文件夹
  - 提供常用路径拼接与验证函数
"""

import os
from pathlib import Path
from typing import Optional


# === 基础路径定义 ===

def get_project_root() -> Path:
    """返回项目根目录路径（基于 src/mybci 上级）"""
    return Path(__file__).resolve().parents[2]


def get_data_dir(subdir: Optional[str] = None) -> Path:
    """获取数据主目录，可指定子目录"""
    base = get_project_root() / "data"
    if subdir:
        base = base / subdir
    base.mkdir(parents=True, exist_ok=True)
    return base


def get_output_dir(subdir: Optional[str] = None) -> Path:
    """获取输出目录"""
    base = get_project_root() / "outputs"
    if subdir:
        base = base / subdir
    base.mkdir(parents=True, exist_ok=True)
    return base


def ensure_dir(path: str | Path) -> Path:
    """确保路径存在"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# === 文件命名工具 ===

def generate_filename(base_name: str, suffix: str, ext: str = ".txt") -> str:
    """
    生成标准化文件名，例如：
        base_name='report1', suffix='ocr', ext='.csv'
        -> report1_ocr.csv
    """
    clean_base = os.path.splitext(base_name)[0]
    return f"{clean_base}_{suffix}{ext}"


# === 示例 ===
if __name__ == "__main__":
    print("Project root:", get_project_root())
    print("Data dir:", get_data_dir("images"))
    print("Output dir:", get_output_dir("ocr_results"))
