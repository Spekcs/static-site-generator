import unittest
from textnode import TextNode
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", "bold", "url.com")        
        node2 = TextNode("This is a text node", "bold")        
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("A", "B", "url")
        self.assertEqual(node.__repr__(), "TextNode(A, B, url)")
    
    def test_to_html_node(self):
        node = TextNode("Hi", "text")
        self.assertEqual(node.to_html_node(), LeafNode("Hi"))

    def test_to_html_node_link(self):
        node = TextNode("text", "link", "url")
        self.assertEqual(node.to_html_node(), LeafNode("text", "a", {"href":"url"}))

    def test_to_html_node_image(self):
        node = TextNode("Alt text", "image", "url")
        self.assertEqual(node.to_html_node(), LeafNode("", "img", {"src":"url", "alt":"Alt text"}))
    
    def test_to_html_node_invalid(self):
        node = TextNode("a", "b")
        self.assertRaises(ValueError, node.to_html_node)

if __name__ == "__main__":
    unittest.main()