from textnode import TextNode
from parentnode import ParentNode
from leafnode import LeafNode
import re

class TextConverter:
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []

        for node in old_nodes:
            if node.text_type != "text":
                new_nodes.append(node)
                continue
            nodes_text = node.text.split(delimiter)
            if len(nodes_text) % 2 == 0:
                raise Exception("Invalid Markdown Syntax")

            for i in range(0, len(nodes_text)):
                if nodes_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(nodes_text[i], "text"))
                else:
                    new_nodes.append(TextNode(nodes_text[i], text_type))

        return new_nodes

    def extract_markdown_images(text):
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    def extract_markdown_links(text):
        return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    
    def split_nodes_image(old_nodes):
        new_nodes = []

        for node in old_nodes:
            if node.text_type != "text":
                new_nodes.append(node)
                continue
            images = TextConverter.extract_markdown_images(node.text)

            if len(images) == 0:
                new_nodes.append(node)
                continue

            current_text = node.text
            for i, image in enumerate(images):
                split_text = current_text.split(f"![{image[0]}]({image[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], "text"))
                new_nodes.append(TextNode(image[0], "image", image[1]))
                current_text = split_text[1]
                if i == len(images) - 1 and split_text[1] != "":
                    new_nodes.append(TextNode(split_text[1], "text"))
                

        return new_nodes


    def split_nodes_link(old_nodes):
        new_nodes = []

        for node in old_nodes:
            if node.text_type != "text":
                new_nodes.append(node)
                continue
            links = TextConverter.extract_markdown_links(node.text)

            if len(links) == 0:
                new_nodes.append(node)
                continue

            current_text = node.text
            for i, link in enumerate(links):
                split_text = current_text.split(f"[{link[0]}]({link[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], "text"))
                new_nodes.append(TextNode(link[0], "link", link[1]))
                current_text = split_text[1]
                if i == len(links) - 1 and split_text[1] != "":
                    new_nodes.append(TextNode(split_text[1], "text"))

        return new_nodes

    def text_to_textnodes(text):
        c = TextConverter
        bold_nodes = c.split_nodes_delimiter([TextNode(text, "text")], "**", "bold")
        italic_nodes = c.split_nodes_delimiter(bold_nodes, "*", "italic")
        code_nodes = c.split_nodes_delimiter(italic_nodes, "`", "code")
        image_nodes = c.split_nodes_image(code_nodes)
        link_nodes = c.split_nodes_link(image_nodes)
        return link_nodes
    
    def markdown_to_blocks(text):
        return [i.strip() for i in text.split("\n\n") if len(i) != 0]
    
    def block_to_block_type(block_text):
        if re.findall(r"^#{1,6} ", block_text):
            return "heading"
        if re.findall(r"^```.*```$", block_text):
            return "code"

        lines = block_text.split("\n")
        if all([i.startswith(">") for i in lines]):
            return "quote"
        if all([i.startswith("- ") for i in lines]) or all([i.startswith("* ") for i in lines]):
            return "unordered_list"
        if all([l.startswith(f"{i + 1}. ") for i, l in enumerate(lines)]):
            return "ordered_list"
        return "paragraph"

    def markdown_to_html_node(markdown):
        blocks = TextConverter.markdown_to_blocks(markdown)
        block_nodes = []
        for block in blocks:
            match TextConverter.block_to_block_type(block):
                case "heading":
                    block_nodes.append(TextConverter.heading_to_html_node(block))
                case "code":
                    block_nodes.append(TextConverter.code_to_html_node(block))
                case "quote":
                    block_nodes.append(TextConverter.quote_to_html_node(block))
                case "unordered_list":
                    block_nodes.append(TextConverter.ul_to_html_node(block))
                case "ordered_list":
                    block_nodes.append(TextConverter.ol_to_html_node(block))
                case "paragraph":
                    block_nodes.append(TextConverter.paragraph_to_html_node(block))
                case _:
                    raise ValueError("Invalid block")
        
        return ParentNode("div", block_nodes)
    
    def heading_to_html_node(block_text):
        heading_md = re.findall(r"^#{1,6} ", block_text)[0]        
        hashtag_count = len(heading_md) - 1
        text = block_text.lstrip(heading_md)
        return ParentNode(f"h{hashtag_count}", TextConverter.text_to_html_nodes(text))

    def code_to_html_node(block_text):
        text = block_text.strip("```")
        return ParentNode("pre", [LeafNode(text, "code")])

    def quote_to_html_node(block_text):
        text_lines = [w.lstrip("> ") for w in block_text.split("\n")]
        child_nodes = []
        for i in [TextConverter.text_to_html_nodes(l) for l in text_lines]:
            child_nodes.extend(i) 
        return ParentNode("blockquote", child_nodes)

    def ul_to_html_node(block_text):
        text_lines = [w for w in block_text.split("\n")]
        if text_lines[0].startswith("- "):
            text_lines = [i.lstrip("- ") for i in text_lines]
        else:
            text_lines = [i.lstrip("* ") for i in text_lines]

        return ParentNode("ul", [ParentNode("li", TextConverter.text_to_html_nodes(i)) for i in text_lines])

    def ol_to_html_node(block_text):
        text_lines = [l.lstrip(f"{i + 1}. ") for i, l in enumerate(block_text.split("\n"))]
        return ParentNode("ol", [ParentNode("li", TextConverter.text_to_html_nodes(i)) for i in text_lines])

    def paragraph_to_html_node(block_text):
        return ParentNode("p", [i.to_html_node() for i in TextConverter.text_to_textnodes(block_text)])
        
    def text_to_html_nodes(text):
        text_nodes = TextConverter.text_to_textnodes(text)
        return [i.to_html_node() for i in text_nodes]

    def extract_title(markdown):
        blocks = TextConverter.markdown_to_blocks(markdown)
        for block in blocks:
            if block.startswith("# "):
                return block.lstrip("# ").strip()
        raise Exception("No title in markdown file")