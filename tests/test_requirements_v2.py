import unittest
import os
import shutil
from pathlib import Path
from src.organizer import FileOrganizer
from src.config import ConfigManager

class TestRequirementsV2(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_env_v2")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        
        # Setup config
        self.config_path = self.test_dir / "config.json"
        self.cm = ConfigManager(str(self.config_path))
        # Ensure default config is loaded (which has our new rules)
        self.cm.save_config()

        # Create files
        # 1. Regular files
        (self.test_dir / "doc.txt").touch()
        (self.test_dir / "pic.jpg").touch()
        
        # 2. Subdirectory with files (should be ignored)
        self.sub_dir = self.test_dir / "SubDir"
        self.sub_dir.mkdir()
        (self.sub_dir / "subfile.txt").touch()
        
        # 3. Special files
        (self.test_dir / "app.exe").touch()
        (self.test_dir / "link.lnk").touch()
        (self.test_dir / "installer.msi").touch()
        
        # 4. Keyword conflict test
        # "report" keyword -> "Reports" usually. But "report.lnk" -> Shortcuts
        self.cm.add_keyword_rule("report", "Reports")
        (self.test_dir / "report.lnk").touch() 
        (self.test_dir / "report.pdf").touch() # Should go to Reports

    def tearDown(self):
        if self.test_dir.exists():
            # Close logger before cleanup
            if hasattr(self, 'organizer'):
                self.organizer.close()
            shutil.rmtree(self.test_dir)

    def test_organization_rules(self):
        self.organizer = FileOrganizer(str(self.test_dir), str(self.config_path))
        self.organizer.organize()
        
        # 1. Check Subdirectory (Non-recursive)
        self.assertTrue((self.sub_dir / "subfile.txt").exists(), "Subdirectory file should remain untouched")
        
        # 2. Check Shortcuts
        shortcuts_dir = self.test_dir / "Shortcuts"
        self.assertTrue(shortcuts_dir.exists(), "Shortcuts directory should exist")
        self.assertTrue((shortcuts_dir / "link.lnk").exists(), "lnk file should be in Shortcuts")
        self.assertTrue((shortcuts_dir / "report.lnk").exists(), "Special type should override keyword")
        
        # 3. Check Applications
        apps_dir = self.test_dir / "Applications"
        self.assertTrue(apps_dir.exists(), "Applications directory should exist")
        self.assertTrue((apps_dir / "app.exe").exists(), "exe file should be in Applications")
        self.assertTrue((apps_dir / "installer.msi").exists(), "msi file should be in Applications")
        
        # 4. Check Regular Files
        docs_dir = self.test_dir / "Documents"
        self.assertTrue(docs_dir.exists())
        self.assertTrue((docs_dir / "doc.txt").exists())
        
        images_dir = self.test_dir / "Images"
        self.assertTrue(images_dir.exists())
        self.assertTrue((images_dir / "pic.jpg").exists())
        
        # 5. Check Keyword Rules (for regular files)
        reports_dir = self.test_dir / "Reports"
        self.assertTrue(reports_dir.exists())
        self.assertTrue((reports_dir / "report.pdf").exists())

if __name__ == "__main__":
    unittest.main()