import os
import shutil
from markdown_to_HTML import markdown_to_html_node
import sys



def main():
    
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # Get the base directory path (where this file lives)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the base directory
    source = os.path.join(base_dir, "../static")
    destination = os.path.join(base_dir, "../docs")

    dir_content = os.path.join(base_dir, "../content")
    #index = os.path.join(destination, "index.html")
    template = os.path.join(base_dir, "../template.html")

    copy_static(source, destination)
    generate_pages_recursive(dir_content, template, destination, basepath)
    


def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination)
        else:
            new_destination = os.path.join(destination, item)
            os.mkdir(new_destination)
            copy_static(item_path, new_destination)

def extract_title(markdown):
    lines = markdown.split("\n")
    header = ""
    for line in lines:
        if line.startswith("# "):
            header = line[2:]
            return header.strip()

    raise Exception("No Header Found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        md = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(md)

    html_node = markdown_to_html_node(md)
    html = html_node.to_html()

    converted_template = template.replace("{{ Title }}", title)
    converted_template = converted_template.replace("{{ Content }}", html)
    converted_template = converted_template.replace('href="/', f'href="{basepath}')
    converted_template = converted_template.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)

    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as f:
        f.write(converted_template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        # If file or directory
        if os.path.isfile(item_path):
            if item.endswith(".md"):
                rel_path = os.path.relpath(item_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_path.replace(".md", ".html"))

                generate_page(item_path, template_path, dest_path, basepath)
        # If directory
        else:
            new_content_dir = item_path
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(new_content_dir, template_path, new_dest_dir, basepath)

main()