# File Search Pro - Build & Deployment Guide

This guide explains how to package the File Search Pro application into a standalone executable for Windows, macOS, and Linux.

## Prerequisites

- Python 3.8+ installed
- `pip` package manager

## Quick Build (Windows/Mac/Linux)

We have provided a build script `build_search_app.py` that automates the process using `PyInstaller`.

1. Open your terminal/command prompt.
2. Navigate to the project root.
3. Run the build script:

```bash
python build_search_app.py
```

This will:
1. Install `pyinstaller` if not present.
2. Clean previous builds.
3. Generate a single executable file in the `dist/` folder.

## Manual Build Instructions

If you prefer to run the commands manually or need to customize the build:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Run PyInstaller

**Windows:**
```bash
pyinstaller --noconfirm --onefile --windowed --name "FileSearchPro" --icon "icon.ico" search_main.py
```
*(Note: You need to provide an `icon.ico` file for the icon to appear)*

**macOS:**
```bash
pyinstaller --noconfirm --onefile --windowed --name "FileSearchPro" --icon "icon.icns" search_main.py
```

**Linux:**
```bash
pyinstaller --noconfirm --onefile --windowed --name "FileSearchPro" search_main.py
```

## Creating an Installer (MSI/DMG/DEB)

For a professional distribution, you can wrap the executable in an installer.

### Windows (MSI/EXE)
- **Tool**: Inno Setup (Recommended) or NSIS.
- **Steps**:
    1. Download Inno Setup.
    2. Create a new script using the wizard.
    3. Point the "Application Main Executable" to `dist/FileSearchPro.exe`.
    4. Compile to get a `setup.exe`.

### macOS (DMG)
- **Tool**: `create-dmg` (Node.js tool) or Disk Utility.
- **Steps**:
    1. Create a folder named `Installer`.
    2. Copy `dist/FileSearchPro.app` into it.
    3. Create a link to `/Applications`.
    4. Use `hdiutil` to create a DMG.

### Linux (DEB/RPM)
- **Tool**: `fpm` (Ruby gem).
- **Steps**:
    ```bash
    fpm -s dir -t deb -n filesearchpro -v 1.0.0 --prefix /usr/local/bin dist/FileSearchPro
    ```

## Auto-Update Mechanism

To implement auto-updates:
1. Host a `version.json` and the latest binary on a static server (e.g., GitHub Releases, AWS S3).
2. On app startup, fetch `version.json` and compare with local version.
3. If newer, download the binary to a temp location and swap it (requires restart).
   - *Note: For Windows, you often need a separate "updater.exe" to handle the file swapping while the main app is closed.*

## Troubleshooting

- **Missing DLLs**: If the app fails to start, check if Visual C++ Redistributable is installed on the target machine.
- **Antivirus**: Unsigned executables might be flagged. You need a Code Signing Certificate (e.g., from Sectigo or DigiCert) to sign your EXE/App.
