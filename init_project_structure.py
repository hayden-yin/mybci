#/init_project_structure.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_project_structure.py
创建项目基础目录结构，并为每个模块生成空的 __init__.py 文件。
"""

from pathlib import Path

# 定义项目目录结构
DIRS = [
    "config",
    "input",
    "output",
    "logs",
    "src/mybci/core",
    "src/mybci/ocr_processing",
    "src/mybci/ml_backend",
    "src/mybci/webapp",
    "src/mybci/utils",
]

def create_dir(path: Path):
    """创建目录（若不存在）"""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[+] Created directory: {path}")
    else:
        print(f"[=] Exists: {path}")

def create_init(path: Path):
    """在目录下生成空的 __init__.py"""
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")
        print(f"    └── Created: {init_file}")
    else:
        print(f"    └── Exists: {init_file}")

def main():
    root = Path(__file__).resolve().parent
    print("\n📁 初始化项目目录结构...\n")

    for d in DIRS:
        dir_path = root / d
        create_dir(dir_path)
        # 若是 src/mybci 下的目录，创建 __init__.py
        if "src/mybci" in d:
            create_init(dir_path)

    # 顶层 mybci 也需要 __init__.py
    mybci_root = root / "src/mybci"
    create_init(mybci_root)

    print("\n✅ 项目结构初始化完成。\n")

if __name__ == "__main__":
    main()
