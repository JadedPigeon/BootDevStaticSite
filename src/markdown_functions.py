from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) > 1:
                #check for even number of delimiters which splits parts into an odd number. ie "before **bold word** after" will be ["before", "bold word", "after"]
                if len(parts) % 2 == 0:
                    raise Exception(f"Invalid markdown: Unmatched delimiter {delimiter}")
                else:
                    for i in range(len(parts)):
                        if i % 2 == 0:
                            new_nodes.append(TextNode(parts[i], TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(parts[i], text_type))
            else:
                new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    image_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches

def extract_markdown_links(text):
    links_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links_matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        all_images_altText_image = extract_markdown_images(text)
        if all_images_altText_image == []:
            new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            for image in all_images_altText_image:
                image_alt = image[0]
                image_url = image[1]
                sections = text.split(f"![{image_alt}]({image_url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                text = sections[1]
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        links_text_url = extract_markdown_links(text)
        if links_text_url == []:
            new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            for link in links_text_url:
                link_text = link[0]
                link_url = link[1]
                sections = text.split(f"[{link_text}]({link_url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                text = sections[1]
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

