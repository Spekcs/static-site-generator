from leafnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text \
            and self.text_type == other.text_type \
            and self.url == other.url
    
    def to_html_node(self):
        match self.text_type:
            case "text":
                return LeafNode(self.text)
            case "bold":
                return LeafNode(self.text, "b")
            case "italic":
                return LeafNode(self.text, "i")
            case "code":
                return LeafNode(self.text, "code")
            case "link":
                return LeafNode(self.text, "a", props={"href":self.url})
            case "image":
                return LeafNode("", "img", props={"src": self.url, "alt": self.text})
            case _:
                raise ValueError("Invalid text_type")


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"