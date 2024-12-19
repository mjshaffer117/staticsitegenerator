import unittest

from textnode import TextNode, TextType

from inline_markdown import(
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnode,
    split_nodes_images,
    split_nodes_links
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delimiter_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delimiter_bold_and_italic(self):
        node = TextNode("**Bold** & *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" & ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delimiter_exception(self):
        node = TextNode("This is `text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    # TEST IMAGES #
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_no_image(self):
        text = "This is text without any images"
        self.assertListEqual(
            extract_markdown_images(text),
            []
        )

    # TEST LINKS #
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_extract_links_with_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). But I also wanted to share an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_split_nodes_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_images([node]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_split_nodes_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_links([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com")
            ]
        )

    def test_split_nodes_no_links(self):
        node = TextNode("This is a text with no links.", TextType.TEXT)
        self.assertListEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a text with no links.", TextType.TEXT)
            ]
        )

    def test_split_nodes_malformed(self):
        node = TextNode("Here's an [invalid link(no closing bracket) and some text", TextType.TEXT)
        self.assertListEqual(
            split_nodes_links([node]),
            [
                TextNode("Here's an [invalid link(no closing bracket) and some text", TextType.TEXT)
            ]
        )

    # TEST TEXT TO TEXTNODE #
    def test_text_to_textnode(self):
        nodes = text_to_textnode("This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        )

if __name__ == "__main__":
    unittest.main()