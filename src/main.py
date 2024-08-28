from textnode import TextNode
import shutil
import os

def main():
    copy_files_to_public()

def copy_files_to_public():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    # print(os.listdir())
    os.mkdir("public/")

    copy_file_recursive("static/")

def copy_file_recursive(directory):
    for i in os.listdir(directory):
        if os.path.isfile(f"{directory}/{i}"):
            shutil.copy(f"{directory}/{i}", f"{directory}/{i}".replace("static", "public"))
            # print(f"Copied {directory}/{i} to {directory.replace('static', 'public')}/{i}")
        else:
            os.mkdir(f"{directory}/{i}".replace("static", "public"))
            copy_file_recursive(f"{directory}/{i}")


if __name__ == "__main__":
    main()