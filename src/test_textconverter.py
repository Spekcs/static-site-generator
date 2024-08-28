import unittest
from parentnode import ParentNode
from leafnode import LeafNode
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
    
    def test_markdown_to_blocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(TextConverter.markdown_to_blocks(text), 
                         ["# This is a heading", 
                          "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                          "* This is the first list item in a list block\n* This is a list item\n* This is another list item"])

    def test_markdown_to_blocks_multiple_lines(self):
        text = """This is a block

This is a second block

  *list
*list2


third block  """

        self.assertEqual(TextConverter.markdown_to_blocks(text), 
                         ["This is a block", "This is a second block", "*list\n*list2", "third block"])
        
    def test_block_to_block_type_heading(self):
        block = "### asdfk"
        block1 = "#sdf"
        block2 = "######## sdfjh"
        self.assertEqual(TextConverter.block_to_block_type(block), "heading")
        self.assertEqual(TextConverter.block_to_block_type(block1), "paragraph")
        self.assertEqual(TextConverter.block_to_block_type(block2), "paragraph")

    def test_block_to_block_type_code(self):
        block = "``````"
        block2 = "```code```"
        block3 = "``` ``"
        self.assertEqual(TextConverter.block_to_block_type(block), "code")
        self.assertEqual(TextConverter.block_to_block_type(block2), "code")
        self.assertEqual(TextConverter.block_to_block_type(block3), "paragraph")
    
    def test_block_to_block_type_quote(self):
        block = ">hi \n> this is quote"
        block2 = ">not \n a quote"
        block3 = "asdf"
        self.assertEqual(TextConverter.block_to_block_type(block), "quote")
        self.assertEqual(TextConverter.block_to_block_type(block2), "paragraph")
        self.assertEqual(TextConverter.block_to_block_type(block3), "paragraph")

    def test_block_to_block_type_ul(self):
        block = "- hi\n- this\n- "
        block2 = "* another\n* list\n* sdf"
        block3 = "- not\n a\n * list"
        self.assertEqual(TextConverter.block_to_block_type(block), "unordered_list")
        self.assertEqual(TextConverter.block_to_block_type(block2), "unordered_list")
        self.assertEqual(TextConverter.block_to_block_type(block3), "paragraph")
    
    def test_block_to_block_type_ol(self):
        block = "1. sdf\n2. sadf \n3. sod"
        block2 = "1. sdf\n 3. asdf\n 2.sdf"
        block3 = "1.sdfh\n2.sdfh"
        self.assertEqual(TextConverter.block_to_block_type(block), "ordered_list")
        self.assertEqual(TextConverter.block_to_block_type(block2), "paragraph")
        self.assertEqual(TextConverter.block_to_block_type(block3), "paragraph")
    
    def test_markdown_to_html_node_heading(self):
        block = "## This is a heading \n\n### This is another"
        self.assertEqual(TextConverter.markdown_to_html_node(block), 
                         ParentNode("div", [ParentNode("h2", [LeafNode("This is a heading")]), ParentNode("h3", [LeafNode("This is another")])]))
                    
    def test_markdown_to_html_node_code(self):
        block = "```This is code```"
        self.assertEqual(TextConverter.markdown_to_html_node(block),
                         ParentNode("div", [ParentNode("pre", [LeafNode("This is code", "code")])]))
    
    def test_markdown_to_html_node_quote(self):
        block = ">*This is * a"
        self.assertEqual(TextConverter.markdown_to_html_node(block),
                         ParentNode("div", [ParentNode("blockquote", [LeafNode("This is ", "i"), LeafNode(" a")])]))

    def test_markdown_to_html_node_ul(self):
        block = "- this\n- is \n- a list \n\n * so\n* is this "
        self.assertEqual(TextConverter.markdown_to_html_node(block),
                         ParentNode("div", [ParentNode("ul", [ParentNode("li", [LeafNode("this")]), ParentNode("li", [LeafNode("is ")]), ParentNode("li", [LeafNode("a list")])]),
                                            ParentNode("ul", [ParentNode("li", [LeafNode("so")]), ParentNode("li", [LeafNode("is this")])])]))

    def test_markdown_to_html_node_ol(self):
        block = "1. this\n2. is \n3. a list \n\n 1. so\n2. is this "
        self.assertEqual(TextConverter.markdown_to_html_node(block),
                         ParentNode("div", [ParentNode("ol", [ParentNode("li", [LeafNode("this")]), ParentNode("li", [LeafNode("is ")]), ParentNode("li", [LeafNode("a list")])]),
                                            ParentNode("ol", [ParentNode("li", [LeafNode("so")]), ParentNode("li", [LeafNode("is this")])])]))
            
    def test_markdown_to_html_node_paragraph(self):
        block = "*this is italic* and **bold**"
        self.assertEqual(TextConverter.markdown_to_html_node(block), 
                         ParentNode("div", [ParentNode("p", [
            LeafNode("this is italic", "i"), LeafNode(" and "), LeafNode("bold", "b")
        ])]))

    def test_text_to_html_nodes(self):
        text = "*italic text*`code`*italic* ![image](url)"
        self.assertEqual(TextConverter.text_to_html_nodes(text), [
            LeafNode("italic text", "i"),
            LeafNode("code", "code"),
            LeafNode("italic", "i"),
            LeafNode(" "),
            LeafNode("", "img", {"src": "url", "alt": "image"})
        ])
    
    def test_extract_title(self):
        text = "# This is a title "
        self.assertEqual(TextConverter.extract_title(text), "This is a title")

    def test_extract_title_raises(self):
        text = "## no title"
        with self.assertRaises(Exception):
            TextConverter.extract_title(text)