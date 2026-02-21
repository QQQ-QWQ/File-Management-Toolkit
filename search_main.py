import tkinter as tk
import sys
from src.search_ui import ModernSearchUI

def main():
    root = tk.Tk()
    
    # Try to set icon if exists
    try:
        if sys.platform.startswith('win'):
            root.iconbitmap('icon.ico')
    except:
        pass
        
    app = ModernSearchUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
