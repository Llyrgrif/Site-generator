from enum import Enum
from htmlnode import *
from textnode import *
import re

def markdown_to_blocks(markdown):
    block_list = []
    parts = markdown.split("\n\n")
    for markdowns in parts:
        if markdowns == "":
            continue
        else:
            block = markdowns.strip()
            block_list.append(block)
    return block_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):

    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("-") for line in lines):
        return BlockType.UNORDERED_LIST

    for i in range(len(lines)):
        if lines and all(line.startswith(f"{(i + 1)}. ") for i, line in enumerate(lines)):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def  markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
        if block_type == BlockType.CODE:
            pre_node, code_node = create_htmlnode(block_type, block)
            code_content = extract_code_content(block)
            text_node = TextNode(code_content, TextType.TEXT)
            html_node = text_node_to_html_node(text_node) 
            code_node.children = [html_node]
            all_nodes.append(pre_node)
        else:
            htmlnode = create_htmlnode(block_type, block)
            htmlnode.children = text_to_children(block)
            all_nodes.append(htmlnode)
    parent_div = HTMLNode("div", None, all_nodes, None)
    return parent_div

def create_htmlnode(block_type, block_text):
    tag_dict = {
        BlockType.PARAGRAPH: "p",
        BlockType.HEADING: "#",
        BlockType.CODE: ("pre", "code"),
        BlockType.QUOTE: "blockquote",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.ORDERED_LIST: "ol"
    }
    
    if block_type in tag_dict:
        tag = tag_dict[block_type]
        if block_type == BlockType.HEADING:
            type_of_heading = re.findall("#", block_text)
            tag = f"h{len(type_of_heading)}"
        elif block_type == BlockType.CODE:
            code_node = HTMLNode(tag_dict[BlockType.CODE][1], None, None, None)
            pre_node = HTMLNode(tag_dict[BlockType.CODE][0], None, [code_node], None)
            return pre_node, code_node
        return HTMLNode(tag, None, None, None)


def text_to_children(block):
    block_type = block_to_block_type(block)
    processed_block = block
    if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:

        lines = block.split("\n")
        list_items = []
        for line in lines:

            if block_type == BlockType.UNORDERED_LIST:
                item_text = re.sub(r'^-\s+', '', line)
            else: 
                item_text = re.sub(r'^\d+\.\s+', '', line)

            item_text_nodes = text_to_textnodes(item_text)
            item_html_nodes = [text_node_to_html_node(node) for node in item_text_nodes]

            li_node = HTMLNode("li", None, item_html_nodes, None)
            list_items.append(li_node)
            
        return list_items
    
    elif block_to_block_type(block) == BlockType.HEADING:
        text = re.sub(r'^#+\s+', '', processed_block)

    elif block_to_block_type(block) == BlockType.QUOTE:
        text = re.sub(r'^>\s+', '', processed_block)
    else:
        text = processed_block
    
    text_nodes = text_to_textnodes(text)
    
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes

def extract_code_content(content):
    content = content.strip()
    first_newline = content.find('\n')
    if first_newline == -1:
        return ""    

    last_backticks = content.rfind('```')
    if last_backticks == 0: 
        code_content = content[first_newline+1:]
    else:
        code_content = content[first_newline+1:last_backticks]
    
    return code_content

            


