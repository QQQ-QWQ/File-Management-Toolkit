import unittest
import os
import json
from src.config import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_config = "test_config.json"
        self.manager = ConfigManager(self.test_config)

    def tearDown(self):
        if os.path.exists(self.test_config):
            os.remove(self.test_config)

    def test_load_default(self):
        config = self.manager.load_config()
        self.assertIn("file_types", config)
        self.assertIn("keywords", config)

    def test_save_and_load(self):
        config = self.manager.load_config()
        config["keywords"]["test"] = "TestFolder"
        self.manager.save_config(config)
        
        new_manager = ConfigManager(self.test_config)
        new_config = new_manager.load_config()
        self.assertEqual(new_config["keywords"]["test"], "TestFolder")

    def test_add_rule(self):
        self.manager.add_keyword_rule("foo", "FooFolder")
        config = self.manager.load_config()
        self.assertEqual(config["keywords"]["foo"], "FooFolder")

if __name__ == '__main__':
    unittest.main()
