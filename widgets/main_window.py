import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QScrollArea, QLabel,
                             QSystemTrayIcon, QMenu, QAction, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor

# 添加父目录到路径以便导入其他模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import config
from note_manager import note_manager, RepeatType
from widgets.note_widget import NoteWidget

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.is_minimized = False
        self.setup_ui()
        self.setup_tray()
        self.setup_timer()
        self.apply_styles()
        
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setFixedSize(*config.WINDOW_SIZE)
        
        # 设置窗口属性
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 中央部件
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # 标题栏
        title_bar = self.create_title_bar()
        layout.addWidget(title_bar)
        
        # 内容区域
        self.content_area = QWidget()
        self.content_area.setObjectName("ContentArea")
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(6)
        
        # 添加新笔记按钮
        self.add_note_btn = QPushButton("+ 添加新便签")
        self.add_note_btn.clicked.connect(self.add_new_note)
        content_layout.addWidget(self.add_note_btn)
        
        # 笔记列表滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.notes_container = QWidget()
        self.notes_layout = QVBoxLayout(self.notes_container)
        self.notes_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_layout.setSpacing(6)
        
        self.scroll_area.setWidget(self.notes_container)
        content_layout.addWidget(self.scroll_area)
        
        layout.addWidget(self.content_area)
        
        # 加载现有笔记
        self.load_notes()
    
    def create_title_bar(self):
        """创建自定义标题栏"""
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(30)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(5, 0, 5, 0)
        
        # 标题
        title_label = QLabel(config.WINDOW_TITLE)
        title_label.setFont(QFont(config.FONT_FAMILY, 10, QFont.Bold))
        
        # 按钮
        self.minimize_btn = QPushButton("_")
        self.minimize_btn.setFixedSize(20, 20)
        self.minimize_btn.clicked.connect(self.toggle_minimize)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.hide_to_tray)
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.minimize_btn)
        layout.addWidget(close_btn)
        
        return title_bar
    
    def setup_tray(self):
        """设置系统托盘"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "系统托盘", "系统不支持托盘功能")
            return
        
        self.tray_icon = QSystemTrayIcon(self)
        # 这里可以设置托盘图标
        # self.tray_icon.setIcon(QIcon("assets/icons/app.png"))
        
        tray_menu = QMenu()
        
        show_action = QAction("显示/隐藏", self)
        show_action.triggered.connect(self.toggle_visibility)
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def setup_timer(self):
        """设置定时器检查提醒"""
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_reminders)
        self.check_timer.start(config.CHECK_INTERVAL)
    
    def apply_styles(self):
        """应用样式"""
        style_sheet = f"""
            #CentralWidget {{
                background: {config.BACKGROUND_COLOR};
                border-radius: {config.BORDER_RADIUS}px;
                border: 1px solid #E0E0E0;
            }}
            #TitleBar {{
                background: transparent;
                border-bottom: 1px solid #DDDDDD;
            }}
            #ContentArea {{
                background: transparent;
            }}
            QPushButton {{
                font-family: {config.FONT_FAMILY};
                font-size: 12px;
            }}
            QPushButton#add_note_btn {{
                background: rgba(255, 255, 255, 150);
                border: 1px dashed #CCCCCC;
                border-radius: 5px;
                padding: 8px;
            }}
            QPushButton#add_note_btn:hover {{
                background: rgba(255, 255, 255, 200);
                border-color: #999999;
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: rgba(255, 255, 255, 100);
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(0, 0, 0, 100);
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: rgba(0, 0, 0, 150);
            }}
        """
        self.setStyleSheet(style_sheet)
    
    def load_notes(self):
        """加载并显示笔记"""
        # 清空现有笔记组件
        for i in reversed(range(self.notes_layout.count())):
            widget = self.notes_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # 添加待处理笔记
        pending_notes = note_manager.get_pending_notes()
        for note in pending_notes:
            note_widget = NoteWidget(note)
            note_widget.deleted.connect(self.on_note_deleted)
            note_widget.completed.connect(self.on_note_completed)
            self.notes_layout.addWidget(note_widget)
    
    def add_new_note(self):
        """添加新笔记"""
        from datetime import datetime, timedelta
        default_time = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=1)
        
        new_note = note_manager.add_note(
            content="新提醒...",
            due_date=default_time,
            repeat_type=RepeatType.NONE
        )
        
        note_widget = NoteWidget(new_note)
        note_widget.deleted.connect(self.on_note_deleted)
        note_widget.completed.connect(self.on_note_completed)
        self.notes_layout.addWidget(note_widget)
    
    def on_note_deleted(self, note_id):
        """处理笔记删除"""
        note_manager.delete_note(note_id)
        self.load_notes()  # 重新加载
    
    def on_note_completed(self, note_id):
        """处理笔记完成"""
        note_manager.mark_completed(note_id)
        self.load_notes()  # 重新加载
    
    def toggle_minimize(self):
        """切换最小化模式"""
        if self.is_minimized:
            # 恢复
            self.setFixedSize(*config.WINDOW_SIZE)
            self.content_area.show()
            self.is_minimized = False
        else:
            # 最小化
            self.setFixedSize(config.WINDOW_SIZE[0], config.MINIMIZED_HEIGHT)
            self.content_area.hide()
            self.is_minimized = True
    
    def toggle_visibility(self):
        """切换窗口显示/隐藏"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()
    
    def hide_to_tray(self):
        """隐藏到系统托盘"""
        self.hide()
    
    def tray_icon_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_visibility()
    
    def check_reminders(self):
        """检查提醒"""
        due_notes = note_manager.get_due_notes()
        for note in due_notes:
            # 这里可以实现提醒效果，比如闪烁、系统通知等
            self.tray_icon.showMessage(
                "便签提醒",
                note.content,
                QSystemTrayIcon.Information,
                3000
            )
    
    def quit_application(self):
        """退出应用"""
        self.tray_icon.hide()
        QApplication.quit()
    
    def mousePressEvent(self, event):
        """鼠标按下事件，实现拖动"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，实现拖动"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()