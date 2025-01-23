# Obsidian 2 Quarto

For my blogging workstream, I use Obsidian and quarto. 

These are incompatible in some aspects.

This repo is a selection of scripts, which copy the blog to a new directory.


For more background see: https://www.storymelange.com/posts/blogging-with-quarto.html
## Contains
- update_yaml_front_matter.py: to check/update front matter
- copy_to_blog_repo.py: used to work around the qmd/md incompatibility
- resolve_wikiling.py: can be used to modify a wikilink to markdownlink. Not integrated

## Status
Currently, the software requires the blog structure to be like my own. 
The structure is a fairly standard quarto structure, but might not work for everybody.

Many parameters are hardcoded.


## Usage

Either run as python script or integrate into your bash via functions:

```
quarto_publish(){
 python3 obsidian2quarto/cli.py --inputdir=blogdir --outputdir=blog-publish
}

quarto_draft(){
 python3 obsidian2quarto/cli.py --inputdir=blogdir --outputdir=blog-draft --draft_mode True
}
```