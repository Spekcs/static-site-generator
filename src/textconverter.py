from textnode import TextNode

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