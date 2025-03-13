import nbformat
import glob
import os
import argparse


def merge_notebooks(source_dir, target_dir):
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Find all notebooks in the source directory, sorted numerically
    notebook_files = sorted(glob.glob(os.path.join(source_dir, "*.ipynb")))

    # Ignore "merged.ipynb" if it already exists in the source
    notebook_files = [nb for nb in notebook_files if not nb.endswith("merged.ipynb")]

    if not notebook_files:
        print("No valid Jupyter notebooks found in the source directory.")
        return

    merged_nb = nbformat.v4.new_notebook()

    for nb_file in notebook_files:
        with open(nb_file) as f:
            nb = nbformat.read(f, as_version=4)
            merged_nb.cells.extend(nb.cells)  # Merge all cells

    # Save the merged notebook in the target directory
    merged_path = os.path.join(target_dir, "merged.ipynb")
    with open(merged_path, "w") as f:
        nbformat.write(merged_nb, f)

    print(f"Merged notebook saved as {merged_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple Jupyter notebooks into one, ignoring 'merged.ipynb'.")
    parser.add_argument("source_dir", help="Directory containing Jupyter notebooks to merge.")
    parser.add_argument("target_dir", nargs="?", default=os.getcwd(),
                        help="Target directory to save the merged notebook (default: current directory).")

    args = parser.parse_args()
    merge_notebooks(args.source_dir, args.target_dir)
