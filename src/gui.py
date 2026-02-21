import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import os
from typing import Dict, List, Any
from .config import ConfigManager
from .organizer import FileOrganizer
from .logger import OperationLogger

class ModernGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python 智能文件整理器")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.organizer = None
        
        # Styling
        self._setup_styles()
        
        # Layout
        self._create_layout()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' as base for better customization
        
        # Colors
        self.colors = {
            "bg_dark": "#2E3440",
            "bg_light": "#3B4252",
            "fg_primary": "#ECEFF4",
            "accent": "#88C0D0",
            "accent_hover": "#81A1C1",
            "success": "#A3BE8C",
            "warning": "#EBCB8B",
            "error": "#BF616A"
        }
        
        # Configure root background
        self.root.configure(bg=self.colors["bg_dark"])
        
        # General Frame Style
        self.style.configure("TFrame", background=self.colors["bg_dark"])
        self.style.configure("Card.TFrame", background=self.colors["bg_light"], relief="flat")
        
        # Label Style
        self.style.configure("TLabel", background=self.colors["bg_dark"], foreground=self.colors["fg_primary"], font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background=self.colors["bg_dark"], foreground=self.colors["accent"])
        self.style.configure("CardHeader.TLabel", font=("Segoe UI", 12, "bold"), background=self.colors["bg_light"], foreground=self.colors["accent"])
        self.style.configure("Card.TLabel", background=self.colors["bg_light"], foreground=self.colors["fg_primary"])
        
        # Button Style
        self.style.configure("TButton", 
                             font=("Segoe UI", 10), 
                             background=self.colors["accent"], 
                             foreground=self.colors["bg_dark"], 
                             borderwidth=0, 
                             focuscolor=self.colors["accent_hover"])
        self.style.map("TButton", 
                       background=[('active', self.colors["accent_hover"]), ('disabled', '#4C566A')],
                       foreground=[('disabled', '#D8DEE9')])
        
        self.style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), padding=10)
        
        # Entry Style
        self.style.configure("TEntry", fieldbackground=self.colors["bg_light"], foreground=self.colors["fg_primary"], insertcolor=self.colors["fg_primary"], borderwidth=0)
        
        # Notebook (Tabs) Style
        self.style.configure("TNotebook", background=self.colors["bg_dark"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.colors["bg_light"], foreground=self.colors["fg_primary"], padding=[15, 5], font=("Segoe UI", 10))
        self.style.map("TNotebook.Tab", background=[('selected', self.colors["accent"])], foreground=[('selected', self.colors["bg_dark"])])

        # Progressbar
        self.style.configure("Horizontal.TProgressbar", background=self.colors["success"], troughcolor=self.colors["bg_light"], borderwidth=0)

        # Treeview
        self.style.configure("Treeview", 
                             background=self.colors["bg_light"], 
                             foreground=self.colors["fg_primary"], 
                             fieldbackground=self.colors["bg_light"],
                             font=("Segoe UI", 10),
                             rowheight=25)
        self.style.configure("Treeview.Heading", background=self.colors["bg_dark"], foreground=self.colors["fg_primary"], font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[('selected', self.colors["accent"])], foreground=[('selected', self.colors["bg_dark"])])

    def _create_layout(self):
        # Main Container with Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Dashboard
        self.tab_dashboard = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_dashboard, text="仪表盘")
        self._build_dashboard(self.tab_dashboard)
        
        # Tab 2: Rules (Keywords)
        self.tab_keywords = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_keywords, text="关键字规则")
        self._build_keyword_rules(self.tab_keywords)
        
        # Tab 3: Rules (File Types)
        self.tab_filetypes = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_filetypes, text="文件类型规则")
        self._build_filetype_rules(self.tab_filetypes)

        # Tab 4: Settings
        self.tab_settings = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_settings, text="设置")
        self._build_settings(self.tab_settings)

    def _build_dashboard(self, parent):
        # Header
        header_frame = ttk.Frame(parent, style="TFrame")
        header_frame.pack(fill="x", pady=(20, 20), padx=20)
        ttk.Label(header_frame, text="文件整理仪表盘", style="Header.TLabel").pack(side="left")

        # Path Selection Card
        card_path = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card_path.pack(fill="x", padx=20, pady=(0, 20))
        
        ttk.Label(card_path, text="目标目录", style="CardHeader.TLabel").pack(anchor="w", pady=(0, 10))
        
        path_frame = ttk.Frame(card_path, style="Card.TFrame")
        path_frame.pack(fill="x")
        
        self.path_var = tk.StringVar()
        self.entry_path = ttk.Entry(path_frame, textvariable=self.path_var, font=("Segoe UI", 10))
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(path_frame, text="浏览...", command=self._browse_folder).pack(side="right")

        # Actions Card
        card_actions = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card_actions.pack(fill="x", padx=20, pady=(0, 20))
        
        ttk.Label(card_actions, text="操作", style="CardHeader.TLabel").pack(anchor="w", pady=(0, 10))
        
        action_btn_frame = ttk.Frame(card_actions, style="Card.TFrame")
        action_btn_frame.pack(fill="x")
        
        self.btn_organize = ttk.Button(action_btn_frame, text="开始整理", style="Action.TButton", command=self._start_organize)
        self.btn_organize.pack(side="left", padx=(0, 10))
        
        self.btn_undo = ttk.Button(action_btn_frame, text="撤销上一步", style="Action.TButton", command=self._undo_action)
        self.btn_undo.pack(side="left")

        # Progress Section
        card_progress = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card_progress.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(card_progress, text="状态与日志", style="CardHeader.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(card_progress, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        self.status_label = ttk.Label(card_progress, text="就绪", style="Card.TLabel")
        self.status_label.pack(anchor="w", pady=(0, 5))
        
        # Log Output
        log_frame = ttk.Frame(card_progress, style="Card.TFrame")
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, height=10, bg=self.colors["bg_dark"], fg=self.colors["fg_primary"], 
                                insertbackground=self.colors["fg_primary"], borderwidth=0, font=("Consolas", 9))
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def _build_keyword_rules(self, parent):
        # Input Area
        input_frame = ttk.Frame(parent, style="TFrame", padding=20)
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="新建关键字规则", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        grid_frame = ttk.Frame(input_frame, style="TFrame")
        grid_frame.pack(fill="x")
        
        ttk.Label(grid_frame, text="关键字 (如 'invoice'):").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(grid_frame, text="文件夹名 (如 'Financial'):").grid(row=0, column=1, sticky="w", padx=5)
        
        self.kw_entry = ttk.Entry(grid_frame)
        self.kw_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.folder_entry = ttk.Entry(grid_frame)
        self.folder_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Button(grid_frame, text="添加规则", command=self._add_keyword_rule).grid(row=1, column=2, padx=5, pady=5)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # List Area
        list_frame = ttk.Frame(parent, style="TFrame", padding=20)
        list_frame.pack(fill="both", expand=True)
        
        ttk.Label(list_frame, text="现有规则", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        columns = ("keyword", "folder")
        self.kw_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.kw_tree.heading("keyword", text="关键字")
        self.kw_tree.heading("folder", text="目标文件夹")
        self.kw_tree.pack(fill="both", expand=True)
        
        ttk.Button(list_frame, text="删除选中", command=self._delete_keyword_rule).pack(pady=10)
        
        self._refresh_keyword_list()

    def _build_filetype_rules(self, parent):
        # Similar to keyword rules but for extensions
        input_frame = ttk.Frame(parent, style="TFrame", padding=20)
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="新建文件类型规则", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        grid_frame = ttk.Frame(input_frame, style="TFrame")
        grid_frame.pack(fill="x")
        
        ttk.Label(grid_frame, text="扩展名 (如 'psd'):").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(grid_frame, text="类别 (如 'Design'):").grid(row=0, column=1, sticky="w", padx=5)
        
        self.ext_entry = ttk.Entry(grid_frame)
        self.ext_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.cat_entry = ttk.Entry(grid_frame)
        self.cat_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Button(grid_frame, text="添加规则", command=self._add_filetype_rule).grid(row=1, column=2, padx=5, pady=5)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # List Area
        list_frame = ttk.Frame(parent, style="TFrame", padding=20)
        list_frame.pack(fill="both", expand=True)
        
        ttk.Label(list_frame, text="现有扩展名", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        columns = ("extension", "category")
        self.ft_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.ft_tree.heading("extension", text="扩展名")
        self.ft_tree.heading("category", text="类别")
        self.ft_tree.pack(fill="both", expand=True)
        
        ttk.Button(list_frame, text="删除选中", command=self._delete_filetype_rule).pack(pady=10)
        
        self._refresh_filetype_list()

    def _build_settings(self, parent):
        # Exclude Dirs
        frame = ttk.Frame(parent, style="TFrame", padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="排除的目录", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.exclude_text = tk.Text(frame, height=10, bg=self.colors["bg_light"], fg=self.colors["fg_primary"], 
                                    insertbackground=self.colors["fg_primary"], borderwidth=0, font=("Consolas", 10))
        self.exclude_text.pack(fill="x", pady=(0, 10))
        self.exclude_text.insert("1.0", ", ".join(self.config.get("exclude_dirs", [])))
        
        ttk.Label(frame, text="用逗号分隔 (如 .git, venv, temp)", style="TLabel").pack(anchor="w")
        
        ttk.Button(frame, text="保存设置", command=self._save_settings).pack(pady=20)

    # Logic Implementation
    def _browse_folder(self):
        folder_selected = filedialog.askdirectory(title="选择要整理的目录")
        if folder_selected:
            self.path_var.set(folder_selected)

    def _log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def _start_organize(self):
        path = self.path_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("错误", "请选择有效的目录。")
            return

        self.btn_organize.config(state="disabled")
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        self._log(f"开始整理目录: {path}")

        def run_task():
            try:
                self.organizer = FileOrganizer(path)
                
                def progress_callback(current, total):
                    progress = (current / total) * 100
                    # Use after to update GUI from thread
                    self.root.after(0, lambda: self.progress_var.set(progress))
                    self.root.after(0, lambda: self.status_label.config(text=f"处理中: {current}/{total}"))

                self.organizer.organize(progress_callback)
                
                self.root.after(0, lambda: self._log("整理完成！"))
                self.root.after(0, lambda: messagebox.showinfo("成功", "文件整理完成！"))
                
            except Exception as e:
                self.root.after(0, lambda: self._log(f"错误: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("错误", str(e)))
            finally:
                self.root.after(0, lambda: self.btn_organize.config(state="normal"))

        threading.Thread(target=run_task, daemon=True).start()

    def _undo_action(self):
        try:
            logger = OperationLogger()
            if logger.undo_last_operation():
                self._log("撤销成功。")
                messagebox.showinfo("撤销", "上一步操作已成功撤销。")
            else:
                self._log("撤销失败或无可撤销操作。")
                messagebox.showwarning("撤销", "无可撤销操作或撤销失败。")
        except Exception as e:
            self._log(f"撤销错误: {e}")
            messagebox.showerror("错误", f"撤销失败: {e}")

    # Rule Management Logic
    def _refresh_keyword_list(self):
        for i in self.kw_tree.get_children():
            self.kw_tree.delete(i)
        
        # Reload config to ensure we have latest data
        self.config = self.config_manager.load_config()
        
        for kw, folder in self.config.get("keywords", {}).items():
            self.kw_tree.insert("", "end", values=(kw, folder))

    def _add_keyword_rule(self):
        kw = self.kw_entry.get().strip()
        folder = self.folder_entry.get().strip()
        if kw and folder:
            self.config_manager.add_keyword_rule(kw, folder)
            self._refresh_keyword_list()
            self.kw_entry.delete(0, tk.END)
            self.folder_entry.delete(0, tk.END)
            messagebox.showinfo("成功", f"规则已添加: '{kw}' -> '{folder}'")
        else:
            messagebox.showwarning("输入错误", "两个字段都必须填写。")

    def _delete_keyword_rule(self):
        selected = self.kw_tree.selection()
        if not selected:
            messagebox.showwarning("选择错误", "请选择要删除的规则。")
            return
            
        confirm = messagebox.askyesno("确认删除", "确定要删除选中的规则吗？")
        if not confirm:
            return

        for item in selected:
            kw = self.kw_tree.item(item)['values'][0]
            if kw in self.config["keywords"]:
                del self.config["keywords"][kw]
                
        self.config_manager.save_config(self.config)
        self._refresh_keyword_list()

    def _refresh_filetype_list(self):
        for i in self.ft_tree.get_children():
            self.ft_tree.delete(i)
        
        # Reload config
        self.config = self.config_manager.load_config()
        ext_map = self.config_manager.get_extension_map()
        
        # Sort by category for better view
        sorted_items = sorted(ext_map.items(), key=lambda x: x[1])
        for ext, cat in sorted_items:
            self.ft_tree.insert("", "end", values=(ext, cat))

    def _add_filetype_rule(self):
        ext = self.ext_entry.get().strip().lstrip(".")
        cat = self.cat_entry.get().strip()
        if ext and cat:
            self.config_manager.add_file_type_rule(cat, ext)
            self._refresh_filetype_list()
            self.ext_entry.delete(0, tk.END)
            self.cat_entry.delete(0, tk.END)
            messagebox.showinfo("成功", f"规则已添加: '.{ext}' -> '{cat}'")
        else:
            messagebox.showwarning("输入错误", "两个字段都必须填写。")

    def _delete_filetype_rule(self):
        selected = self.ft_tree.selection()
        if not selected:
            messagebox.showwarning("选择错误", "请选择要删除的规则。")
            return
        
        confirm = messagebox.askyesno("确认删除", "确定要删除选中的规则吗？")
        if not confirm:
            return

        # This is a bit complex because structure is {Category: [exts]}
        # We need to rebuild the structure
        items_to_remove = [] # List of (ext, cat)
        for item in selected:
            values = self.ft_tree.item(item)['values']
            items_to_remove.append((str(values[0]), str(values[1]))) # ext, cat
            
        for ext, cat in items_to_remove:
            if cat in self.config["file_types"]:
                # Ensure we are modifying the list in the config
                if ext in self.config["file_types"][cat]:
                    self.config["file_types"][cat].remove(ext)
                
                # Clean up empty categories if desired
                # if not self.config["file_types"][cat]:
                #     del self.config["file_types"][cat]
                    
        self.config_manager.save_config(self.config)
        self._refresh_filetype_list()

    def _save_settings(self):
        exclude_str = self.exclude_text.get("1.0", tk.END).strip()
        exclude_list = [x.strip() for x in exclude_str.split(",") if x.strip()]
        self.config["exclude_dirs"] = exclude_list
        self.config_manager.save_config(self.config)
        messagebox.showinfo("设置", "设置保存成功。")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()
