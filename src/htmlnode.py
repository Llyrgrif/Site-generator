import re
from textnode import *

class HTMLNode:
     def __init__(self, tag=None, value=None, children=None, props=None):
         self.tag = tag
         self.value = value
         self.children = children
         self.props = props

     def to_html(self):
         if self.tag is None:
            return self.value or ""
        
         props_html = ""
         if self.props is not None:
             for prop, value in self.props.items():
                 props_html += f' {prop}="{value}"'
        
         if self.children is None:
             if self.value is None:
                 return f"<{self.tag}{props_html}></{self.tag}>"
             else:
                 return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        
         children_html = ""
         for child in self.children:
             children_html += child.to_html()
        
         return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
         

     def props_to_html(self):
         if not self.props:
             return ""

         props_list = []
         for key, value in self.props.items():
             props_list.append(f' {key}="{value}"')
         return "".join(props_list)

     def __repr__(self):
         print(f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}")

class LeafNode(HTMLNode):
     def __init__(self, tag, value, props=None):
         super().__init__()
         self.tag = tag
         self.value = value
         self.props = props

     def to_html(self):
         if self.value == None:
             raise ValueError
         elif self.tag == None or self.tag == "":
             return self.value
         elif self.tag == "a":
             return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
         elif self.tag == "img":
             return f"<{self.tag}{self.props_to_html()}>"
         return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
     def __init__(self, tag, children, props=None):
         self.tag = tag
         self.children = children
         self.props = props

     def to_html(self):
         if self.tag == None or self.tag == "":
             raise ValueError("Tag cannot be None")
         elif self.children == None or self.children == "":
             raise ValueError("Can't be a parent without children")

         html_tags = f"<{self.tag}>"
         for childs in self.children:
             html_tags += childs.to_html()
         html_tags += f"</{self.tag}>"
         return html_tags

def text_node_to_html_node(text_node):
     TextType_dict = {
         TextType.TEXT: (None, {}),
         TextType.BOLD: ("b", {}),
         TextType.ITALIC: ("i", {}),
         TextType.CODE: ("code", {}),
         TextType.LINK: ("a", {"href": None}),
         TextType.IMAGE: ("img", {"src": None, "alt": None})
     }

     if text_node.text_type in TextType_dict:
         tag, props = TextType_dict[text_node.text_type]
         if text_node.text_type == TextType.LINK:
            props["href"] = text_node.url
         elif text_node.text_type == TextType.IMAGE:
            props["src"] = text_node.url
            props["alt"] = text_node.text
         node = LeafNode(tag, text_node.text, props)
         return node
     else:
         raise Exception("Not a type of textnode")



def split_nodes_delimiter(old_nodes, delimiter, text_type):
     new_list = []
     for node in old_nodes:
         if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

         splitted_nodes = node.text.split(delimiter)
         if len(splitted_nodes) == 1:
            new_list.append(node)
            continue

         for i in  range(len(splitted_nodes)):
            if splitted_nodes[i] == "":
                continue
            if i % 2 == 0:
                if splitted_nodes[i]:
                    new_list.append(TextNode(splitted_nodes[i], TextType.TEXT))
            else:
                if splitted_nodes[i]:
                    new_list.append(TextNode(splitted_nodes[i], text_type))
     return new_list

def extract_markdown_images(text):
     matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
     return matches

def extract_markdown_links(text):
     matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
     return matches

def split_nodes_image(old_nodes):
     new_nodes = []
     for old_node in old_nodes:
         if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
         images = extract_markdown_images(old_node.text)
        
         if not images:
            new_nodes.append(old_node)
            continue
            
        
         remaining_text = old_node.text
         for alt_text, url in images:
             image_markdown= f"![{alt_text}]({url})"

             parts = remaining_text.split(image_markdown, 1)
             if parts[0]:
                 new_nodes.append(TextNode(parts[0],TextType.TEXT))
             new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
             if len(parts) > 1:
                 remaining_text = parts[1]
             else:
                 remaining_text = ""
         if remaining_text:
              new_nodes.append(TextNode(remaining_text, TextType.TEXT))
     return new_nodes


def split_nodes_link(old_nodes):
     new_nodes = []
     for old_node in old_nodes:
         if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
         links = extract_markdown_links(old_node.text)
        
         if not links:
            new_nodes.append(old_node)
            continue
            
        
         remaining_text = old_node.text
         for text, url in links:
             links_markdown= f"[{text}]({url})"

             parts = remaining_text.split(links_markdown, 1)
             if parts[0]:
                 new_nodes.append(TextNode(parts[0],TextType.TEXT))
             new_nodes.append(TextNode(text, TextType.LINK, url))
             if len(parts) > 1:
                 remaining_text = parts[1]
             else:
                 remaining_text = ""
         if remaining_text:
              new_nodes.append(TextNode(remaining_text, TextType.TEXT))
     return new_nodes

def text_to_textnodes(text):
     nodes =[TextNode(text, TextType.TEXT)]
     nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
     nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
     nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
     nodes = split_nodes_image(nodes)
     nodes = split_nodes_link(nodes)
     
     return nodes