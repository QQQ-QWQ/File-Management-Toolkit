import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple, Callable
from .classifier import FileClassifier
from .logger import OperationLogger

class FileOrganizer:
    def __init__(self, root_dir: str, config_path: str = "config.json", log_file: str = "organizer.log"):
        self.root_dir = Path(root_dir).resolve()
        self.classifier = FileClassifier(config_path)
        self.logger = OperationLogger(log_file)
        self.log = logging.getLogger("FileOrganizer")
        
        if not self.root_dir.exists():
            raise FileNotFoundError(f"Directory not found: {root_dir}")

    def close(self):
        """Closes the logger."""
        self.logger.close()

    def scan_files(self) -> List[Path]:
        """Scans the directory for files to organize (non-recursive)."""
        files_to_move = []
        try:
            # Use os.scandir for better performance and check for directories
            with os.scandir(self.root_dir) as entries:
                for entry in entries:
                    if entry.is_dir():
                        self.log.info(f"Skipping directory: {entry.path}")
                        continue
                    
                    if entry.is_file():
                        file_path = Path(entry.path)
                        # Check exclusion rules
                        if not self.classifier.is_excluded(str(file_path)):
                            files_to_move.append(file_path)
                            
        except OSError as e:
            self.log.error(f"Error scanning directory {self.root_dir}: {e}")
            
        return files_to_move

    def _get_unique_path(self, destination: Path) -> Path:
        """Generates a unique filename if the destination exists."""
        if not destination.exists():
            return destination
        
        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent
        counter = 1
        
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def move_file(self, file_path: Path) -> bool:
        """Moves a single file to its classified folder."""
        try:
            category = self.classifier.classify_file(str(file_path))
            if not category:
                self.log.info(f"Skipped: {file_path} (No category found)")
                return False

            dest_dir = self.root_dir / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = dest_dir / file_path.name
            
            # Prevent moving to same location
            if file_path.parent == dest_dir:
                 return False

            final_dest = self._get_unique_path(dest_path)
            
            shutil.move(str(file_path), str(final_dest))
            self.logger.log_operation("MOVE", str(file_path), str(final_dest), True)
            return True
            
        except Exception as e:
            self.logger.log_operation("MOVE", str(file_path), "", False, str(e))
            return False

    def organize(self, progress_callback: Callable[[int, int], None] = None):
        """Main organization function using thread pool."""
        files = self.scan_files()
        total_files = len(files)
        completed = 0
        
        self.log.info(f"Found {total_files} files to organize.")
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.move_file, f): f for f in files}
            
            for future in as_completed(futures):
                completed += 1
                if progress_callback:
                    progress_callback(completed, total_files)
                
                try:
                    future.result()
                except Exception as e:
                    self.log.error(f"Error processing file: {e}")

    def undo(self):
        """Reverts the last batch of operations."""
        # Simple implementation: undo until empty or user stops (interactive logic elsewhere)
        # For now, undo one by one in reverse order
        # In a real app, we might track "sessions" or "batches"
        # Here we just expose the single undo capability from logger
        pass  # Implementation handled by logger.undo_last_operation
