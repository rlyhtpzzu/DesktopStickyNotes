import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 现在导入其他模块
try:
    from config import config
    from note_manager import NoteManager, RepeatType
    from widgets.main_window import MainWindow
    from widgets.note_widget import NoteWidget
    from widgets.time_picker import TimePicker, CompactTimePicker
    print("所有模块导入成功！")
except ImportError as e:
    print(f"导入错误: {e}")
    print("当前目录:", current_dir)
    print("文件列表:", os.listdir(current_dir))
    if os.path.exists(os.path.join(current_dir, 'widgets')):
        print("widgets目录内容:", os.listdir(os.path.join(current_dir, 'widgets')))
    sys.exit(1)

def setup_environment():
    """设置应用环境"""
    # 在Windows上设置应用ID（用于任务栏分组）
    if sys.platform == "win32":
        try:
            myappid = 'desktop.stickynotes.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
    
    # 创建必要的目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("assets/icons", exist_ok=True)

def load_fonts():
    """加载字体（如果需要）"""
    pass

def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"未处理的异常: {exc_type.__name__}: {exc_value}")
    error_msg = f"发生了一个错误:\n\n{exc_type.__name__}: {exc_value}"
    QMessageBox.critical(None, "应用程序错误", error_msg)

def main():
    """主函数"""
    # 设置全局异常处理
    sys.excepthook = handle_exception
    
    # 设置环境
    setup_environment()
    
    # 创建QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("桌面便签")
    app.setApplicationDisplayName("桌面便签")
    app.setQuitOnLastWindowClosed(False)
    
    # 加载字体
    load_fonts()
    
    # 设置高DPI支持
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # 创建并显示主窗口
        print("正在创建主窗口...")
        window = MainWindow()
        window.show()
        
        print("桌面便签应用已启动！")
        print("使用说明:")
        print("- 点击标题栏的 '_' 按钮可以最小化窗口")
        print("- 点击 '×' 按钮可以隐藏到系统托盘")
        print("- 在系统托盘图标上双击可以显示/隐藏窗口")
        print("- 右键点击系统托盘图标可以退出应用")
        
        # 运行应用
        return app.exec_()
        
    except Exception as e:
        print(f"启动应用时发生错误: {e}")
        import traceback
        traceback.print_exc()
        QMessageBox.critical(None, "启动错误", f"无法启动应用:\n\n{str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)