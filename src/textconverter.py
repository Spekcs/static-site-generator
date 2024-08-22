from textnode import TextNode
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