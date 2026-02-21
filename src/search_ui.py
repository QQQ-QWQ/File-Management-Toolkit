import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import queue
from datetime import datetime
from .searcher import SearchEngine
from typing import List

class ModernSearchUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("文件搜索专家")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        self.search_engine = SearchEngine()
        self.result_queue = queue.Queue()
        self.is_searching = False
        
        self._setup_styles()
        self._create_layout()
        self._setup_result_processing()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color Palette (Dark Theme)
        self.colors = {
            "bg_dark": "#1E1E1E",       # Main background
            "bg_sidebar": "#252526",    # Sidebar/Header
            "bg_light": "#333333",      # Input fields/Cards
            "fg_primary": "#CCCCCC",    # Main text
            "fg_secondary": "#858585",  # Secondary text
            "accent": "#007ACC",        # Blue accent
            "accent_hover": "#0062A3",
            "border": "#3E3E42"
        }
        
        self.root.configure(bg=self.colors["bg_dark"])
        
        # General Styles
        self.style.configure("TFrame", background=self.colors["bg_dark"])
        self.style.configure("Sidebar.TFrame", background=self.colors["bg_sidebar"])
        self.style.configure("Card.TFrame", background=self.colors["bg_light"], relief="flat")
        
        # Label Styles
        self.style.configure("TLabel", background=self.colors["bg_dark"], foreground=self.colors["fg_primary"], font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background=self.colors["bg_sidebar"], foreground=self.colors["fg_primary"])
        self.style.configure("Sidebar.TLabel", background=self.colors["bg_sidebar"], foreground=self.colors["fg_primary"])
        
        # Button Styles
        self.style.configure("TButton", 
                             font=("Segoe UI", 9), 
                             background=self.colors["bg_light"], 
                             foreground=self.colors["fg_primary"], 
                             borderwidth=1, 
                             focuscolor=self.colors["border"])
        self.style.map("TButton", 
                       background=[('active', self.colors["border"]), ('disabled', '#2D2D30')],
                       foreground=[('disabled', '#555555')])
        
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground="white", font=("Segoe UI", 9, "bold"))
        self.style.map("Accent.TButton", background=[('active', self.colors["accent_hover"])])

        # Entry Style
        self.style.configure("TEntry", fieldbackground=self.colors["bg_light"], foreground="white", insertcolor="white", borderwidth=0)
        
        # Treeview Style
        self.style.configure("Treeview", 
                             background=self.colors["bg_dark"], 
                             foreground=self.colors["fg_primary"], 
                             fieldbackground=self.colors["bg_dark"],
                             font=("Segoe UI", 9),
                             rowheight=25)
        self.style.configure("Treeview.Heading", background=self.colors["bg_sidebar"], foreground=self.colors["fg_primary"], font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[('selected', self.colors["accent"])], foreground=[('selected', "white")])

    def _create_layout(self):
        # Main Layout: Sidebar (Left) + Content (Right)
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(main_container, style="Sidebar.TFrame", padding=10, width=250)
        main_container.add(self.sidebar, weight=1)
        
        self._build_sidebar()
        
        # Content Area
        self.content_area = ttk.Frame(main_container, style="TFrame", padding=10)
        main_container.add(self.content_area, weight=3)
        
        self._build_content_area()

    def _build_sidebar(self):
        ttk.Label(self.sidebar, text="搜索筛选", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Path Selection
        ttk.Label(self.sidebar, text="搜索路径:", style="Sidebar.TLabel").pack(anchor="w", pady=(0, 5))
        path_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        path_frame.pack(fill="x", pady=(0, 15))
        
        self.path_var = tk.StringVar(value=os.getcwd())
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(path_frame, text="...", width=3, command=self._browse_folder).pack(side="right")
        
        # Keywords
        ttk.Label(self.sidebar, text="关键字 (逗号分隔):", style="Sidebar.TLabel").pack(anchor="w", pady=(0, 5))
        self.keyword_var = tk.StringVar()
        ttk.Entry(self.sidebar, textvariable=self.keyword_var).pack(fill="x", pady=(0, 15))
        
        # File Types
        ttk.Label(self.sidebar, text="文件扩展名 (如 py, txt):", style="Sidebar.TLabel").pack(anchor="w", pady=(0, 5))
        self.ext_var = tk.StringVar()
        ttk.Entry(self.sidebar, textvariable=self.ext_var).pack(fill="x", pady=(0, 15))
        
        # Options
        self.content_search_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.sidebar, text="搜索文件内容", variable=self.content_search_var, style="Sidebar.TCheckbutton").pack(anchor="w", pady=2)
        
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="递归搜索子目录", variable=self.recursive_var, style="Sidebar.TCheckbutton").pack(anchor="w", pady=2)

        # Actions
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=20)
        
        self.btn_search = ttk.Button(self.sidebar, text="开始搜索", style="Accent.TButton", command=self._toggle_search)
        self.btn_search.pack(fill="x", pady=5)
        
        # History
        ttk.Label(self.sidebar, text="最近搜索记录", style="Sidebar.TLabel").pack(anchor="w", pady=(20, 5))
        self.history_list = tk.Listbox(self.sidebar, bg=self.colors["bg_light"], fg=self.colors["fg_primary"], borderwidth=0, height=5)
        self.history_list.pack(fill="x")
        self.history_list.bind('<<ListboxSelect>>', self._load_history)

    def _build_content_area(self):
        # Results Header
        header_frame = ttk.Frame(self.content_area, style="TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        self.status_label = ttk.Label(header_frame, text="准备就绪。", style="TLabel")
        self.status_label.pack(side="left")
        
        ttk.Button(header_frame, text="导出 CSV", command=self._export_results).pack(side="right")

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.content_area, mode="indeterminate", style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.pack_forget() # Hide initially

        # Split Pane: Results (Top) + Preview (Bottom)
        content_pane = ttk.PanedWindow(self.content_area, orient=tk.VERTICAL)
        content_pane.pack(fill="both", expand=True)
        
        # Results Table
        columns = ("name", "path", "size", "modified")
        self.tree = ttk.Treeview(content_pane, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("name", text="文件名", command=lambda: self._sort_column("name", False))
        self.tree.heading("path", text="路径", command=lambda: self._sort_column("path", False))
        self.tree.heading("size", text="大小 (KB)", command=lambda: self._sort_column("size", False))
        self.tree.heading("modified", text="修改时间", command=lambda: self._sort_column("modified", False))
        
        self.tree.column("name", width=150)
        self.tree.column("path", width=300)
        self.tree.column("size", width=80, anchor="e")
        self.tree.column("modified", width=120)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")
        
        content_pane.add(self.tree, weight=3)
        
        # Bind selection for preview
        self.tree.bind('<<TreeviewSelect>>', self._show_preview)

        # Preview Pane
        preview_frame = ttk.Frame(content_pane, style="Card.TFrame", padding=10)
        content_pane.add(preview_frame, weight=1)
        
        ttk.Label(preview_frame, text="内容预览", style="Sidebar.TLabel").pack(anchor="w", pady=(0, 5))
        self.preview_text = tk.Text(preview_frame, bg=self.colors["bg_dark"], fg=self.colors["fg_primary"], 
                                    insertbackground="white", borderwidth=0, font=("Consolas", 9), state="disabled")
        self.preview_text.pack(fill="both", expand=True)

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="选择搜索目录")
        if folder:
            self.path_var.set(folder)

    def _toggle_search(self):
        if self.is_searching:
            self.search_engine.stop_search()
            self.btn_search.config(text="开始搜索")
            self.status_label.config(text="搜索已停止。")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.is_searching = False
        else:
            self._start_search()

    def _start_search(self):
        path = self.path_var.get()
        keywords = [k.strip() for k in self.keyword_var.get().split(",") if k.strip()]
        extensions = [e.strip() for e in self.ext_var.get().split(",") if e.strip()]
        
        if not path or not os.path.exists(path):
            messagebox.showerror("错误", "无效的目录路径。")
            return

        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state="disabled")

        self.is_searching = True
        self.btn_search.config(text="停止搜索")
        self.status_label.config(text="正在搜索...")
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.start(10)
        
        # Add to history
        if keywords:
            self.history_list.insert(0, self.keyword_var.get())

        # Start Search Thread
        threading.Thread(target=self._run_search_thread, args=(path, keywords, extensions), daemon=True).start()

    def _run_search_thread(self, path, keywords, extensions):
        def on_match(result):
            self.result_queue.put(result)
            
        def on_progress(msg):
            # self.root.after(0, lambda: self.status_label.config(text=msg))
            pass # Too fast for UI updates sometimes

        self.search_engine.search(
            root_dir=path,
            keywords=keywords,
            extensions=extensions if extensions else None,
            search_content=self.content_search_var.get(),
            callback=on_match,
            progress_callback=on_progress
        )
        
        self.root.after(0, self._search_complete)

    def _setup_result_processing(self):
        """Periodically check queue for new results to update UI."""
        try:
            while True:
                result = self.result_queue.get_nowait()
                size_kb = f"{result['size'] / 1024:.1f}"
                mod_time = datetime.fromtimestamp(result['modified']).strftime('%Y-%m-%d %H:%M')
                
                self.tree.insert("", "end", values=(
                    result['name'],
                    result['path'],
                    size_kb,
                    mod_time
                ))
        except queue.Empty:
            pass
        
        self.root.after(100, self._setup_result_processing)

    def _search_complete(self):
        self.is_searching = False
        self.btn_search.config(text="开始搜索")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        count = len(self.tree.get_children())
        self.status_label.config(text=f"搜索完成。找到 {count} 个项目。")

    def _show_preview(self, event):
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        file_path = item['values'][1]
        
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        
        try:
            if os.path.getsize(file_path) > 1024 * 1024: # 1MB Limit for preview
                self.preview_text.insert(tk.END, "[文件过大无法预览]")
            else:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read(5000) # Read first 5000 chars
                    self.preview_text.insert(tk.END, content)
        except Exception as e:
            self.preview_text.insert(tk.END, f"[无法预览: {e}]")
            
        self.preview_text.config(state="disabled")

    def _sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Handle numeric sorting for size
        try:
            if col == "size":
                l.sort(key=lambda t: float(t[0]), reverse=reverse)
            else:
                l.sort(reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))

    def _export_results(self):
        file_path = filedialog.asksaveasfilename(title="导出结果", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("文件名,路径,大小(KB),修改时间\n")
                for item in self.tree.get_children():
                    vals = self.tree.item(item)['values']
                    f.write(f"{vals[0]},{vals[1]},{vals[2]},{vals[3]}\n")
            messagebox.showinfo("导出成功", "结果已成功导出。")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出失败: {e}")

    def _load_history(self, event):
        selection = self.history_list.curselection()
        if selection:
            keyword = self.history_list.get(selection[0])
            self.keyword_var.set(keyword)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSearchUI(root)
    root.mainloop()
