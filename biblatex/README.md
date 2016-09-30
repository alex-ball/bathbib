# biblatex-bath: Harvard referencing style as recommended by the University of Bath Library

This package provides a .bst file for using BibTeX to format reference lists in the
[Harvard style][bath-harvard] recommended by the University of Bath Library.

## Installation

### Automated way

A makefile is provided which you can use with the Make utility on UNIX-like systems:

  * Running `make source` generates the derived files
      - README.md
      - bath.bbx
      - biblatex-bath.bib
      - biblatex-bath.ins
  * Running `make` generates the above files and also biblatex-bath.pdf.
  * Running `make inst` installs the files in the user's TeX tree.
    You can undo this with `make uninst`.
  * Running `make install` installs the files in the local TeX tree.
    You can undo this with `make uninstall`.

### Manual way

You only need to follow the first two steps if you have made your own changes to the .dtx file.
The compiled files you need are included in the zip archive.

 1. Run `tex biblatex-bath.dtx` to generate the source files.
 2. Compile biblatex-bath.dtx with LuaLaTeX and BibTeX to generate the documentation.
 3. Move the files to your TeX tree as follows:
      - `source/latex/biblatex-bath`:
        biblatex-bath.dtx,
        (biblatex-bath.ins)
      - `tex/latex/biblatex-bath`:
        bath.bst
      - `doc/latex/biblatex-bath`:
        biblatex-bath.pdf,
        README.md

 4. You may then have to update your installation's file name database
    before TeX and friends can see the files.

[bath-harvard]: http://www.bath.ac.uk/library/infoskills/referencing-plagiarism/harvard-bath-style.html

## Licence

Copyright 2016 University of Bath.

This work consists of the documented LaTeX file biblatex-bath.dtx and a Makefile.

The text files contained in this work may be distributed and/or modified
under the conditions of the [LaTeX Project Public License (LPPL)][lppl],
either version 1.3c of this license or (at your option) any later
version.

This work is `maintained' (as per LPPL maintenance status) by [Alex Ball][me].

[lppl]: http://www.latex-project.org/lppl.txt "LaTeX Project Public License (LPPL)"
[me]: https://github.bath.ac.uk/ab318/bathbib "Alex Ball"

