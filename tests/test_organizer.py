import unittest
import os
import shutil
import tempfile
import logging
from pathlib import Path
from src.organizer import FileOrganizer
from src.config import ConfigManager

class TestOrganizer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "config.json")
        self.manager = ConfigManager(self.config_path)
        self.manager.save_config()
        
        # Reset logger handlers
        logger = logging.getLogger("FileOrganizer")
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
            
        self.organizer = FileOrganizer(self.temp_dir, self.config_path)

    def tearDown(self):
        self.organizer.close()
        # Ensure all handlers are closed before removing directory
        logger = logging.getLogger("FileOrganizer")
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
            
        shutil.rmtree(self.temp_dir)

    def test_organize_files(self):
        # Create test files
        (Path(self.temp_dir) / "document.txt").touch()
        (Path(self.temp_dir) / "image.png").touch()
        (Path(self.temp_dir) / "unknown.xyz").touch()

        # Run organizer
        self.organizer.organize()

        # Check if files are moved
        self.assertTrue((Path(self.temp_dir) / "Documents" / "document.txt").exists())
        self.assertTrue((Path(self.temp_dir) / "Images" / "image.png").exists())
        self.assertTrue((Path(self.temp_dir) / "Others" / "unknown.xyz").exists())

    def test_duplicate_handling(self):
        # Create a file in destination already
        os.makedirs(os.path.join(self.temp_dir, "Documents"))
        (Path(self.temp_dir) / "Documents" / "document.txt").touch()
        
        # Create a new file with same name in root
        (Path(self.temp_dir) / "document.txt").touch()

        # Run organizer
        self.organizer.organize()

        # Check if renamed
        self.assertTrue((Path(self.temp_dir) / "Documents" / "document.txt").exists())
        self.assertTrue((Path(self.temp_dir) / "Documents" / "document_1.txt").exists())

    def test_keyword_organization(self):
        self.manager.add_keyword_rule("report", "Reports")
        
        # Close old organizer and reload
        self.organizer.close()
        self.organizer = FileOrganizer(self.temp_dir, self.config_path)

        (Path(self.temp_dir) / "annual_report.pdf").touch()
        self.organizer.organize()
        
        self.assertTrue((Path(self.temp_dir) / "Reports" / "annual_report.pdf").exists())

if __name__ == '__main__':
    unittest.main()
