from textnode import TextNode
from functools import reduce
import shutil
import os
from textconverter import TextConverter

def main():
    copy_files_to_public()

def copy_files_to_public():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    # print(os.listdir())
    os.mkdir("public/")

    copy_file_recursive("static/")

    generate_page("content/index.md", "template.html", "public/index.html")

def copy_file_recursive(directory):
    for i in os.listdir(directory):
        if os.path.isfile(f"{directory}/{i}"):
            shutil.copy(f"{directory}/{i}", f"{directory}/{i}".replace("static", "public"))
            # print(f"Copied {directory}/{i} to {directory.replace('static', 'public')}/{i}")
        else:
            os.mkdir(f"{directory}/{i}".replace("static", "public"))
            copy_file_recursive(f"{directory}/{i}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    with (open(from_path) as f):
        markdown = f.read()
    with (open(template_path) as f):
        template = f.read()
    HTML_string = TextConverter.markdown_to_html_node(markdown).to_html()
    title = TextConverter.extract_title(markdown)
    final_HTML = template.replace("{{ Title }}", title).replace("{{ Content }}", HTML_string)

    full_path = dest_path.split("/")
    curr_path = ""
    for i, val in enumerate(full_path):
        curr_path += f"/val"
        if i < len(val) - 1 and os.path.exists(curr_path):
            os.mkdir(curr_path)

    with (open(dest_path, "w") as f):
        f.write(final_HTML)


if __name__ == "__main__":
    main()