import logging
import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any

class OperationLogger:
    def __init__(self, log_file: str = "organizer.log", undo_file: str = "undo_log.json"):
        self.log_file = log_file
        self.undo_file = undo_file
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configures the logger."""
        logger = logging.getLogger("FileOrganizer")
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers to ensure we write to the correct file
        # This is important for tests or when log file path changes
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Ensure log directory exists
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
            
        return logger

    def close(self):
        """Closes all handlers to release file locks."""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def log_operation(self, operation_type: str, src: str, dest: str, success: bool, message: str = ""):
        """Logs an operation and saves to undo history if successful move."""
        log_msg = f"{operation_type}: {src} -> {dest} | Success: {success} | {message}"
        if success:
            self.logger.info(log_msg)
            if operation_type == "MOVE":
                self._save_undo_record(src, dest)
        else:
            self.logger.error(log_msg)

    def _save_undo_record(self, src: str, dest: str):
        """Saves a record to the undo log."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "src": src,
            "dest": dest
        }
        
        history = self._load_undo_history()
        history.append(record)
        
        try:
            with open(self.undo_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save undo record: {e}")

    def _load_undo_history(self) -> List[Dict[str, str]]:
        """Loads the undo history."""
        if not os.path.exists(self.undo_file):
            return []
        try:
            with open(self.undo_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def undo_last_operation(self) -> bool:
        """Undoes the last recorded operation."""
        history = self._load_undo_history()
        if not history:
            self.logger.warning("No operations to undo.")
            return False

        last_op = history.pop()
        src = last_op["src"]
        dest = last_op["dest"]

        try:
            if os.path.exists(dest):
                # Ensure the original directory exists
                os.makedirs(os.path.dirname(src), exist_ok=True)
                shutil.move(dest, src)
                self.logger.info(f"Undo successful: {dest} -> {src}")
                
                # Update history file
                with open(self.undo_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                return True
            else:
                self.logger.error(f"Undo failed: File not found at {dest}")
                return False
        except Exception as e:
            self.logger.error(f"Undo failed: {e}")
            return False

    def clear_undo_history(self):
        """Clears the undo history."""
        if os.path.exists(self.undo_file):
            os.remove(self.undo_file)
            self.logger.info("Undo history cleared.")
