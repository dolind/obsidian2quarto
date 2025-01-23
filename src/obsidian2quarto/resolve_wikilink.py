import os
import re

import re
import sys
from tempfile import TemporaryDirectory


def wikilink_to_markdown(wikilink):
    """
    Converts a given MediaWiki-style link to a Markdown link.
    """
    # Match external links with custom text
    print(wikilink)
    if re.match(r"\[http[s]?:\/\/[^\s]+\s+[^\]]+\]", wikilink):
        match = re.match(r"\[([^\s]+)\s+(.+)\]", wikilink)
        return f"[{match.group(2)}]({match.group(1)})"

    # Match external links without custom text
    if re.match(r"\[http[s]?:\/\/[^\]]+\]", wikilink):
        match = re.match(r"\[([^\]]+)\]", wikilink)
        return f"[{match.group(1)}]({match.group(1)})"

    # Match internal links with a section and custom text
    if re.match(r"\[\[[^\|]+\#[^\|]+\|[^\]]+\]\]", wikilink):
        match = re.match(r"\[\[([^\|]+)\#([^\|]+)\|([^\]]+)\]\]", wikilink)
        return f"[{match.group(3)}]({match.group(1)}#{match.group(2)})"

    # Match internal links with a section only
    if re.match(r"\[\[[^\|]+\#[^\]]+\]\]", wikilink):
        match = re.match(r"\[\[([^\|]+)\#([^\]]+)\]\]", wikilink)
        return f"[{match.group(1)}]({match.group(1)}#{match.group(2)})"

    # Match internal links with custom display text
    if re.match(r"\[\[[^\|]+\|[^\]]+\]\]", wikilink):
        match = re.match(r"\[\[([^\|]+)\|([^\]]+)\]\]", wikilink)
        return f"[{match.group(2)}]({match.group(1)})"

    # Match basic internal links
    if re.match(r"\[\[[^\]]+\]\]", wikilink):
        match = re.match(r"\[\[([^\]]+)\]\]", wikilink)
        return f"[{match.group(1)}]({match.group(1)})"

    # If no pattern matches, return the input unchanged
    return wikilink

def convert_link_group(match):
    for link in match.groups():
        print(link)

def convert_wiki_to_markdown(content):
    """Convert Wiki-style [[links]] to Markdown-style [links](path)."""

    return re.sub(r"\[\[[^\]]+\]\]", lambda match: wikilink_to_markdown(match.group(0)), content)


def process_file(file_path, temp_dir):
    """Process a file and write the modified version to a temporary directory."""
    print("Processing", file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    modified_content = convert_wiki_to_markdown(content)
    print("Writing", modified_content)
    # Write the modified content to the temporary directory
    temp_file_path = os.path.join(temp_dir, os.path.relpath(file_path))
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(modified_content)

    print(f"Processed: {file_path} -> Temporary: {temp_file_path}")
    return temp_file_path


def process_files_in_temp(files_to_process):
    """Process all files and store them in a temporary directory."""
    print(files_to_process)
    with TemporaryDirectory() as temp_dir:
        temp_files = []
        for file_path in files_to_process:
            temp_files.append(process_file(file_path, temp_dir))

        # Return the temporary directory and the list of processed files
        return temp_dir, temp_files


if __name__ == "__main__":
    # Quarto passes files to process as arguments
    files_to_process = os.getenv("QUARTO_PROJECT_INPUT_FILES").strip().split("\n")
    if files_to_process:
      temp_dir, temp_files = process_files_in_temp(files_to_process)

      # Print out the temporary directory for Quarto to use
      print(f"Temporary directory for rendered files: {temp_dir}")
# Example usage:
# Replace 'your-vault-folder' with your Obsidian vault path
# resolve_wiki_links('your-vault-folder', 'output-folder')