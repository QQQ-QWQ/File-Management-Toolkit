import unittest
import os
import shutil
from src.classifier import FileClassifier
from src.config import ConfigManager

class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.config_path = "test_config_classifier.json"
        self.manager = ConfigManager(self.config_path)
        self.classifier = FileClassifier(self.config_path)
        
        # Ensure default config is written
        self.manager.save_config(self.manager.load_config())

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_classify_by_extension(self):
        self.assertEqual(self.classifier.classify_file("document.pdf"), "Documents")
        self.assertEqual(self.classifier.classify_file("image.jpg"), "Images")
        self.assertEqual(self.classifier.classify_file("script.py"), "Code")

    def test_classify_by_keyword(self):
        self.manager.add_keyword_rule("report", "Reports")
        # Reload classifier to pick up changes
        self.classifier = FileClassifier(self.config_path)
        
        self.assertEqual(self.classifier.classify_file("annual_report_2023.pdf"), "Reports")

    def test_unknown_file(self):
        self.assertEqual(self.classifier.classify_file("unknown.xyz"), "Others")

    def test_excluded_file(self):
        self.assertTrue(self.classifier.is_excluded("path/to/.git/config"))
        self.assertTrue(self.classifier.is_excluded("temp.tmp"))
        self.assertFalse(self.classifier.is_excluded("normal.txt"))

if __name__ == '__main__':
    unittest.main()
