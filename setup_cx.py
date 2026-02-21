import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["os", "json", "tkinter", "threading", "queue", "pathlib", "logging", "shutil", "datetime"],
    "excludes": [],
    "include_files": ["src"] # Include source files if needed for dynamic loading, though compiled is better
}

# Base for GUI applications
base = "gui" if sys.platform == "win32" else None

setup(
    name="Python File Management Toolkit",
    version="1.0",
    description="File Organizer and Search Tool",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("main.py", base=base, target_name="FileOrganizer.exe"),
        Executable("search_main.py", base=base, target_name="FileSearchPro.exe")
    ]
)
