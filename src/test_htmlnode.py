import unittest
from main import *
from htmlnode import *
from textnode import *
from blocks import *

class TestHTMLNode(unittest.TestCase):

      def test_props(self):
         node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
         self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

      def test_leaf_to_html_a(self):
         node = LeafNode("a", "como estamos??", {"href": "https://www.mohammed_el_meon.com"}).to_html()
         self.assertEqual(node, '<a href="https://www.mohammed_el_meon.com">como estamos??</a>')

      def test_leaf_to_html_p(self):
         node = LeafNode("p", "Hello, world!")
         self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

      def test_leaf_to_html_h1(self):
         node = LeafNode("h1", "this is a header!")
         self.assertEqual(node.to_html(), "<h1>this is a header</h1>")

      def test_leaf_to_html_h1(self):
         node = LeafNode("", "this should be raw text")
         self.assertEqual(node.to_html(), "this should be raw text")


      def test_to_html_with_children(self):
         child_node = LeafNode("span", "child")
         parent_node = ParentNode("div", [child_node])
         self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

      def test_to_html_with_grandchildren(self):
         grandchild_node = LeafNode("b", "grandchild")
         child_node = ParentNode("span", [grandchild_node])
         parent_node = ParentNode("div", [child_node])
         self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
         )

      def test_text(self):
         node = TextNode("This is a text node", TextType.TEXT)
         html_node = text_node_to_html_node(node)
         self.assertEqual(html_node.tag, None)
         self.assertEqual(html_node.value, "This is a text node")

      def test_split_nodes(self):
         node = TextNode("this is text with _bold_ text", TextType.TEXT)
         new_nodes = split_nodes_delimiter([node], "_", TextType.BOLD)
         self.assertEqual(new_nodes, [
            TextNode("this is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),])

      def test_extract_markdown_images(self):
         matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
         self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

      def test_split_images(self):
         node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
         )
         new_nodes = split_nodes_image([node])
         self.assertListEqual(
            [
               TextNode("This is text with an ", TextType.TEXT),
               TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
               TextNode(" and another ", TextType.TEXT),
               TextNode(
                   "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
               ),
            ],
            new_nodes,
         )

      def test_text_to_nodes(self):
         node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
         new_node = text_to_textnodes(node)
         self.assertEqual(new_node, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
            )
      def test_markdown_to_blocks(self):
         md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

            - This is a list
- with items
"""
         blocks = markdown_to_blocks(md)
         self.assertEqual(
            blocks,
            [
               "This is **bolded** paragraph",
               "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
               "- This is a list\n- with items",
            ],
         )

      def test_block_to_blocktype_heading(self):
         heading = "### this is a heading"
         block = block_to_block_type(heading)
         self.assertEqual(block, BlockType.HEADING)

      def test_block_to_blocktype_quote(self):
         quote = ">this is a quote\n>this is another quote"
         block = block_to_block_type(quote)
         self.assertEqual(block, BlockType.QUOTE)

      def test_block_to_blocktype_ordered_list(self):
         or_list = "1. this is the firts item of a list\n2. this is the second item of a list\n3. this is the third item of a list"
         block = block_to_block_type(or_list)
         self.assertEqual(block, BlockType.ORDERED_LIST)

      def test_block_to_blocktype_paragraph(self):
         paragraph = "this is a paragraph"
         block = block_to_block_type(paragraph)
         self.assertEqual(block, BlockType.PARAGRAPH)

      def test_paragraphs(self):
         md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

         node = markdown_to_html_node(md)
         html = node.to_html()
         self.assertEqual(
         html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
         )

         def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
      
      def test_extract_title(self):
         title = extract_title("# Tolkien Fan Club")
         self.assertEqual(title,"Tolkien Fan Club")
         
         
