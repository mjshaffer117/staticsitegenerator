import unittest

from markdown_blocks import markdown_to_blocks, block_to_blocktype

class TestMarkDownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )

    def test_block_to_blocktype(self):
        block = "# heading"
        self.assertEqual(block_to_blocktype(block), "heading")

        block = "```\ncode here\n```"
        self.assertEqual(block_to_blocktype(block), "code")

        block = "> quote\n> more quote"
        self.assertEqual(block_to_blocktype(block), "quote")

        block = "* list\n* items"
        self.assertEqual(block_to_blocktype(block), "unordered_list")

        block = "1. list\n2. items"
        self.assertEqual(block_to_blocktype(block), "ordered_list")
        
        block = "paragraph\n1. paragraph"
        self.assertEqual(block_to_blocktype(block), "paragraph")