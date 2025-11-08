from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QComboBox, QDateTimeEdit, QLabel, 
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime, timedelta
import sys
import os

# 添加父目录到路径以便导入其他模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from note_manager import Note, RepeatType
from config import config
from widgets.time_picker import CompactTimePicker

class NoteWidget(QFrame):
    """单个笔记组件"""
    
    deleted = pyqtSignal(int)  # 笔记ID
    completed = pyqtSignal(int)  # 笔记ID
    
    def __init__(self, note: Note):
        super().__init__()
        self.note = note
        self.is_editing = True  # 新建的笔记默认处于编辑模式
        
        self.setup_ui()
        self.apply_styles()
        self.update_display()
    
    def setup_ui(self):
        """设置界面"""
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        self.complete_btn = QPushButton("○")
        self.complete_btn.setFixedSize(20, 20)
        self.complete_btn.clicked.connect(self.toggle_complete)
        
        self.delete_btn = QPushButton("×")
        self.delete_btn.setFixedSize(20, 20)
        self.delete_btn.clicked.connect(self.delete_note)
        
        toolbar_layout.addWidget(self.complete_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.delete_btn)
        
        # 内容编辑区
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("记录你要做的事情...")
        self.content_edit.setText(self.note.content)
        self.content_edit.textChanged.connect(self.on_content_changed)
        
        # 时间选择区
        time_layout = QHBoxLayout()
        
        # 时间选择
        datetime_layout = QVBoxLayout()
        datetime_layout.setSpacing(2)
        
        datetime_label = QLabel("提醒时间:")
        datetime_label.setFont(QFont(config.FONT_FAMILY, 8))
        
        self.time_picker = CompactTimePicker()
        self.time_picker.set_datetime(self.note.due_date)
        self.time_picker.timeChanged.connect(self.on_datetime_changed)
        
        datetime_layout.addWidget(datetime_label)
        datetime_layout.addWidget(self.time_picker)
        
        # 重复规则选择
        repeat_layout = QVBoxLayout()
        repeat_layout.setSpacing(2)
        
        repeat_label = QLabel("重复:")
        repeat_label.setFont(QFont(config.FONT_FAMILY, 8))
        
        self.repeat_combo = QComboBox()
        for repeat_type in RepeatType:
            self.repeat_combo.addItem(repeat_type.value, repeat_type)
        
        # 设置当前重复类型
        current_index = self.repeat_combo.findData(self.note.repeat_type)
        if current_index >= 0:
            self.repeat_combo.setCurrentIndex(current_index)
        
        self.repeat_combo.currentIndexChanged.connect(self.on_repeat_changed)
        
        repeat_layout.addWidget(repeat_label)
        repeat_layout.addWidget(self.repeat_combo)
        
        time_layout.addLayout(datetime_layout)
        time_layout.addLayout(repeat_layout)
        
        # 状态显示
        self.status_label = QLabel()
        self.status_label.setFont(QFont(config.FONT_FAMILY, 8))
        self.update_status_label()
        
        # 组装布局
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.content_edit)
        layout.addLayout(time_layout)
        layout.addWidget(self.status_label)
        
        # 设置大小策略
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
    
    
    def apply_styles(self):
        """应用样式"""
        style_sheet = f"""
            NoteWidget {{
                background: rgba(255, 255, 255, 180);
                border: 1px solid #CCCCCC;
                border-radius: 8px;
            }}
            QTextEdit {{
                background: rgba(255, 255, 255, 200);
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                padding: 4px;
                font-family: {config.FONT_FAMILY};
                font-size: 12px;
            }}
            QTextEdit:focus {{
                border: 1px solid #4A90E2;
            }}
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 3px;
                font-family: {config.FONT_FAMILY};
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: rgba(0, 0, 0, 0.1);
            }}
            QDateTimeEdit, QComboBox {{
                background: rgba(255, 255, 255, 200);
                border: 1px solid #DDDDDD;
                border-radius: 3px;
                padding: 2px 4px;
                font-family: {config.FONT_FAMILY};
                font-size: 10px;
                min-height: 20px;
            }}
            QLabel {{
                background: transparent;
                font-family: {config.FONT_FAMILY};
                color: #666666;
            }}
        """
        self.setStyleSheet(style_sheet)
    
    def on_content_changed(self):
        """内容改变事件"""
        self.note.content = self.content_edit.toPlainText()
        self.update_status_label()
    
    def on_datetime_changed(self, new_datetime):
        """日期时间改变事件"""
        # 验证日期不能是过去
        if new_datetime < QDateTime.currentDateTime():
            # 重置为当前时间+5分钟
            current = QDateTime.currentDateTime().addSecs(300)
            self.time_picker.set_datetime(current)
            return
        
        # 转换为Python datetime并更新
        python_datetime = datetime(
            new_datetime.date().year(),
            new_datetime.date().month(), 
            new_datetime.date().day(),
            new_datetime.time().hour(),
            new_datetime.time().minute()
        )
        self.note.due_date = python_datetime
        self.update_status_label()
    
    def on_repeat_changed(self, index):
        """重复规则改变事件"""
        repeat_type = self.repeat_combo.currentData()
        self.note.repeat_type = repeat_type
        self.update_status_label()
    
    def toggle_complete(self):
        """切换完成状态"""
        if self.note.content.strip():  # 只有有内容时才允许完成
            self.completed.emit(self.note.id)
    
    def delete_note(self):
        """删除笔记"""
        self.deleted.emit(self.note.id)
    
    def update_status_label(self):
        """更新状态标签"""
        now = datetime.now()
        time_diff = self.note.due_date - now
        
        if time_diff.total_seconds() <= 0:
            status = "🔔 已到期"
            color = "#FF4444"
        elif time_diff.total_seconds() <= 3600:  # 1小时内
            minutes = int(time_diff.total_seconds() / 60)
            status = f"⏰ {minutes}分钟后"
            color = "#FFAA00"
        elif time_diff.days == 0:  # 今天
            hours = int(time_diff.total_seconds() / 3600)
            status = f"📅 今天 {self.note.due_date.strftime('%H:%M')}"
            color = "#44AAFF"
        elif time_diff.days == 1:  # 明天
            status = f"📅 明天 {self.note.due_date.strftime('%H:%M')}"
            color = "#44AAFF"
        else:
            status = f"📅 {self.note.due_date.strftime('%m-%d %H:%M')}"
            color = "#666666"
        
        # 添加重复信息
        if self.note.repeat_type != RepeatType.NONE:
            status += f" 🔄 {self.note.repeat_type.value}"
        
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color};")
    
    def update_display(self):
        """更新显示状态"""
        # 根据笔记状态更新显示
        if self.note.is_completed:
            self.complete_btn.setText("✓")
            self.content_edit.setStyleSheet("text-decoration: line-through; color: #999999;")
            self.setStyleSheet(self.styleSheet() + "background: rgba(240, 240, 240, 180);")
        else:
            self.complete_btn.setText("○")
            self.content_edit.setStyleSheet("text-decoration: none; color: #000000;")
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        self.setStyleSheet(self.styleSheet() + "border: 1px solid #4A90E2;")
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        if not self.note.is_completed:
            self.setStyleSheet(self.styleSheet() + "border: 1px solid #CCCCCC;")