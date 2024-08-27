import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href":"url", "target":"_blank"})
        self.assertEqual(node.props_to_html(), " href=\"url\" target=\"_blank\"")

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(props = {"hi": "some_url"})
        self.assertEqual(node.props_to_html(), " hi=\"some_url\"")
      