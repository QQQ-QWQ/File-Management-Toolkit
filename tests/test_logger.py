import unittest
import os
import shutil
import tempfile
import logging
from src.logger import OperationLogger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.undo_file = os.path.join(self.temp_dir, "test_undo.json")
        
        # Reset logger handlers to avoid using old handlers from previous tests
        logger = logging.getLogger("FileOrganizer")
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
            
        self.logger = OperationLogger(self.log_file, self.undo_file)

    def tearDown(self):
        # Close logger handlers to release file lock
        self.logger.close()
        shutil.rmtree(self.temp_dir)

    def test_log_operation(self):
        self.logger.log_operation("MOVE", "src/file.txt", "dest/file.txt", True)
        
        # Flush handlers to ensure data is written
        for handler in self.logger.logger.handlers:
            handler.flush()
            
        self.assertTrue(os.path.exists(self.log_file))
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("MOVE: src/file.txt -> dest/file.txt | Success: True", content)

    def test_undo_operation(self):
        # Create a dummy file at "dest" to simulate a move
        dest_path = os.path.join(self.temp_dir, "dest", "file.txt")
        os.makedirs(os.path.dirname(dest_path))
        with open(dest_path, 'w') as f:
            f.write("test")

        src_path = os.path.join(self.temp_dir, "src", "file.txt")
        
        # Log the operation manually to simulate history
        self.logger._save_undo_record(src_path, dest_path)

        # Undo
        self.assertTrue(self.logger.undo_last_operation())
        
        # Check if file moved back
        self.assertTrue(os.path.exists(src_path))
        self.assertFalse(os.path.exists(dest_path))

if __name__ == '__main__':
    unittest.main()
