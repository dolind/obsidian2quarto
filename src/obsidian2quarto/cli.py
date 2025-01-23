import argparse
from update_yaml_front_matter import modify_markdown_files
from copy_to_blog_repo import copy_files
def main():
    parser = argparse.ArgumentParser(description="Process markdown files to add/remove a 'draft' category.")
    parser.add_argument("--inputdir", help="Base directory containing .md or .qmd files.")
    parser.add_argument("--outputdir", help="Output directory to store modified files.")
    parser.add_argument("--draft_mode", help="Specify if to copy drafts")
    args = parser.parse_args()
    files_changed = modify_markdown_files(args.inputdir  + '/posts/')

    if files_changed:
        print("Files changed. Commit changes and rerun.")
        exit(0)
    copy_files(args.inputdir, args.outputdir, args.draft_mode)


if __name__ == "__main__":
    main()
