import unittest
import os

class TestCommit(unittest.TestCase):
    def test_verif_files(self):
        root_files = os.listdir()
        self.assertIn('.gitignore', root_files)
        self.assertIn('requirements.txt', root_files)

if __name__ == '__main__':
    unittest.main(verbosity = 2)