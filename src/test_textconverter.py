import unittest
from textnode import TextNode
from textconverter import TextConverter

class TestTextConverter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("Hello *italic*.", "text")]
        nodes = TextConverter.split_nodes_delimiter(old_nodes, "*", "italic")
        self.assertEqual(nodes, [TextNode("Hello ", "text"), 
                                 TextNode("italic", "italic"), 
                                 TextNode(".", "text")])

    def test_split_nodes_delimiter_in_front(self):
        old_nodes = [TextNode("`some code` other text", "text"), 
                     TextNode("`code`", "text")]    
        nodes = TextConverter.split_nodes_delimiter(old_nodes, "`", "code")
        self.assertEqual(nodes, [TextNode("some code", "code"), 
                                 TextNode(" other text", "text"), 
                                 TextNode("code", "code")])
    
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("**bold** some text *italic* **bold again**", "text")]
        nodes = TextConverter.split_nodes_delimiter(old_nodes, "**", "bold")
        self.assertEqual(nodes, [TextNode("bold", "bold"), 
                                 TextNode(" some text *italic* ", "text"), 
                                 TextNode("bold again", "bold")])
    
    def test_split_nodes_delimiter_raises(self):
        old_nodes = [TextNode("* hi, this is broken", "text")]
        with self.assertRaises(Exception):
            TextConverter.split_nodes_delimiter(old_nodes, "*", "italic")

    def test_split_nodes_delimiter_several(self):
        old_nodes = [TextNode("**Hi** this is `code`*and italics*", "text")]
        nodes_bold = TextConverter.split_nodes_delimiter(old_nodes, "**", "bold")
        nodes_code = TextConverter.split_nodes_delimiter(nodes_bold, "`", "code")
        nodes_italic = TextConverter.split_nodes_delimiter(nodes_code, "*", "italic")
        self.assertEqual(nodes_italic, [TextNode("Hi", "bold"), 
                                        TextNode(" this is ", "text"),
                                        TextNode("code", "code"),
                                        TextNode("and italics", "italic")])
    
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(TextConverter.extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_markdown_images_no_images(self):
        text = "![this is not an image](because"
        self.assertEqual(TextConverter.extract_markdown_images(text), [])

    def test_extract_markdown_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(TextConverter.extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_link_no_link(self):
        text = "![This is a markdown image](url)"
        self.assertEqual(TextConverter.extract_markdown_links(text), [])
    
    def test_split_nodes_image(self):
        old_nodes = [TextNode("image ![to boot dev](https://www.boot.dev) and ![youtube](https)", "text")]
        self.assertEqual(TextConverter.split_nodes_image(old_nodes), [
                             TextNode("image ", "text"), 
                             TextNode("to boot dev", "image", "https://www.boot.dev"),
                             TextNode(" and ", "text"),
                             TextNode("youtube", "image", "https")])

    def test_split_nodes_image_first(self):
        old_nodes = [TextNode("![text](link) and link [link](url) ![second image](url)", "text")]
        self.assertEqual(TextConverter.split_nodes_image(old_nodes), 
                         [TextNode("text", "image", "link"),
                          TextNode(" and link [link](url) ", "text"),
                          TextNode("second image", "image", "url")])

    def test_split_nodes_link(self):
        old_nodes = [TextNode("link [link](url) and [second link](url)", "text")]
        self.assertEqual(TextConverter.split_nodes_link(old_nodes), [
                             TextNode("link ", "text"), 
                             TextNode("link", "link", "url"),
                             TextNode(" and ", "text"),
                             TextNode("second link", "link", "url")])

    def test_split_nodes_link_and_image(self):
        old_nodes = [TextNode("this is code", "code"), TextNode("![image](url)[link](url)", "text")]
        split_images = TextConverter.split_nodes_image(old_nodes)
        self.assertEqual(TextConverter.split_nodes_link(split_images), [
                         TextNode("this is code", "code"),
                         TextNode("image", "image", "url"),
                         TextNode("link", "link", "url")])
    
    def test_split_nodes_link_text_final(self):
        old_nodes = [TextNode("[link](url) text", "text")]
        self.assertEqual(TextConverter.split_nodes_link(old_nodes), [
            TextNode("link", "link", "url"), 
            TextNode(" text", "text")])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(TextConverter.text_to_textnodes(text),
                         [
        TextNode("This is ", "text"),
        TextNode("text", "bold"),
        TextNode(" with an ", "text"),
        TextNode("italic", "italic"),
        TextNode(" word and a ", "text"),
        TextNode("code block", "code"),
        TextNode(" and an ", "text"),
        TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", "text"),
        TextNode("link", "link", "https://boot.dev"),
        ])

    def test_text_to_textnodes_multiple(self):
        text = "*italic text*`code`*italic* ![image](url)"
        self.assertEqual(TextConverter.text_to_textnodes(text), [
            TextNode("italic text", "italic"),
            TextNode("code", "code"),
            TextNode("italic", "italic"),
            TextNode(" ", "text"),
            TextNode("image", "image", "url")
        ])

    def test_text_to_textnodes_text_final(self):
        text = "*italic* text **bold**"
        self.assertEqual(TextConverter.text_to_textnodes(text), [
            TextNode("italic", "italic"),
            TextNode(" text ", "text"),
            TextNode("bold", "bold")
        ])