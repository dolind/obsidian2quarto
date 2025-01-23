import re
import shutil
from pathlib import Path

import pytest
import yaml

import src.obsidian2quarto.update_yaml_front_matter
from src.obsidian2quarto.resolve_wikilink import wikilink_to_markdown


def compare_files(processed_file, expected_file):
    with open(processed_file, 'r') as pf, open(expected_file, 'r') as ef:
        processed_content = pf.read()
        expected_content = ef.read()

    # Extract YAML front matter and the rest of the content
    def extract_yaml_and_content(file_content):
        match = re.match(r"---\n(.*?)\n---\n(.*)", file_content, re.DOTALL)
        if not match:
            return None, file_content.strip()  # No YAML found
        yaml_part, content_part = match.groups()
        return yaml.safe_load(yaml_part), content_part.strip()

    processed_yaml, processed_body = extract_yaml_and_content(processed_content)
    expected_yaml, expected_body = extract_yaml_and_content(expected_content)

    # Compare YAML dictionaries
    if processed_yaml != expected_yaml:
        print(f"YAML mismatch in {processed_file}:")
        print(f"Processed YAML: {processed_yaml}")
        print(f"Expected YAML: {expected_yaml}")
        assert False, "YAML mismatch"

    # Compare body content
    if processed_body != expected_body:
        print(f"Body content mismatch in {processed_file}:")
        print(f"Processed Body: {repr(processed_body)}")
        print(f"Expected Body: {repr(expected_body)}")
        assert False, "Body content mismatch"

def test_modify_markdown_no_draft_tag(tmp_path: Path):
    # Setup: copy input files to tmp_path
    input_dir = Path(__file__).parent / "input_files"
    expected_dir = Path(__file__).parent / "expected_files"
    for file_name in ["no_draft_tag.md"]:
        shutil.copy(input_dir / file_name, tmp_path / file_name)

    src.obsidian2quarto.update_yaml_front_matter.modify_markdown_files(tmp_path)
    # Compare files with expected output

    for file_name in ["no_draft_tag.md"]:
        processed_file = tmp_path / file_name
        expected_file = expected_dir / file_name
        # Use filecmp or read and compare content

        compare_files(processed_file,expected_file)


def test_modify_markdown_no_yaml(tmp_path: Path):
    # Setup: copy input files to tmp_path
    input_dir = Path(__file__).parent / "input_files"
    expected_dir = Path(__file__).parent / "expected_files"
    for file_name in ["no_yaml.md"]:
        shutil.copy(input_dir / file_name, tmp_path / file_name)

    src.obsidian2quarto.update_yaml_front_matter.modify_markdown_files(tmp_path)
    # Compare files with expected output

    for file_name in ["no_yaml.md"]:
        processed_file = tmp_path / file_name
        expected_file = expected_dir / file_name
        # Use filecmp or read and compare content

        compare_files(processed_file,expected_file)

def test_modify_markdown_wrong_draft_tag(tmp_path: Path):
    # Setup: copy input files to tmp_path
    input_dir = Path(__file__).parent / "input_files"
    expected_dir = Path(__file__).parent / "expected_files"
    for file_name in ["wrong_draft_tag.md"]:
        shutil.copy(input_dir / file_name, tmp_path / file_name)

    src.obsidian2quarto.update_yaml_front_matter.modify_markdown_files(tmp_path)
    # Compare files with expected output

    for file_name in ["wrong_draft_tag.md"]:
        processed_file = tmp_path / file_name
        expected_file = expected_dir / file_name
        # Use filecmp or read and compare content

        compare_files(processed_file,expected_file)


@pytest.mark.parametrize("wikilink, markdown", [
    ("[[Page Name]]", "[Page Name](Page Name)"),
    ("[[Page Name|Display Text]]", "[Display Text](Page Name)"),
    ("[[Page Name#Section Name]]", "[Page Name](Page Name#Section Name)"),
    ("[[Page Name#Section Name|Display Text]]", "[Display Text](Page Name#Section Name)"),
    ("[[Category:Category Name]]", "[Category:Category Name](Category:Category Name)"),
    ("[[File:File Name]]", "[File:File Name](File:File Name)"),
    ("[[interwiki-prefix:Page Name]]", "[Page Name](interwiki-prefix:Page Name)"),
    ("[[LanguageCode:Page Name]]", "[Page Name](LanguageCode:Page Name)"),
    ("[[Nonexistent Page]]", "[Nonexistent Page](Nonexistent Page)"),
    ("[[Namespace:Page Name]]", "[Page Name](Namespace:Page Name)"),
    ("[[Namespace:Page Name|Page Name]]", "[Page Name](Namespace:Page Name)"),
    ("[http://example.com]", "[http://example.com](http://example.com)"),
    ("[http://example.com Custom Text]", "[Custom Text](http://example.com)"),
])
def test_wikilink_to_markdown(wikilink, markdown):
    # Replace this with the actual function once implemented
    result = wikilink_to_markdown(wikilink)
    assert result == markdown
