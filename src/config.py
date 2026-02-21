import json
import os
from pathlib import Path
from typing import Dict, List, Any

DEFAULT_CONFIG = {
    "special_types": {
        "Shortcuts": ["lnk", "url", "desktop"],
        "Applications": ["exe", "msi", "dmg", "app"]
    },
    "file_types": {
        "Documents": ["doc", "docx", "pdf", "txt", "xls", "xlsx", "ppt", "pptx", "md", "csv"],
        "Images": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "tiff", "ico"],
        "Videos": ["mp4", "mkv", "avi", "mov", "wmv", "flv", "webm"],
        "Audio": ["mp3", "wav", "flac", "m4a", "aac", "ogg"],
        "Archives": ["zip", "rar", "7z", "tar", "gz", "iso"],
        "Code": ["py", "java", "c", "cpp", "js", "html", "css", "php", "json", "xml", "sql"]
    },
    "keywords": {},  # Format: {"keyword": "Folder Name"}
    "exclude_dirs": [".git", ".vscode", "__pycache__", "venv", "node_modules"],
    "exclude_extensions": ["ini", "tmp", "log"],
    "backup_enabled": True,
    "log_file": "organizer.log",
    "undo_file": "undo_log.json"
}

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Loads configuration from file or returns default."""
        if not os.path.exists(self.config_path):
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with default to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            print(f"Error loading config: {e}. Using default.")
            return DEFAULT_CONFIG

    def save_config(self, config: Dict[str, Any] = None):
        """Saves current configuration to file."""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_extension_map(self) -> Dict[str, str]:
        """Inverts the file_types dict to map extension -> category."""
        ext_map = {}
        for category, extensions in self.config["file_types"].items():
            for ext in extensions:
                ext_map[ext.lower()] = category
        return ext_map

    def add_keyword_rule(self, keyword: str, folder_name: str):
        """Adds a keyword rule."""
        self.config["keywords"][keyword] = folder_name
        self.save_config()

    def add_file_type_rule(self, category: str, extension: str):
        """Adds a file type rule."""
        if category not in self.config["file_types"]:
            self.config["file_types"][category] = []
        if extension.lower() not in self.config["file_types"][category]:
            self.config["file_types"][category].append(extension.lower())
            self.save_config()
