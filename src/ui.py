import argparse
import sys
import time
from pathlib import Path
from .organizer import FileOrganizer
from .config import ConfigManager
from .logger import OperationLogger

class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Python File Organizer")
        self.parser.add_argument("path", nargs="?", help="Target directory to organize")
        self.parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
        self.parser.add_argument("--undo", "-u", action="store_true", help="Undo last operation")
        self.parser.add_argument("--config", "-c", default="config.json", help="Path to configuration file")

    def run(self):
        args = self.parser.parse_args()
        
        if args.interactive:
            self.interactive_menu()
        elif args.undo:
            self.undo_operation()
        elif args.path:
            self.organize_folder(args.path)
        else:
            self.parser.print_help()

    def interactive_menu(self):
        while True:
            print("\n=== File Organizer Menu ===")
            print("1. Organize a Folder")
            print("2. Add Keyword Rule")
            print("3. Add File Type Rule")
            print("4. Undo Last Operation")
            print("5. Exit")
            
            choice = input("Select an option: ")
            
            if choice == "1":
                path = input("Enter folder path: ")
                self.organize_folder(path)
            elif choice == "2":
                self.add_keyword_rule()
            elif choice == "3":
                self.add_file_type_rule()
            elif choice == "4":
                self.undo_operation()
            elif choice == "5":
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid option. Please try again.")

    def organize_folder(self, path: str):
        print(f"Scanning directory: {path}...")
        try:
            organizer = FileOrganizer(path)
            
            def progress_callback(current, total):
                percent = (current / total) * 100
                bar_length = 40
                filled_length = int(bar_length * current // total)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                sys.stdout.write(f'\rProgress: |{bar}| {percent:.1f}% ({current}/{total})')
                sys.stdout.flush()

            print("Starting organization...")
            organizer.organize(progress_callback)
            print("\nOrganization complete!")
            
        except Exception as e:
            print(f"\nError: {e}")

    def add_keyword_rule(self):
        keyword = input("Enter keyword: ")
        folder = input("Enter folder name: ")
        config = ConfigManager()
        config.add_keyword_rule(keyword, folder)
        print(f"Rule added: Files containing '{keyword}' will move to '{folder}'")

    def add_file_type_rule(self):
        ext = input("Enter file extension (e.g., mp4): ")
        category = input("Enter category (e.g., Videos): ")
        config = ConfigManager()
        config.add_file_type_rule(category, ext)
        print(f"Rule added: .{ext} files will move to '{category}'")

    def undo_operation(self):
        logger = OperationLogger()
        if logger.undo_last_operation():
            print("Undo successful.")
        else:
            print("Undo failed or nothing to undo.")

if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.run()
