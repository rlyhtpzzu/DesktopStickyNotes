from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QDateEdit, QTimeEdit, QLabel, QGridLayout)
from PyQt5.QtCore import QDateTime, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
import sys
import os

# 添加父目录到路径以便导入其他模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import config

class TimePicker(QWidget):
    """高级时间选择器"""
    
    timeChanged = pyqtSignal(QDateTime)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_datetime = QDateTime.currentDateTime()
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # 快速选择
        quick_select_layout = QHBoxLayout()
        
        quick_select_label = QLabel("快速选择:")
        quick_select_label.setFont(QFont(config.FONT_FAMILY, 9))
        
        self.quick_combo = QComboBox()
        self.quick_combo.addItems([
            "自定义时间",
            "15分钟后", 
            "30分钟后",
            "1小时后",
            "2小时后",
            "今天 12:00",
            "今天 18:00",
            "今天 21:00",
            "明天 09:00",
            "明天此时"
        ])
        
        quick_select_layout.addWidget(quick_select_label)
        quick_select_layout.addWidget(self.quick_combo)
        quick_select_layout.setStretchFactor(self.quick_combo, 1)
        
        # 详细时间选择
        detail_layout = QGridLayout()
        detail_layout.setHorizontalSpacing(8)
        detail_layout.setVerticalSpacing(4)
        
        # 日期选择
        date_label = QLabel("日期:")
        date_label.setFont(QFont(config.FONT_FAMILY, 9))
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())  # 只能选择今天及以后的日期
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        
        # 时间选择
        time_label = QLabel("时间:")
        time_label.setFont(QFont(config.FONT_FAMILY, 9))
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime().addSecs(3600))  # 默认1小时后
        self.time_edit.setDisplayFormat("HH:mm")
        
        # 星期显示
        self.weekday_label = QLabel()
        self.weekday_label.setFont(QFont(config.FONT_FAMILY, 9))
        self.update_weekday_label()
        
        detail_layout.addWidget(date_label, 0, 0)
        detail_layout.addWidget(self.date_edit, 0, 1)
        detail_layout.addWidget(time_label, 1, 0)
        detail_layout.addWidget(self.time_edit, 1, 1)
        detail_layout.addWidget(self.weekday_label, 0, 2, 2, 1)
        
        # 组装布局
        layout.addLayout(quick_select_layout)
        layout.addLayout(detail_layout)
    
    def apply_styles(self):
        """应用样式"""
        style_sheet = f"""
            QComboBox, QDateEdit, QTimeEdit {{
                background: rgba(255, 255, 255, 200);
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                padding: 4px 8px;
                font-family: {config.FONT_FAMILY};
                font-size: 11px;
                min-height: 24px;
            }}
            QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {{
                border: 1px solid #4A90E2;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 1px solid #DDDDDD;
                width: 20px;
            }}
            QLabel {{
                background: transparent;
                font-family: {config.FONT_FAMILY};
                color: #666666;
            }}
            QCalendarWidget {{
                background: white;
                border: 1px solid #CCCCCC;
            }}
        """
        self.setStyleSheet(style_sheet)
    
    def connect_signals(self):
        """连接信号槽"""
        self.quick_combo.currentIndexChanged.connect(self.on_quick_select_changed)
        self.date_edit.dateChanged.connect(self.on_datetime_changed)
        self.time_edit.timeChanged.connect(self.on_datetime_changed)
    
    def on_quick_select_changed(self, index):
        """快速选择改变事件"""
        if index == 0:  # 自定义时间
            return
        
        now = QDateTime.currentDateTime()
        new_datetime = now
        
        if index == 1:  # 15分钟后
            new_datetime = now.addSecs(15 * 60)
        elif index == 2:  # 30分钟后
            new_datetime = now.addSecs(30 * 60)
        elif index == 3:  # 1小时后
            new_datetime = now.addSecs(3600)
        elif index == 4:  # 2小时后
            new_datetime = now.addSecs(7200)
        elif index == 5:  # 今天 12:00
            new_datetime = QDateTime(QDate.currentDate(), QTime(12, 0))
        elif index == 6:  # 今天 18:00
            new_datetime = QDateTime(QDate.currentDate(), QTime(18, 0))
        elif index == 7:  # 今天 21:00
            new_datetime = QDateTime(QDate.currentDate(), QTime(21, 0))
        elif index == 8:  # 明天 09:00
            new_datetime = QDateTime(QDate.currentDate().addDays(1), QTime(9, 0))
        elif index == 9:  # 明天此时
            new_datetime = now.addDays(1)
        
        # 更新控件
        self.date_edit.setDate(new_datetime.date())
        self.time_edit.setTime(new_datetime.time())
        self.update_weekday_label()
        
        # 发射信号
        self.timeChanged.emit(new_datetime)
    
    def on_datetime_changed(self):
        date = self.date_edit.date()
        time = self.time_edit.time()
        new_datetime = QDateTime(date, time)
        
        # 验证日期不能是过去
        if new_datetime < QDateTime.currentDateTime():
            # 重置为当前时间+5分钟
            current = QDateTime.currentDateTime().addSecs(300)
            self.date_edit.setDate(current.date())
            self.time_edit.setTime(current.time())
            return
        
        self.current_datetime = new_datetime
        self.update_weekday_label()
        self.timeChanged.emit(new_datetime)
        
        # 重置快速选择为"自定义时间"
        self.quick_combo.setCurrentIndex(0)
    
    def update_weekday_label(self):
        """更新星期显示"""
        date = self.date_edit.date()
        weekday = date.dayOfWeek()
        
        weekdays = {
            1: "星期一",
            2: "星期二", 
            3: "星期三",
            4: "星期四",
            5: "星期五",
            6: "星期六",
            7: "星期日"
        }
        
        weekday_text = weekdays.get(weekday, "")
        
        # 添加特殊日期标识
        today = QDate.currentDate()
        if date == today:
            weekday_text = "今天"
        elif date == today.addDays(1):
            weekday_text = "明天"
        elif date == today.addDays(2):
            weekday_text = "后天"
        
        self.weekday_label.setText(weekday_text)
    
    def get_datetime(self) -> QDateTime:
        """获取当前选择的日期时间"""
        return self.current_datetime
    
    def set_datetime(self, datetime_obj):
        """设置日期时间"""
        if isinstance(datetime_obj, datetime):
            qdatetime = QDateTime(
                QDate(datetime_obj.year, datetime_obj.month, datetime_obj.day),
                QTime(datetime_obj.hour, datetime_obj.minute)
            )
        elif isinstance(datetime_obj, QDateTime):
            qdatetime = datetime_obj
        else:
            return
        
        self.date_edit.setDate(qdatetime.date())
        self.time_edit.setTime(qdatetime.time())
        self.current_datetime = qdatetime
        self.update_weekday_label()
    
    def get_python_datetime(self) -> datetime:
        """获取Python datetime对象"""
        qdt = self.get_datetime()
        return datetime(
            qdt.date().year(),
            qdt.date().month(), 
            qdt.date().day(),
            qdt.time().hour(),
            qdt.time().minute()
        )

