import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode(
            "div",
            "Hello World",
            None,
            {"class" : "greeting", "href" : "https://boot.dev"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"'
        )

    def test_values(self):
        node = HTMLNode(
            "p",
            "This is a paragraph",
            None,
            {"class" : "paragraph", "href" : "https://boot.dev"}
        )
        self.assertEqual(
            node.tag,
            "p"
        )
        self.assertEqual(
            node.value,
            "This is a paragraph"
        )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            {"class" : "paragraph", "href" : "https://boot.dev"}
        )

    def test_html_props_none(self):
        node = HTMLNode(
            "div",
            "Hello World",
            None,
            None
        )
        self.assertEqual(
            node.props_to_html(),
            ""
        )

    def test_repr(self):
        node = HTMLNode(
            "h1",
            "This Is A Heading",
            None,
            None
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(h1, This Is A Heading, children: None, None)"
        )
        

if __name__ == "__main__":
    unittest.main()