import os
from dataclasses import dataclass
from typing import Tuple

@dataclass
class AppConfig:
    """应用配置类"""
    # 窗口配置
    WINDOW_SIZE: Tuple[int, int] = (300, 400)
    WINDOW_TITLE: str = "桌面便签"
    MINIMIZED_HEIGHT: int = 30  # 隐藏模式时的高度
    
    # 样式配置
    BACKGROUND_COLOR: str = "rgba(255, 253, 231, 230)"  # 浅黄色背景
    BORDER_RADIUS: int = 10
    FONT_FAMILY: str = "Microsoft YaHei, SimHei, sans-serif"
    
    # 数据配置
    DATA_DIR: str = "data"
    NOTES_FILE: str = "notes.json"
    
    # 提醒配置
    CHECK_INTERVAL: int = 1000  # 检查提醒的时间间隔(毫秒)
    
    def __post_init__(self):
        """确保数据目录存在"""
        os.makedirs(self.DATA_DIR, exist_ok=True)
    
    @property
    def notes_file_path(self) -> str:
        """获取笔记文件完整路径"""
        return os.path.join(self.DATA_DIR, self.NOTES_FILE)

# 全局配置实例
config = AppConfig()