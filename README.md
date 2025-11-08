# 📝 Desktop Sticky Notes - 桌面便签

一个简洁美观的桌面便签应用，支持提醒功能和系统托盘常驻。

![版本](https://img.shields.io/badge/版本-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.13+-green)
![许可证](https://img.shields.io/badge/许可证-MIT-yellow)
![平台](https://img.shields.io/badge/平台-Windows-lightgrey)

## ✨ 特性

- 🖥️ **桌面置顶** - 窗口始终显示在最前端
- 📌 **智能提醒** - 支持定时提醒和重复任务
- 🎯 **简洁界面** - 半透明设计，不干扰工作
- 🔄 **重复任务** - 支持每日、工作日、每周等重复模式
- 📂 **系统托盘** - 最小化到托盘，不占用任务栏
- 💾 **数据持久化** - 自动保存，重启后数据不丢失
- 🎨 **自定义样式** - 支持背景色、字体等个性化设置

## 🚀 快速开始

### 方法一：使用预编译版本（推荐）

1. 从 [Releases](https://github.com/rlyhtpzzu/DesktopStickyNotes/releases) 页面下载最新版本的 `DesktopStickyNotes.exe`
2. 直接双击运行即可使用

### 方法二：从源码运行

#### 环境要求
- Python 3.8+
- Windows 10/11

#### 安装步骤

1. **下载项目**
   ```bash
   git clone https://github.com/rlyhtpzzu/DesktopStickyNotes.git
   cd DesktopStickyNotes
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   python main.py
   ```

## 📖 使用说明

### 基本操作

1. **添加便签**：点击 "+ 添加新便签" 按钮
2. **设置提醒**：选择日期、时间和重复规则
3. **完成任务**：点击圆圈按钮标记完成
4. **删除便签**：点击 × 按钮删除
5. **最小化**：点击标题栏的 _ 按钮隐藏内容
6. **隐藏到托盘**：点击 × 按钮隐藏到系统托盘

### 重复规则

- **不重复**：单次提醒
- **每天**：每天同一时间提醒
- **每个工作日**：周一至周五提醒
- **每周**：每周同一天提醒
- **每月**：每月同一天提醒

### 系统托盘

- **双击托盘图标**：显示/隐藏主窗口
- **右键托盘图标**：显示菜单选项
- **提醒通知**：到期任务会在系统通知中显示

## 🛠️ 项目结构

```
DesktopStickyNotes/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── note_manager.py        # 笔记管理核心逻辑
├── widgets/               # 界面组件
│   ├── main_window.py     # 主窗口
│   ├── note_widget.py     # 单个笔记组件
│   └── time_picker.py     # 时间选择组件
├── assets/                # 图片资源
│   └── icons/             # 应用图标
├── data/                  # 数据存储
│   └── notes.json         # 笔记数据
├── requirements.txt       # Python依赖
└── README.md             # 项目说明
```

## 🔧 开发指南

### 自定义配置

在 `config.py` 中可以修改以下配置：

```python
# 窗口大小
WINDOW_SIZE = (300, 400)

# 背景颜色（RGBA）
BACKGROUND_COLOR = "rgba(255, 253, 231, 230)"

# 字体设置
FONT_FAMILY = "Microsoft YaHei, SimHei, sans-serif"
```

### 打包为可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包应用
pyinstaller --name="DesktopStickyNotes" --windowed --onefile main.py
```

## 📝 更新日志

### v1.0.0 (2024-01-15)
- ✅ 基础便签功能
- ✅ 提醒和重复任务
- ✅ 系统托盘支持
- ✅ 数据持久化存储

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🐛 问题反馈

如果你遇到任何问题，请：

1. 查看 [Issues](https://github.com/rlyhtpzzu/DesktopStickyNotes/issues) 是否已有类似问题
2. 创建新 Issue，详细描述问题和复现步骤

## 🙏 致谢

感谢以下开源项目：
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI框架
- [PyInstaller](https://www.pyinstaller.org/) - 应用打包工具

---

**⭐ 如果这个项目对你有帮助，请给我们一个 Star！**
