import os

import yaml
import re


def shorten_title_with_hyphens(title):
    # Remove non-letter characters
    title = re.sub(r'[^a-zA-Z\s]', '', title)
    # Remove timestamp (assumes it starts with digits)
    title = re.sub(r'^\d{8,}', '', title).strip()
    # Capitalize words and connect with hyphens
    words = title.split()
    meaningful_title = '-'.join(word.lower() for word in words)
    return meaningful_title

def modify_markdown_files(base_dir):
    any_file_changed = False
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.endswith((".qmd", ".md")):
                file_path = os.path.join(root, file_name)
                file_changed = process_file(file_path)
                if file_changed:
                    any_file_changed = True
    return any_file_changed

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content_changed = False
    yaml_match = re.match(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if  yaml_match:
        yaml_content, rest_of_file = yaml_match.groups()
        yaml_data = yaml.safe_load(yaml_content) or {}
    else:
        print('No yaml front matter for {}'.format(file_path))
        yaml_data, rest_of_file = {}, content
        yaml_data.setdefault("title", "")
        yaml_data.setdefault("draft", True)
        yaml_data.setdefault("description", "")
        yaml_data.setdefault("date", '')
        yaml_data.setdefault("categories",['draft'])
        yaml_data.setdefault("execute", {"message": False, "warning": False})
        yaml_data.setdefault("editor_options", {"chunk_output_type": "console"})
        yaml_data.setdefault("output-file", '')
        content_changed = True
    # Check for draft
    is_draft = yaml_data.get("draft", False)

    # Adjust categories
    categories = yaml_data.get("categories", [])
    if isinstance(categories, str):
        categories = [categories]

    if is_draft:
        if "draft" not in categories:
            categories.append("draft")
            print('Draft tag missing for {}'.format(file_path))
            content_changed = True
    else:
        if "draft" in categories:
            content_changed = True
        categories = [cat for cat in categories if cat != "draft"]

    if categories != yaml_data["categories"]:
        content_changed = True
        yaml_data["categories"] = categories

    correct_output_file = shorten_title_with_hyphens(yaml_data['title'])
    if  'output-file' not in yaml_data.keys() or yaml_data['output-file'] == '' or yaml_data['output-file'] != correct_output_file:
        print('Wrong output_file for {}'.format(file_path))
        content_changed = True
        yaml_data['output-file'] = correct_output_file

    new_yaml_content = yaml.dump(yaml_data, sort_keys=False).strip()
    new_content = f"---\n{new_yaml_content}\n---\n{rest_of_file.strip()}\n"
    if content_changed:
        print("changing content for {}".format(file_path))
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

    if content_changed:
        return True
    else:
        return False
