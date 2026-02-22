import argparse
import sys
import time
from pathlib import Path
from .organizer import FileOrganizer
from .config import ConfigManager
from .logger import OperationLogger

class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Python 文件整理器")
        self.parser.add_argument("path", nargs="?", help="要整理的目标目录")
        self.parser.add_argument("--interactive", "-i", action="store_true", help="以交互模式运行")
        self.parser.add_argument("--undo", "-u", action="store_true", help="撤销上一步操作")
        self.parser.add_argument("--config", "-c", default="config.json", help="配置文件路径")

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
            print("\n=== 文件整理器菜单 ===")
            print("1. 整理文件夹")
            print("2. 添加关键字规则")
            print("3. 添加文件类型规则")
            print("4. 撤销上一步操作")
            print("5. 退出")
            
            choice = input("请选择一个选项: ")
            
            if choice == "1":
                path = input("请输入文件夹路径: ")
                self.organize_folder(path)
            elif choice == "2":
                self.add_keyword_rule()
            elif choice == "3":
                self.add_file_type_rule()
            elif choice == "4":
                self.undo_operation()
            elif choice == "5":
                print("正在退出...")
                sys.exit(0)
            else:
                print("无效选项，请重试。")

    def organize_folder(self, path: str):
        print(f"正在扫描目录: {path}...")
        try:
            organizer = FileOrganizer(path)
            
            def progress_callback(current, total):
                percent = (current / total) * 100
                bar_length = 40
                filled_length = int(bar_length * current // total)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                sys.stdout.write(f'\r进度: |{bar}| {percent:.1f}% ({current}/{total})')
                sys.stdout.flush()

            print("开始整理...")
            organizer.organize(progress_callback)
            print("\n整理完成！")
            
        except Exception as e:
            print(f"\n错误: {e}")

    def add_keyword_rule(self):
        keyword = input("请输入关键字: ")
        folder = input("请输入文件夹名称: ")
        config = ConfigManager()
        config.add_keyword_rule(keyword, folder)
        print(f"规则已添加: 包含 '{keyword}' 的文件将移动到 '{folder}'")

    def add_file_type_rule(self):
        ext = input("请输入文件扩展名 (如 mp4): ")
        category = input("请输入类别 (如 Videos): ")
        config = ConfigManager()
        config.add_file_type_rule(category, ext)
        print(f"规则已添加: .{ext} 文件将移动到 '{category}'")

    def undo_operation(self):
        logger = OperationLogger()
        if logger.undo_last_operation():
            print("撤销成功。")
        else:
            print("撤销失败或没有可撤销的操作。")

if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.run()
