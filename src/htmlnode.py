class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, 
                 children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return_str = ""
        for prop in self.props:
            return_str += f" {prop}=\"{self.props[prop]}\""
        return return_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"
    
    def __eq__(self, other):
        return self.tag == other.tag \
                and self.value == other.value \
                and self.children == other.children \
                and self.props == other.props