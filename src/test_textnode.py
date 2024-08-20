import unittest
from textnode import TextNode

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
    

if __name__ == "__main__":
    unittest.main()