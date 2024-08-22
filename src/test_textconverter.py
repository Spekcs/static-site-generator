import unittest
from textnode import TextNode
from textconverter import TextConverter

class TestTextConverter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("Hello *italic*.", "text")]
        nodes = TextConverter.split_nodes_delimiter(old_nodes, "*", "italic")
        self.assertEqual(nodes, [TextNode("Hello ", "text"), TextNode("italic", "italic"), TextNode(".", "text")])

    def test_split_nodes_delimiter_in_front(self):
        old_nodes = [TextNode("`some code` other text", "text"), TextNode("`code`", "text")]    
        nodes = TextConverter.split_nodes_delimiter(old_nodes, "`", "code")
        self.assertEqual(nodes, [TextNode("some code", "code"), TextNode(" other text", "text"), TextNode("code", "code")])
    
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("**bold** some text *italic* **bold again**", "text")]
        nodes = TextConverter.split_nodes_delimiter(old_nodes, "**", "bold")
        self.assertEqual(nodes, [TextNode("bold", "bold"), TextNode(" some text *italic* ", "text"), TextNode("bold again", "bold")])
    
    def test_split_nodes_delimiter_raises(self):
        old_nodes = [TextNode("* hi, this is broken", "text")]
        with self.assertRaises(Exception):
            TextConverter.split_nodes_delimiter(old_nodes, "*", "italic")

    def test_split_nodes_delimiter_several(self):
        old_nodes = [TextNode("**Hi** this is `code`*and italics*", "text")]
        nodes_bold = TextConverter.split_nodes_delimiter(old_nodes, "**", "bold")
        nodes_code = TextConverter.split_nodes_delimiter(nodes_bold, "`", "code")
        nodes_italic = TextConverter.split_nodes_delimiter(nodes_code, "*", "italic")
        self.assertEqual(nodes_italic, [TextNode("Hi", "bold"), TextNode(" this is ", "text"), TextNode("code", "code"), TextNode("and italics", "italic")])