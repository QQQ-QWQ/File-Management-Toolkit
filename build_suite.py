import os
import subprocess
import sys
import shutil

def install_requirements():
    print("Installing requirements...")
    # Ensure pyinstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def clean_build_dirs():
    """Clean up build artifacts."""
    for d in ["build", "dist"]:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    for f in os.listdir("."):
        if f.endswith(".spec"):
            os.remove(f)

def build_app(script_name, app_name, hidden_imports=None, console=False):
    print(f"Building {app_name}...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--name", app_name,
        "--clean"
    ]
    
    if not console:
        cmd.append("--windowed")
        
    if hidden_imports:
        for imp in hidden_imports:
            cmd.extend(["--hidden-import", imp])
            
    # Add source directory to collection
    cmd.extend(["--collect-all", "src"])
    
    cmd.append(script_name)
    
    # Environment for PyInstaller 6.x
    env = os.environ.copy()
    env["PYINSTALLER_CONFIG_DIR"] = os.path.join(os.getcwd(), "build_config")

    try:
        subprocess.check_call(cmd, env=env)
        print(f"Successfully built {app_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to build {app_name}: {e}")
        raise e

def main():
    try:
        install_requirements()
        clean_build_dirs()
        
        # Build File Organizer
        build_app(
            "main.py", 
            "FileOrganizer", 
            hidden_imports=["tkinter", "pathlib", "json", "logging"],
            console=False 
        )
        
        # Build File Search Pro
        build_app(
            "search_main.py", 
            "FileSearchPro", 
            hidden_imports=["tkinter", "pathlib", "queue", "datetime"],
            console=False
        )
        
        print("\nBuild Suite Complete!")
        print("Executables are in the 'dist' folder:")
        print(f" - dist/FileOrganizer.exe")
        print(f" - dist/FileSearchPro.exe")
        
    except Exception as e:
        print(f"\nBuild Suite Failed: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
