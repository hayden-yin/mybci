#/src/mybci/utils/logger.py
"""
日志工具模块
------------------
功能：
  - 提供统一的日志记录接口
  - 支持控制台输出和文件输出
  - 可自定义日志格式和级别
"""

import logging
from pathlib import Path


def get_logger(
    name: str = "mybci",
    log_file: str | Path = None,
    level: int = logging.INFO,
    console: bool = True
) -> logging.Logger:
    """
    创建并返回一个 logger。

    参数:
        name: logger 名称
        log_file: 可选，日志文件路径
        level: 日志级别
        console: 是否输出到控制台
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 避免重复添加 handler
    if not logger.handlers:
        if console:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger


# === 示例使用 ===
if __name__ == "__main__":
    log = get_logger(log_file="logs/test.log")
    log.info("Logger initialized successfully.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
