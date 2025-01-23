import os
import shutil
import re
import yaml


def has_valid_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml_match = re.match(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if yaml_match:
        yaml_content, _ = yaml_match.groups()
        yaml_data = yaml.safe_load(yaml_content) or {}
        if yaml_data.get('draft'):  # Check if 'draft: true'
            print(f"Skipping, due to draft: {file_path}")
            return False
    else:
        print(f"Skipping, no YAML header:  {file_path}, ")
        return False
    return True


def copy_files(src, dst, debug=False):
    print(f"Synchronizing {src} to {dst} with .md files renamed to .qmd")

    # Keep track of destination files for deletion
    dst_files = set()

    # Walk through the source directory
    for root, dirs, files in os.walk(src):
        if '.git' in root or '.quarto' in root:
            continue

        for name in files:
            ext = os.path.splitext(name)[1].lower()
            src_path = os.path.join(root, name)
            rel_path = os.path.relpath(root, src).lstrip("./")

            # Check that it is a valid yaml file
            if ext in ['.md'] and not debug:
                if not has_valid_yaml(src_path):
                    continue

            # Rename .md to .qmd
            if 'qmd.md' in name:
                name = name.replace('.qmd.md', '.qmd')
                ext = '.qmd'

            dst_path = os.path.join(dst, rel_path, name)
            dst_files.add(dst_path)

            # Skip copying if the file exists and is the same size
            if os.path.exists(dst_path) and os.path.getsize(src_path) == os.path.getsize(dst_path):
                continue


            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"Copied: {src_path} -> {dst_path}")

    # Walk through the destination directory to delete files not in source
    for root, dirs, files in os.walk(dst):
        if '.git' in root or '.quarto' in root or 'docs' in root:
            continue
        for name in files:
            dst_path = os.path.join(root, name)
            if dst_path not in dst_files:
                os.remove(dst_path)
                print(f"Deleted: {dst_path}")

    print("Synchronization complete.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <dest_dir>")
        sys.exit(1)
    copy_files(sys.argv[1], sys.argv[2])
