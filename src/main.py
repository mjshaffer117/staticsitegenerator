from textnode import TextNode, TextType

def main():
    node = TextNode("This is a text", TextType.CODE, "https://whompwhomp.io")
    print(node)

if __name__ == "__main__":
    main()

