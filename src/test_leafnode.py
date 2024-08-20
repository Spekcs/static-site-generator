import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("Hi", "a", {"href":"url.com"})
        self.assertEqual(node.to_html(), "<a href=\"url.com\">Hi</a>")
    
    def test_to_html_empty(self):
        node = LeafNode(None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_props(self):
        node = LeafNode("Hi", "p")
        self.assertEqual(node.to_html(), "<p>Hi</p>")

    def test_to_html_no_tag(self):
        node = LeafNode("Hi")
        self.assertEqual(node.to_html(), "Hi")