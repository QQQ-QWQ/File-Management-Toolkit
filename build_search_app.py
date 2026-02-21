import os
import subprocess
import sys

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    print("Building executable...")
    
    # Clean previous build
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist")
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")

    # PyInstaller command
    # --onefile: Create a single executable
    # --windowed: No console window
    # --name: Name of the executable
    # --add-data: Add resources (if any, e.g., icons)
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "FileSearchPro",
        "--hidden-import", "tkinter",
        "--hidden-import", "pathlib",
        "--hidden-import", "queue",
        "--hidden-import", "datetime",
        "--collect-all", "src",
        "search_main.py"
    ]
    
    # Add environment variable to handle PyInstaller 6.x regex issue
    env = os.environ.copy()
    env["PYINSTALLER_CONFIG_DIR"] = os.path.join(os.getcwd(), "build_config")

    try:
        subprocess.check_call(cmd, env=env)
        print("Build complete! Check the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code {e.returncode}. Trying alternative configuration...")
        # Fallback: try without hidden imports if the first attempt fails, 
        # or try with specific --exclude-module if needed.
        # But for 'LOAD_FAST_BORROW', it's often an internal PyInstaller issue with Python 3.14 (or newer/beta versions).
        # We can try to use a different bootloader or just report the specific error.
        
        # Another common fix for "KeyError: 'LOAD_FAST_BORROW'" is upgrading pyinstaller or downgrading python.
        # Since we cannot easily change python version here, we might need to ensure pyinstaller supports 3.14.
        # Python 3.14 is very new (preview), PyInstaller might not fully support it yet.
        
        print("NOTE: You are using Python 3.14. PyInstaller might not fully support this version yet.")
        print("Please try running this script with Python 3.12 or 3.13 if possible.")
        raise e

if __name__ == "__main__":
    try:
        install_requirements()
        build_exe()
    except Exception as e:
        print(f"Build failed: {e}")
        input("Press Enter to exit...")
