import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
        "p",
        [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
        ])

        self.assertEqual(node.to_html(), 
                         "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_no_tag(self):
        node = ParentNode(None, LeafNode("Hi"))
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("a", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_props(self):
        node = ParentNode("p", [LeafNode("Bold text", "b")], {"prop": "something"})
        self.assertEqual(node.to_html(), "<p prop=\"something\"><b>Bold text</b></p>")
    
    def test_to_html_recursion(self):
        node = ParentNode(
        "p",
        [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
        ])
        node2 = ParentNode("p", [node, LeafNode("Normal text", None)], {"prop": "hi"})
        self.assertEqual(node2.to_html(),
                         "<p prop=\"hi\"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text</p>")