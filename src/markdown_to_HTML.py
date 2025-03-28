from htmlnode import *
from blocks import *
from markdown_functions import *
import re

def markdown_to_html_node(markdown):
    #init
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        #-----PARAGRAPHGS-----
        if block_type == BlockType.PARAGRAPH:
            #Convert to html_nodes
            text_nodes = text_to_textnodes(block.replace("\n", " "))
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            p_node = ParentNode("p", html_nodes)
            children.append(p_node)

        #-----HEADERS-----
        elif block_type == BlockType.HEADING:
            #check what header it is
            header_number = 0
            for char in block:
                if char == "#":
                    header_number += 1
                else:
                    break
            #get the text after the header
            header_text = block[header_number:].strip()

            text_nodes = text_to_textnodes(header_text)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]

            heading_node = ParentNode(f"h{header_number}", html_nodes)
            children.append(heading_node)

        #-----CODE-----
        elif block_type == BlockType.CODE:
            #get the content
            code_text = "\n".join(block.split("\n")[1:-1])

            #created a text node. Note we're not parsing it further. IE checking for bold
            text_node = TextNode(code_text, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)

            code_node = ParentNode("code", [html_node])
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)

        #-----QUOTE-----
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_lines = []
            for line in lines:
                quote_lines.append(line.replace(">", "", 1).strip())
                
            quote = "\n".join(quote_lines)
            text_nodes = text_to_textnodes(quote)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            quote_node = ParentNode("blockquote", html_nodes)
            children.append(quote_node)

        #-----UNORDERED LIST-----
        elif block_type == BlockType.UNORDERED_LIST:
            list_item = block.split("\n")
            ulist_nodes = []
            for item in list_item:
                if item.strip():
                    li_content = item.replace("-", "", 1).strip()
                    li_text_nodes = text_to_textnodes(li_content)
                    li_html_nodes = [text_node_to_html_node(node) for node in li_text_nodes]
                    li_node = ParentNode("li", li_html_nodes)
                    ulist_nodes.append(li_node)
            lu_node = ParentNode("ul", ulist_nodes)
            children.append(lu_node)
        
        #------Ordered List-----
        elif block_type == BlockType.ORDERED_LIST:
            list_item = block.split("\n")
            olist_nodes = []
            for item in list_item:
                if item.strip():
                    li_content = re.sub(r"^\d+\.\s*", "", item)
                    li_text_nodes = text_to_textnodes(li_content)
                    li_html_nodes = [text_node_to_html_node(node) for node in li_text_nodes]
                    li_node = ParentNode("li", li_html_nodes)
                    olist_nodes.append(li_node)
            ou_node = ParentNode("ol", olist_nodes)
            children.append(ou_node)

        #-----Catch-----
        else:
            raise Exception("Invalid block_type passed into markdown_to_html_node") 

    #Create the parent node and add all children
    parent_node = ParentNode("div", children)
    return parent_node