class CompactTimePicker(QWidget):
    """紧凑版时间选择器（用于笔记组件中）"""
    
    timeChanged = pyqtSignal(QDateTime)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()
    
    def setup_ui(self):
        """设置界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # 日期选择
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("MM-dd")
        self.date_edit.setFixedWidth(70)
        
        # 时间选择
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime().addSecs(3600))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFixedWidth(60)
        
        # 星期显示
        self.weekday_label = QLabel()
        self.weekday_label.setFont(QFont(config.FONT_FAMILY, 9))
        self.weekday_label.setFixedWidth(40)
        self.update_weekday_label()
        
        layout.addWidget(self.date_edit)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.weekday_label)
        layout.addStretch()
    
    def apply_styles(self):
        """应用样式"""
        style_sheet = f"""
            QDateEdit, QTimeEdit {{
                background: rgba(255, 255, 255, 200);
                border: 1px solid #DDDDDD;
                border-radius: 3px;
                padding: 2px 4px;
                font-family: {config.FONT_FAMILY};
                font-size: 10px;
            }}
            QLabel {{
                background: transparent;
                font-family: {config.FONT_FAMILY};
                color: #666666;
                font-size: 9px;
            }}
        """
        self.setStyleSheet(style_sheet)
    
    def connect_signals(self):
        """连接信号槽"""
        self.date_edit.dateChanged.connect(self.on_datetime_changed)
        self.time_edit.timeChanged.connect(self.on_datetime_changed)
    
    def on_datetime_changed(self):
        """日期时间改变事件"""
        date = self.date_edit.date()
        time = self.time_edit.time()
        new_datetime = QDateTime(date, time)
        
        # 验证日期不能是过去
        if new_datetime < QDateTime.currentDateTime():
            current = QDateTime.currentDateTime().addSecs(300)
            self.date_edit.setDate(current.date())
            self.time_edit.setTime(current.time())
            return
        
        self.update_weekday_label()
        self.timeChanged.emit(new_datetime)
    
    def update_weekday_label(self):
        """更新星期显示"""
        date = self.date_edit.date()
        weekday = date.dayOfWeek()
        
        weekdays = {
            1: "周一",
            2: "周二", 
            3: "周三",
            4: "周四",
            5: "周五",
            6: "周六",
            7: "周日"
        }
        
        weekday_text = weekdays.get(weekday, "")
        
        today = QDate.currentDate()
        if date == today:
            weekday_text = "今天"
        elif date == today.addDays(1):
            weekday_text = "明天"
        
        self.weekday_label.setText(weekday_text)
    
    def get_datetime(self) -> QDateTime:
        """获取当前选择的日期时间"""
        return QDateTime(self.date_edit.date(), self.time_edit.time())
    
    def set_datetime(self, datetime_obj):
        """设置日期时间"""
        if isinstance(datetime_obj, datetime):
            qdatetime = QDateTime(
                QDate(datetime_obj.year, datetime_obj.month, datetime_obj.day),
                QTime(datetime_obj.hour, datetime_obj.minute)
            )
        elif isinstance(datetime_obj, QDateTime):
            qdatetime = datetime_obj
        else:
            return
        
        self.date_edit.setDate(qdatetime.date())
        self.time_edit.setTime(qdatetime.time())
        self.update_weekday_label()