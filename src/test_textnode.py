import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("URL is set to None", TextType.ITALIC, None)
        node2 = TextNode("URL is set to None", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_unequal_text(self):
        node = TextNode("One text", TextType.CODE)
        node2 = TextNode("Two text", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_unequal_texttype(self):
        node = TextNode("Testing different text types", TextType.BOLD)
        node2 = TextNode("Testing different text types", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_unequal_url(self):
        node = TextNode("Testing different URLs", TextType.BOLD, "www.notarealwebsitedomain.com")
        node2 = TextNode("Testing different URLs", TextType.BOLD, "www.veryrealwebsitedomain.org")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()