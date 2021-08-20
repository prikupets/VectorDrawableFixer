import sys
import os

ARG_RECURSIVELY = "-r"
VECTOR_DRAWABLE_EXTENSION = ".xml"
FILL_TYPE_FIX = 'android:fillType="evenOdd"'
INCORRECT_FILL_TYPE = 'android:fillType="evenOdd"'
PATH_TAG = "<path"
TAG_ENDING = "/>"


def fix_tag_fill_type(tag_content) -> str:
    if INCORRECT_FILL_TYPE in tag_content:
        tag_content = tag_content.replace(INCORRECT_FILL_TYPE, FILL_TYPE_FIX)

    if FILL_TYPE_FIX not in tag_content:
        indent = tag_content[tag_content.rfind('\n'):tag_content.rfind("android")]
        if '\n' not in indent:
            indent += "\n"

        tag_content += f"{indent}{FILL_TYPE_FIX}"

    print(" [Result]:")
    print(tag_content)

    return tag_content


def try_fix_file_fill_type(file_path) -> bool:
    def read_file():
        with open(file_path, "r") as file_to_read:
            return file_to_read.readlines()

    def save_file():
        with open(file_path, "w") as file_to_write:
            file_to_write.write(file_result_content)

    fixed_any = False

    file_lines = read_file()
    file_result_content = ''.join(file_lines)

    tag_start = -1
    line_index = -1

    for line in file_lines:
        line_index += 1

        if PATH_TAG in line:
            tag_start = line_index

        if TAG_ENDING in line and tag_start != -1:
            tag_content = ''.join(file_lines[tag_start:line_index + 1])[:-len(TAG_ENDING) - 1]
            tag_start = -1

            fixed_tag_content = fix_tag_fill_type(tag_content)
            if tag_content != fixed_tag_content:
                file_result_content = file_result_content.replace(tag_content, fixed_tag_content)
                fixed_any = True

    if fixed_any:
        save_file()

    return fixed_any


def try_fix(file_path) -> bool:
    return try_fix_file_fill_type(file_path)


def fix_files(fixed_files, dir_path, recursively):
    for file_name in os.listdir(dir_path):
        file_path = dir_path + "/" + file_name

        if os.path.isdir(file_path):
            if recursively:
                fix_files(fixed_files, file_path, recursively)
            continue

        if VECTOR_DRAWABLE_EXTENSION not in file_name:
            continue

        print(f"Fixing {file_name}")
        if try_fix(file_path):
            fixed_files.append(file_name)


def validate_args():
    if len(sys.argv) <= 1:
        print("Usage: python vectorfix.py vector_drawables_directory_path (-r to do recursively)")
        exit(1)

    if not os.path.isdir(sys.argv[1]):
        print("Incorrect directory")
        exit(1)


def main():
    validate_args()
    dir_path = sys.argv[1]
    recursively = ARG_RECURSIVELY in sys.argv

    fixed_files = []
    fix_files(fixed_files, dir_path, recursively)
    print(f"Fixed: {fixed_files}")


main()
