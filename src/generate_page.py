import os

from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    if not markdown.strip():
        raise Exception("Empty markdown file")
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("No header was found")

def extract_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        raise Exception(f"File not found {file_path}")

def generate_page(source_path, template_path, target_path):
    print(f" * Generating page from {source_path} to {target_path} using {template_path}")
    markdown = extract_contents(source_path)
    template = extract_contents(template_path)
    contents = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", contents)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w') as file:
        file.write(template)

def generate_pages(content_path, template_path, target_path):
    for filename in os.listdir(content_path):
        print(f" * Generating -> {filename}")
        file_path = os.path.join(content_path, filename)
        target = os.path.join(target_path, filename)
        if os.path.isfile(file_path) and file_path.endswith(".md"):
            target = target.replace(".md", ".html")
            generate_page(file_path, template_path, target)
        else:
            if not os.path.exists(target):
                os.mkdir(target)
            generate_pages(file_path, template_path, target)
