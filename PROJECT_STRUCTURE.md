# 项目结构说明文档

本文档详细说明了 Python 文件管理工具集（Python File Management Toolkit）中每个文件和文件夹的用途。

## 📂 根目录 (Root Directory)

### 核心程序入口
- **`main.py`**: **文件整理程序**的主入口文件。运行此文件将启动文件整理工具（默认启动 GUI 界面）。
- **`search_main.py`**: **文件搜索程序**的主入口文件。运行此文件将启动文件搜索专家工具。

### 构建与打包脚本
- **`build_suite.py`**: 自动化构建脚本（基于 PyInstaller）。用于在 Python 3.12 等稳定环境中一键生成单文件 `.exe`。
- **`setup_cx.py`**: 替代构建脚本（基于 cx_Freeze）。专为 Python 3.14 等预览版环境设计，生成包含依赖的文件夹。
- **`setup.iss`**: Inno Setup 脚本文件。用于将 `dist/` 目录下的可执行文件打包成标准的 Windows 安装程序 (`setup.exe`)。
- **`FileOrganizer.spec`**: PyInstaller 生成的文件整理程序打包配置文件。
- **`FileSearchPro.spec`**: PyInstaller 生成的文件搜索程序打包配置文件。
- **`build_search_app.py`**: (旧) 仅用于构建搜索程序的脚本，现已被 `build_suite.py` 取代。

### 配置文件与文档
- **`config.json`**: 用户的运行时配置文件。存储了自定义整理规则、API 密钥（如有）等设置。程序运行时会自动生成。
- **`config.sample.json`**: 配置文件模板。提供了默认的分类规则示例，供用户参考或重置配置。
- **`requirements.txt`**: 项目依赖列表。列出了项目运行和开发所需的 Python 库（如 `cx_Freeze`, `pyinstaller` 等）。
- **`README.md`**: 项目主文档。包含项目简介、安装指南、快速开始和打包说明。
- **`USER_MANUAL.md`**: 详细用户手册。包含完整的功能介绍和操作指南。
- **`BUILD_INSTRUCTIONS.md`**: 构建指南。详细说明了如何从源码编译本项目。

### 运行时数据
- **`organizer.log`**: 程序运行日志文件。记录了所有的文件操作、错误信息和调试信息。
- **`undo_log.json`**: 撤销操作记录文件。存储了最近的文件移动记录，用于实现“撤销”功能。

## 📂 src/ (源代码目录)

这是项目的核心代码库，包含了所有功能模块的实现。

### 通用模块
- **`config.py`**: **配置管理模块**。负责加载、保存 `config.json`，并提供默认配置。
- **`logger.py`**: **日志与历史模块**。封装了 `logging` 库，并实现了基于 JSON 的撤销记录管理。

### 文件整理模块 (File Organizer)
- **`classifier.py`**: **文件分类器**。实现了三级分类逻辑：特殊文件优先 > 关键字匹配 > 扩展名匹配。
- **`organizer.py`**: **整理核心引擎**。执行非递归文件扫描（跳过子目录）、文件移动、重命名和去重操作。
- **`gui.py`**: **整理工具 GUI**。使用 Tkinter 构建的现代化图形界面，包含主控板、规则配置和日志显示。
- **`ui.py`**: **命令行界面 (CLI)**。提供基于文本终端的交互方式（作为 GUI 的备用或调试接口）。

### 文件搜索模块 (File Search Pro)
- **`searcher.py`**: **搜索核心引擎**。实现了多线程文件扫描、递归目录遍历和文件内容搜索算法。
- **`search_ui.py`**: **搜索工具 GUI**。独立的搜索界面，提供关键字输入、类型筛选、结果预览等功能。

## 📂 tests/ (测试目录)

包含自动化单元测试，用于确保代码质量。

- **`test_all.py`**: 测试套件入口，可运行所有测试。
- **`test_classifier.py`**: 测试文件分类逻辑准确性。
- **`test_config.py`**: 测试配置加载与保存功能。
- **`test_logger.py`**: 测试日志记录与撤销功能。
- **`test_organizer.py`**: 测试文件移动、重名处理等核心逻辑。
- **`test_requirements_v2.py`**: **新功能测试**。验证非递归扫描、特殊文件（快捷方式/应用）分类规则。

## 📂 辅助目录

- **`venv_312/`**: **Python 3.12 虚拟环境**。包含一个独立的 Python 运行环境，用于解决 Python 3.14 的打包兼容性问题。
- **`dist/`**: **发布目录**。构建成功后的 `.exe` 可执行文件会存放在这里。
- **`build/`**: **构建中间目录**。PyInstaller 或 cx_Freeze 在打包过程中生成的临时文件，通常可以忽略或清理。
