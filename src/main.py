from textnode import TextNode, TextType
import os
import shutil

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    copy = recursive_copy("/home/pau/workspace/github.com/Llyrgrif/site_generator/static", "/home/pau/workspace/github.com/Llyrgrif/site_generator/public")

    print(copy)
    print(node)


def recursive_copy(source_dir, dest_dir):
	if os.path.exists(dest_dir):
    	shutil.rmtree(dest_dir)

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

if __name__ == "__main__":
	main()

