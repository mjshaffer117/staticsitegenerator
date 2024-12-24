import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_return_text(self):
        node = LeafNode(
            None,
            "This is just normal text."
        )
        self.assertEqual(
            node.to_html(),
            "This is just normal text."
        )

    def test_leafnode(self):
        node = LeafNode(
            "p",
            "A simple paragraph node"
        )
        self.assertEqual(
            node.to_html(),
            "<p>A simple paragraph node</p>"
        )

    def test_leafnode_props(self):
        node = LeafNode(
            "a",
            "Click Me!",
            {"href" : "https://google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com">Click Me!</a>'
        )

    def test_leafnode_exception(self):
        node = LeafNode(
            None,
            None,
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_repr(self):
        node = LeafNode(
            None,
            "plain text"
        )
        self.assertEqual(
            node.__repr__(),
            "LeafNode(None, plain text, None)"
        )

    def test_parentnode(self):
        node = ParentNode(
            'p',
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_parentnode_grandchildren(self):
        grandchild_node = LeafNode("i", "Grandchild node")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><i>Grandchild node</i></span></div>"
        )

    def test_parentnode_repr(self):
        node = ParentNode(
            'p',
            [
                LeafNode("b", "Bold text")
            ]
        )
        self.assertEqual(
            node.__repr__(),
            "ParentNode(p, children: [LeafNode(b, Bold text, None)], None)"
        )
        

if __name__ == "__main__":
    unittest.main()