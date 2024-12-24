from htmlnode import HTMLNode, LeafNode, ParentNode

from inline_markdown import text_to_textnode
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_blocktype(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def heading_to_html_node(block):
    header_tag = f"h{len(block.split(' ')[0])}"
    block = block.lstrip('#').strip()
    return ParentNode(header_tag, text_to_children(block))

def code_to_html_node(block):
    # NEST INSIDE A <PRE> TAG
    return ParentNode("pre", [LeafNode("code", block)])

def quote_to_html_node(block):
    items = [line.lstrip('>').strip() for line in block.split('\n') if line.strip()]
    block = " ".join(items)
    return ParentNode("blockquote", text_to_children(block))

def unordered_list_to_html_node(block):
    # EACH LISTED ITEM <LI>
    items = [line.lstrip('* -').strip() for line in block.split('\n') if line.strip()]
    list_items = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", list_items)

def ordered_list_to_html_block(block):
    # EACH LISTED ITEM <LI>
    items = [line.split('. ', 1)[1].strip() for line in block.split('\n') if line.strip()]
    list_items = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", list_items)

def paragraph_to_html_node(block):
    block = " ".join(block.split("\n"))
    processed_children = text_to_children(block)
    return ParentNode("p", processed_children)

def div_wrapper(nodes):
    return ParentNode("div", nodes)

def markdown_to_html_node(markdown):
    nodes = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_blocktype(block)
        if block_type == "heading":
            html_node = heading_to_html_node(block)
        elif block_type == "code":
            html_node = code_to_html_node(block)
        elif block_type == "quote":
            html_node = quote_to_html_node(block)
        elif block_type == "unordered_list":
            html_node = unordered_list_to_html_node(block)
        elif block_type == "ordered_list":
            html_node = ordered_list_to_html_block(block)
        elif block_type == "paragraph":
            html_node = paragraph_to_html_node(block)
        else:
            raise ValueError("Invalid block type")
        nodes.append(html_node)
    return div_wrapper(nodes)