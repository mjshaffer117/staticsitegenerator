from textnode import TextNode, TextType

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_element(old_nodes, extract_func, text_type, format_str):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_string = old_node.text
        elements = extract_func(text_string)
        if len(elements) == 0:
            new_nodes.append(old_node)
            continue
        for element in elements:
            alt_text, url = element[0], element[1]
            sections = text_string.split(format_str.format(alt_text, url), 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, element section not closed")
            if sections[0] == "":
                continue
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, text_type, url))
                text_string = sections[1]
        if text_string != "":
            new_nodes.append(TextNode(text_string, TextType.TEXT))
    return new_nodes

def split_nodes_images(old_nodes):
    return split_nodes_element(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        "![{}]({})"
        )

def split_nodes_links(old_nodes):
    return split_nodes_element(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        "[{}]({})"
        )

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches