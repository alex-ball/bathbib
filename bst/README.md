# bath-bst: Harvard referencing style as recommended by the University of Bath Library

This package provides a [BibTeX] style to format reference lists in the
[Harvard style][bath-harvard] recommended by the University of Bath Library.
It should be used in conjunction with [natbib] for citations.

## Installation

The files you need are included in the zip archive available from [GitHub].
If you use the zip archive from [CTAN], you will need to run `luatex
bath-bst.dtx` to generate them.

You can use this style simply by copying the `bath.bst`/`bathx.bst` files into
your working directory, that is, the directory holding the main `.tex` file for
your document. If you want the style to be available for all your documents
without having to copy it over each time, you can install it using the
instructions below.

### Managed way

The latest stable release of bath-bst has been packaged for TeX Live and
MiKTeX. If you are running TeX Live and have `tlmgr` installed, you can install
the package simply by running `tlmgr install bath-bst`. If you are running
MiKTeX, you can install the package by running `mpm --install=bath-bst`.
Both `tlmgr` and `mpm` have GUI versions that you might find friendlier.

### Automated way

A makefile is provided which you can use with the Make utility on
UNIX-like systems:

  * Running `make source` generates the derived files
      - `README.md`
      - `bath.bst` and `bathx.bst`
      - `bath-bst-v1.tex`
      - `bath-bst.bib` and `bath-bst-v1.bib`
      - `bath-bst.ins`
  * Running `make` generates the above files and also `bath-bst.pdf` and
    `bath-bst-v1.pdf`. Ensure you have (at least) the [luatexja], [adobemapping]
    and [ipaex] packages installed first.
  * Running `make inst` installs the files in the user's TeX tree.
    You can undo this with `make uninst`.
  * Running `make install` installs the files in the local TeX tree.
    You can undo this with `make uninstall`.

### Manual way

You do not need to follow the first step if you downloaded the zip archive from
[GitHub]. You do not need to follow the second step if you already have the PDF
documentation.

 1. Run `luatex bath-bst.dtx` to generate the source files.

 2. Compile `bath-bst.dtx` with [LuaLaTeX] and BibTeX to generate the
    documentation. You will need, among other things, the [luatexja],
    [adobemapping] and [ipaex] packages installed; this is just for the
    documentation, not for the BibTeX style itself. To generate the version 1
    tests and documentation, compile `bath-bst-v1.tex` with LuaLaTeX and BibTeX.

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
      - `source/bibtex/bath-bst`:
        `bath-bst.dtx`,
        (`bath-bst.ins`)
      - `bibtex/bst/bath-bst`:
        `bath.bst`,
        `bathx.bst`
      - `doc/bibtex/bath-bst`:
        `bath-bst.pdf`,
        `bath-bst-v1.pdf`,
        `README.md`

 5. You may then have to update your installation's file name database
    before TeX and friends can see the files.

[bath-harvard]: https://library.bath.ac.uk/referencing/harvard-bath
[BibTeX]: http://ctan.org/pkg/bibtex
[GitHub]: https://github.com/alex-ball/bathbib/releases
[CTAN]: http://ctan.org/pkg/bath-bst
[natbib]: http://www.ctan.org/pkg/natbib
[LuaLaTeX]: http://ctan.org/pkg/lualatex-doc
[luatexja]: http://ctan.org/pkg/luatexja
[adobemapping]: http://ctan.org/pkg/adobemapping
[ipaex]: http://ctan.org/pkg/ipaex

## Licence

Copyright 2016-2019 University of Bath.

This work consists of the documented LaTeX file bath-bst.dtx and a Makefile.

The text files contained in this work may be distributed and/or modified
under the conditions of the [LaTeX Project Public License (LPPL)][lppl],
either version 1.3c of this license or (at your option) any later
version.

This work is ‘maintained’ (as per LPPL maintenance status) by [Alex Ball][me].

[lppl]: http://www.latex-project.org/lppl.txt "LaTeX Project Public License (LPPL)"
[me]: https://github.com/alex-ball/bathbib "Alex Ball"
