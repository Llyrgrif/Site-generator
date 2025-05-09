from textnode import TextNode, TextType
import os
import shutil

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    copy = recursive_copy("/home/pau/workspace/github.com/Llyrgrif/site_generator/static", "/home/pau/workspace/github.com/Llyrgrif/site_generator/public")

    print(copy)
    print(node)


def recursive_copy(source_dir, dest_dir):
	#destination = dest_dir
	tree = []
	print(f"Processing: {source_dir}")
	if os.path.isfile(source_dir) == True:
		tree.append(source_dir)
		print(f"Appended file 2: {source_dir}")
		return tree
	else:
		source = os.listdir(source_dir)
		for files in source:
			path = f"{source_dir}/{files}"
			print(f"Looking at: {path}")
			if os.path.isfile(files) == True:
				return tree
			else:
				tree.append(files)
				print(f"Appended: {files}")
				result = recursive_copy(path)
				print(f"Recursive result: {result}")
				tree.extend(result)
		return tree

if __name__ == "__main__":
	main()

