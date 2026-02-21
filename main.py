import tkinter as tk
from src.ui import CommandLineInterface
from src.gui import ModernGUI

if __name__ == "__main__":
    import sys
    
    # Check if run with arguments (CLI mode) or without (GUI mode)
    if len(sys.argv) > 1:
        cli = CommandLineInterface()
        cli.run()
    else:
        # Launch GUI
        root = tk.Tk()
        app = ModernGUI(root)
        root.mainloop()
