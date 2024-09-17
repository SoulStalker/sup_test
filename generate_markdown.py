import os


def generate_directory_structure(root_dir, exclude_folders=None, level=0):
    if exclude_folders is None:
        exclude_folders = []

    result = ""
    indent = "    " * level
    for item in sorted(os.listdir(root_dir)):
        item_path = os.path.join(root_dir, item)
        if "__" in item:
            item = item.replace("__", "\\_\\_")

        # Пропуск скрытых папок и папок из списка исключений
        if os.path.isdir(item_path) and (item.startswith(".") or item in exclude_folders):
            continue

        # Пропуск файлов с расширением .pyc
        if os.path.isfile(item_path) and item.endswith(".pyc"):
            continue

        if os.path.isdir(item_path):
            result += f"{indent}- {item}/\n"
            result += generate_directory_structure(item_path, exclude_folders, level + 1)

        else:
            result += f"{indent}- {item}\n"
    return result


if __name__ == "__main__":
    root_directory = "."
    exclude = [".git", ".idea", ".venv", "\\_\\_pycache\\_\\_"]
    structure = generate_directory_structure(root_directory, exclude)

    with open("directory_structure.md", "w") as file:
        file.write(structure)
    print("Структура папок записана в directory_structure.md")
