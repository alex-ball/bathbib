# biblatex-bath: Harvard referencing style as recommended by the University of Bath Library

This package provides a [biblatex] style to format reference lists in the
[Harvard style][bath-harvard] recommended by the University of Bath Library.

## Installation

You can use this style simply by copying all the `.bbx`, `.cbx`, `.dbx` and
`.lbx` files into your working directory, that is, the directory holding the
main `.tex` file for your document. If you want the style to be available for
all your documents without having to copy the files over each time, you can
install them using the instructions below.

### Managed way

The latest stable release of biblatex-bath has been packaged for TeX Live and
MiKTeX. If you are running TeX Live and have `tlmgr` installed, you can install
the package simply by running `tlmgr install biblatex-bath`. If you are running
MiKTeX, you can install the package by running `mpm --install=biblatex-bath`.
Both `tlmgr` and `mpm` have GUI versions that you might find friendlier.

### Automated way

A makefile is provided which you can use with the Make utility on
UNIX-like systems:

  * Running `make source` generates the derived files
      - `README.md`
      - `bath.bbx`, `bath.cbx`, `bath.dbx`
      - `english-bath.lbx`, `british-bath.lbx`
      - `biblatex-bath.bib`
      - `biblatex-bath.ins`
  * Running `make` generates the above files and also `biblatex-bath.pdf`.
  * Running `make inst` installs the files in the user's TeX tree.
    You can undo this with `make uninst`.
  * Running `make install` installs the files in the local TeX tree.
    You can undo this with `make uninstall`.

### Manual way

You only need to follow the first two steps if you have made your own
changes to the .dtx file. The compiled files you need are included in
the zip archive.

 1. Run `luatex biblatex-bath.dtx` to generate the source files.

 2. Compile `biblatex-bath.dtx` with [LuaLaTeX] and [Biber] to generate the
    documentation. You will need, among other things, the [luatexja],
    [adobemapping] and [ipaex] packages installed; this is just for the
    documentation, not for the biblatex style itself.

 3. If you are using TeX Live, find your home TeX tree using the following
    command at the command prompt/terminal:

    ```
    kpsewhich -var-value=TEXMFHOME
    ```

    If you are using MikTeX, consult the MikTeX manual entry for [integrating
    local additions](http://docs.miktex.org/manual/localadditions.html). You
    can use one of the roots (TeX trees) already defined – preferably one of
    the User roots – or set up a new one.

 4. Move the files to your TeX tree as follows:
      - `source/latex/biblatex-bath`:
        `biblatex-bath.dtx`,
        (`biblatex-bath.ins`)
      - `tex/latex/biblatex-bath`:
        `bath.bbx`,
        `bath.cbx`,
        `bath.dbx`,
        `english-bath.lbx`,
        `british-bath.lbx`
      - `doc/latex/biblatex-bath`:
        `biblatex-bath.pdf`,
        `README.md`

 5. You may then have to update your installation's file name database
    before TeX and friends can see the files.

[bath-harvard]: https://library.bath.ac.uk/referencing/harvard-bath
[biblatex]: http://ctan.org/pkg/biblatex
[LuaLaTeX]: http://ctan.org/pkg/lualatex-doc
[Biber]: http://ctan.org/pkg/biber
[luatexja]: http://ctan.org/pkg/luatexja
[adobemapping]: http://ctan.org/pkg/adobemapping
[ipaex]: http://ctan.org/pkg/ipaex

## Licence

Copyright 2016-2018 University of Bath.

This work consists of the documented LaTeX file biblatex-bath.dtx and a Makefile.

The text files contained in this work may be distributed and/or modified
under the conditions of the [LaTeX Project Public License (LPPL)][lppl],
either version 1.3c of this license or (at your option) any later
version.

This work is `maintained' (as per LPPL maintenance status) by [Alex Ball][me].

[lppl]: http://www.latex-project.org/lppl.txt "LaTeX Project Public License (LPPL)"
[me]: https://github.com/alex-ball/bathbib "Alex Ball"

