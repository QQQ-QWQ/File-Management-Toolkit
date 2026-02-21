import unittest
from tests.test_config import TestConfigManager
from tests.test_classifier import TestClassifier
from tests.test_organizer import TestOrganizer
from tests.test_logger import TestLogger

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestClassifier))
    suite.addTests(loader.loadTestsFromTestCase(TestOrganizer))
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
