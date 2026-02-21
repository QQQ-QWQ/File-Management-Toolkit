import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from .config import ConfigManager

class FileClassifier:
    def __init__(self, config_path: str = "config.json"):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        self.extension_map = self._build_extension_map()
        self.special_map = self._build_special_map()

    def _build_extension_map(self) -> Dict[str, str]:
        """Maps file extensions to categories."""
        ext_map = {}
        for category, extensions in self.config.get("file_types", {}).items():
            for ext in extensions:
                ext_map[ext.lower()] = category
        return ext_map

    def _build_special_map(self) -> Dict[str, str]:
        """Maps special extensions to categories."""
        special_map = {}
        for category, extensions in self.config.get("special_types", {}).items():
            for ext in extensions:
                special_map[ext.lower()] = category
        return special_map

    def classify_file(self, file_path: str) -> Optional[str]:
        """Determines the category folder for a file."""
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1].lstrip(".").lower()

        # 1. Special Type matching (Highest Priority)
        if extension in self.special_map:
            return self.special_map[extension]

        # 2. Keyword matching
        for keyword, folder_name in self.config.get("keywords", {}).items():
            if keyword.lower() in file_name.lower():
                return folder_name

        # 3. Extension matching
        if extension in self.extension_map:
            return self.extension_map[extension]
        
        # 4. Default category for unknown files
        return "Others"

    def is_excluded(self, file_path: str) -> bool:
        """Checks if a file or directory should be excluded."""
        path_obj = Path(file_path)
        
        # Check excluded directories
        for excluded_dir in self.config["exclude_dirs"]:
            if excluded_dir in path_obj.parts:
                return True
        
        # Check excluded extensions
        extension = path_obj.suffix.lstrip(".").lower()
        if extension in self.config["exclude_extensions"]:
            return True
            
        return False
