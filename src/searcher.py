import os
import threading
import fnmatch
from typing import List, Callable, Optional, Dict
from pathlib import Path
import time

class SearchEngine:
    def __init__(self):
        self._stop_event = threading.Event()
        self.results: List[Dict] = []
        self.is_searching = False

    def stop_search(self):
        """Stops the current search operation."""
        self._stop_event.set()
        self.is_searching = False

    def search(self, 
               root_dir: str, 
               keywords: List[str], 
               extensions: Optional[List[str]] = None,
               search_content: bool = False,
               max_depth: Optional[int] = None,
               callback: Optional[Callable[[Dict], None]] = None,
               progress_callback: Optional[Callable[[str], None]] = None):
        """
        Executes the search.
        
        Args:
            root_dir: Root directory to start search.
            keywords: List of keywords to match in filename or content.
            extensions: List of file extensions to include (e.g., ['py', 'txt']).
            search_content: If True, searches file content for keywords.
            max_depth: Maximum directory depth to traverse.
            callback: Function called when a match is found.
            progress_callback: Function called to update status/current file.
        """
        self._stop_event.clear()
        self.results = []
        self.is_searching = True
        
        root_path = Path(root_dir)
        if not root_path.exists():
            return

        try:
            self._recursive_search(root_path, keywords, extensions, search_content, max_depth, 0, callback, progress_callback)
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            self.is_searching = False

    def _recursive_search(self, 
                          current_dir: Path, 
                          keywords: List[str], 
                          extensions: Optional[List[str]],
                          search_content: bool, 
                          max_depth: Optional[int], 
                          current_depth: int,
                          callback: Callable,
                          progress_callback: Callable):
        
        if self._stop_event.is_set():
            return

        if max_depth is not None and current_depth > max_depth:
            return

        try:
            # Iterate through directory
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    if self._stop_event.is_set():
                        return
                    
                    if entry.is_dir(follow_symlinks=False):
                        # Recursive call for directories
                        if not entry.name.startswith('.'): # Skip hidden dirs
                            self._recursive_search(Path(entry.path), keywords, extensions, search_content, max_depth, current_depth + 1, callback, progress_callback)
                    
                    elif entry.is_file(follow_symlinks=False):
                        # Check file
                        if progress_callback:
                            progress_callback(f"正在扫描: {entry.name}")
                            
                        file_path = Path(entry.path)
                        
                        # 1. Extension Filter
                        if extensions:
                            if file_path.suffix.lstrip('.').lower() not in [e.lower() for e in extensions]:
                                continue

                        # 2. Keyword Filter (Filename)
                        match_found = False
                        filename_lower = entry.name.lower()
                        
                        # If no keywords provided, match all files (unless extension filter applied)
                        if not keywords:
                            match_found = True
                        else:
                            # Check filename matches any keyword
                            if any(k.lower() in filename_lower for k in keywords):
                                match_found = True
                        
                        # 3. Content Search (if enabled and not already matched by filename)
                        # Note: Usually content search is AND or OR logic. Here assuming OR (filename OR content)
                        # But if user wants to find files *containing* text, they might type a keyword.
                        # Let's refine: If search_content is True, we check content if filename didn't match OR if we want strict content match.
                        # Common behavior: 
                        # - If filename matches, add it.
                        # - If not, and search_content is True, check content.
                        
                        if not match_found and search_content:
                            if self._search_file_content(file_path, keywords):
                                match_found = True

                        if match_found:
                            result = {
                                "name": entry.name,
                                "path": str(file_path),
                                "size": entry.stat().st_size,
                                "modified": entry.stat().st_mtime,
                                "extension": file_path.suffix.lstrip('.')
                            }
                            self.results.append(result)
                            if callback:
                                callback(result)

        except PermissionError:
            pass # Skip non-accessible directories
        except Exception as e:
            print(f"Error scanning {current_dir}: {e}")

    def _search_file_content(self, file_path: Path, keywords: List[str]) -> bool:
        """Checks if file content contains any of the keywords."""
        try:
            # Skip binary files or very large files for content search to avoid hanging
            if file_path.stat().st_size > 10 * 1024 * 1024: # 10MB limit
                return False
                
            # Try reading as text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                return any(k.lower() in content for k in keywords)
        except Exception:
            return False
