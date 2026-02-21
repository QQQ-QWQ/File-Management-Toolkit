# Python 文件管理工具集 (File Management Toolkit)

本项目包含两个强大的桌面应用程序，旨在全方位提升您的文件管理效率：

1.  **智能文件整理程序 (File Organizer)**：自动分类整理杂乱文件，支持自定义规则和撤销操作。
2.  **文件搜索专家 (File Search Pro)**：快速查找文件及内容，支持实时预览和结果导出。

---

## 1. 智能文件整理程序 (File Organizer)

基于 Python 的智能文件整理工具，能够根据文件类型和关键字自动将文件归类到相应的文件夹中。

### 核心功能
*   **自动分类**：识别文档、图片、视频、音频、压缩包等多种文件类型。
*   **可视化界面**：提供现代化的深色主题 GUI，操作直观便捷。
*   **关键字规则**：支持按文件名关键字创建专用文件夹（如包含 "invoice" 的文件 -> "Invoices"）。
*   **安全整理**：自动处理重名文件（自动重命名），并支持**一键撤销**上一次操作。
*   **自定义配置**：用户可自由添加文件类型和关键字规则。

### 使用方法

#### 启动图形界面 (推荐)
直接运行主程序即可启动 GUI：
```bash
python main.py
```
在界面中选择目标文件夹，点击 "START ORGANIZE" 即可开始整理。

#### 命令行模式 (CLI)
如果您偏好命令行操作，可以添加参数运行：
```bash
# 启动交互式命令行菜单
python main.py -i

# 直接整理指定文件夹
python main.py "C:\Path\To\Your\Folder"
```

---

## 2. 文件搜索专家 (File Search Pro)

一个现代化、高性能的本地文件搜索工具，提供比系统自带搜索更灵活的选项。

### 核心功能
*   **多维搜索**：支持同时按**路径**、**关键字**、**文件扩展名**进行过滤。
*   **内容搜索**：支持深入文本文件内容进行搜索（智能跳过大文件）。
*   **实时预览**：点击搜索结果，即可在右侧面板**实时预览**文本内容。
*   **结果导出**：支持将搜索结果导出为 CSV 表格文件。
*   **历史记录**：自动保存最近使用的搜索关键字。

### 使用方法

启动搜索程序：
```bash
python search_main.py
```
或者，如果您已经使用 `build_search_app.py` 进行了打包，可以直接运行 `dist/FileSearchPro.exe`。

---

## 安装与依赖

本项目主要依赖 Python 标准库和 `tkinter` (通常随 Python 安装)。

1.  确保已安装 Python 3.6 或更高版本。
2.  克隆或下载本项目代码。
3.  如果需要打包为独立 EXE 文件，请安装 `pyinstaller`：
    ```bash
    pip install pyinstaller
    ```

## 构建与打包 (exe安装包)

本项目提供了自动化构建脚本，可将 Python 源码打包为独立的 Windows 可执行文件 (.exe)，并支持生成安装包。

### 1. 编译可执行文件

本项目支持两种打包方式：

#### 方式 A: 使用 cx_Freeze (推荐，支持 Python 3.14+)
由于 PyInstaller 对 Python 3.14 预览版支持尚不完善，我们推荐使用 `cx_Freeze` 进行打包。

```bash
# 1. 安装 cx_Freeze
pip install cx_Freeze

# 2. 运行构建命令
python setup_cx.py build
```
构建成功后，可执行文件将位于 `build/exe.win-amd64-3.14/` 目录下（目录名可能因系统而异）。您需要将整个文件夹分发给用户。

#### 方式 B: 使用 PyInstaller (仅限 Python 3.13 及以下)
如果您使用的是稳定版 Python，可以使用单文件打包方案：

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 运行构建脚本
python build_suite.py
```

构建成功后，在 `dist` 目录下会生成单文件 exe。

### 2. 生成安装包 (Installer)

如果您希望生成类似 `Setup.exe` 的安装程序，请按照以下步骤操作：

1.  确保已完成上述 "编译可执行文件" 步骤，且 `dist` 目录下存在生成的 exe 文件。
2.  下载并安装 [Inno Setup](https://jrsoftware.org/isdl.php) (Windows 下流行的免费安装制作工具)。
3.  双击运行项目根目录下的 `setup.iss` 脚本。
4.  在 Inno Setup 编译器中点击 "Compile" (或按 F9)。
5.  编译完成后，会在 `installer_output` 目录下生成最终的安装包 `FileManagementSuite_Setup.exe`。

**注意**：由于 Python 版本兼容性问题，建议使用 Python 3.12 或 3.13 版本进行打包。Python 3.14 (预览版) 可能与 PyInstaller 存在兼容性问题。

## 配置文件 (config.json)

整理程序首次运行会自动生成 `config.json`，用于存储您的自定义规则：

```json
{
    "special_types": {
        "Shortcuts": ["lnk", "url", "desktop"],
        "Applications": ["exe", "msi", "dmg", "app"]
    },
    "file_types": {
        "Documents": ["pdf", "docx", "txt"],
        "Images": ["jpg", "png"]
    },
    "keywords": {
        "project": "ProjectFiles"
    },
    "exclude_dirs": [".git", "venv", "__pycache__"]
}
```

## 开发与测试

运行单元测试以验证核心功能：

```bash
python -m unittest discover tests
```

## 贡献

欢迎提交 Issue 或 Pull Request 来改进本项目！
