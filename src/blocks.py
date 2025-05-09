from enum import Enum
from htmlnode import *
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
            text_node = TextNode(code_content, "text")
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
        BlockType.HEADING: "",
        BlockType.CODE: ("pre", "code"),
        BlockType.QUOTE: "blockquote",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.ORDERED_LIST: "ol"
    }
    
    if block_type in tag_dict:
        tag = tag_dict[block_type]
        if block_type == "heading":
            type_of_heading = re.findall("#", block_text)
            tag = f"h{len(type_of_heading)}"
        elif block_type == "code":
            code_node = HTMLNode(tag_dict["code"][1], None, None, None)
            pre_node = HTMLNode(tag_dict["code"][0], None, [code_node], None)
            return pre_node, code_node
        node = HTMLNode(tag, None, None, None)
        return node

def text_to_children(block):
    processed_block = block
    if block_to_block_type(block) == "heading":
        text = re.sub(r'^#+\s+', '', processed_block)
    elif block_to_block_type(block) == "unordered_list":
        text = re.sub(r'^-\s+', '', processed_block)
    elif block_to_block_type(block) == "ordered_list":
        text = re.sub(r'^\d+\.\s+', '', processed_block)
    elif block_to_block_type(block) == "quote":
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

            


