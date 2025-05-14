from textnode import TextNode, TextType
from blocks import *
from pathlib import Path
import os
import re
import shutil
import sys

basepath = sys.argv[0]

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    recursive_copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs")

    #print(node)


def recursive_copy(source_dir, dest_dir, first_call=True):
	if first_call and os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
		os.makedirs(dest_dir)
	elif not os.path.exist(dest_dir):
		os.makedirs(dest_dir)

	items = os.listdir(source_dir)
    
	for item in items:
		source_path = os.path.join(source_dir, item)
		dest_path = os.path.join(dest_dir, item)
        
		if os.path.isfile(source_path):
			shutil.copy(source_path, dest_path)
			print(f"Copied: {source_path} to {dest_path}")
		else:
			os.makedirs(dest_path, exist_ok=True)
			recursive_copy(source_path, dest_path)

def extract_title(markdown):
	lines = markdown.split("\n")
	first_line = lines[0]
	if first_line.startswith("# "):
		stripped_title = first_line[2:].strip()
		return stripped_title
	else:
		raise Exception("Isn't a h1 title")
	
def generate_page(from_path, template_path, dest_path):
	print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
	with open(from_path, "r") as markdown_file:
		markdown_content = markdown_file.read()
		html_string = markdown_to_html_node(markdown_content)
		title = extract_title(markdown_content)
		
	with open(template_path, "r") as template_file:
		template_content = template_file.read()
	
	replaced_title = template_content.replace("{{ Title }}", title)
	replaced_content = replaced_title.replace("{{ Content }}", html_string.to_html())
	replaced_href = replaced_content.replace('href="/', 'href="{basepath}')
	replaced_src = replaced_href.replace('src="/', 'src="{basepath}')
	if os.path.exists(os.path.dirname(dest_path)) == False:
		os.makedirs(os.path.dirname(dest_path))

	with open(dest_path, "w") as f:
		f.write(replaced_src)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

	if os.path.isfile(dir_path_content):
		generate_page(dir_path_content, template_path, dest_dir_path)
	else:
		files = os.listdir(dir_path_content)
		for file in files:
			source_path = os.path.join(dir_path_content, file)
			dest_path = os.path.join(dest_dir_path, file)
			replaced_dest = dest_path.replace(".md", ".html")

			new_path = generate_pages_recursive(source_path, template_path, replaced_dest)

	#generate_page(entry, template_path, dest_dir_path)


if __name__ == "__main__":
	main()

