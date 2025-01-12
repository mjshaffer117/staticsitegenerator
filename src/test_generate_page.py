import unittest

from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_title(self):
        markdown = """
Some intro text
# This is the Title
More content here
"""
        self.assertEqual(
            extract_title(markdown),
            "This is the Title"
        )

    def test_title_2(self):
        markdown = """
There is no header
## There is no header
### There is no header #
"""
        with self.assertRaises(Exception):
            extract_title(markdown)
            

if __name__ == "__main__":
    unittest.main()