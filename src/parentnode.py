from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        
        html_text = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_text += child.to_html()
        return html_text + f"</{self.tag}>"