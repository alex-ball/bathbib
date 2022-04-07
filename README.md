# Programmatic implementations of the University of Bath's Harvard referencing style

## BibTeX and biblatex styles

This repository contains two LaTeX implementations of the
[Harvard referencing style][bath-harvard] recommended by the University of Bath
Library.

  + [`biblatex`](biblatex/)
    contains the implementation for use with [biblatex] and [Biber].
  + [`bst`](bst/)
    contains the implementation for use with [BibTeX].

For details of how to use these styles, please see the PDF documentation bundled
with the code on the [releases] page, or on the [bath-bst] or [biblatex-bath]
package pages on CTAN.

[bath-harvard]: https://library.bath.ac.uk/referencing/harvard-bath
[biblatex]: https://ctan.org/pkg/biblatex
[Biber]: https://ctan.org/pkg/biber
[BibTeX]: https://ctan.org/pkg/bibtex
[releases]: https://github.com/alex-ball/bathbib/releases
[bath-bst]: https://ctan.org/pkg/bath-bst
[biblatex-bath]: https://ctan.org/pkg/biblatex-bath


## Citation Style Language

This repository also contains a [development area](csl/) for maintaining an
implementation of the Bath Harvard style in [Citation Style Language]. Please
look there for [tips on how to arrange your CSL database](csl/README.md)
to make best use of the style.

Changes made here are submitted upstream to the [official repository][CSL Styles]
for CSL styles.

[Citation Style Language]: http://docs.citationstyles.org/en/stable/
[CSL Styles]: https://github.com/citation-style-language/styles


## Testing

The Python script `check.py` can be used to test the output of the various
styles. It relies on a lot of dependencies, but not all of them are needed
for all tests.

- GNU Make
- `bash`, `awk`, `sed`, `curl`
- A LaTeX distribution (e.g. TeX Live, MikTeX) with `latexmk`, `lualatex`, etc.
- `pandoc` v2.11+
- Python v3.8+ and the Python packages `click`, `lxml` and `pyyaml`
- LibYAML
- `citeproc-js-server` running at `http://127.0.0.1:8085`

You can find [`pandoc`] and [`citeproc-js-server`] on GitHub.

[`pandoc`]: https://github.com/jgm/pandoc
[`citeproc-js-server`]: https://github.com/zotero/citeproc-js-server

To show what testing options are available:

```bash
./check.py -h
```

Testing LaTeX styles:

  - `./check.py biblatex`: tests the biblatex output using `bath.bbx` and
    the more native biblatex `.bib` file.
  - `./check.py compat`: tests the biblatex output using `bath.bbx` and
    the BibTeX `.bib` file tailored for `bathx.bst`.
  - `./check.py bst`: tests the BibTeX output of `bathx.bst`.
  - `./check.py bst-old`: tests the BibTeX output of `bath.bst`.

Testing the CSL style:

  - `./check.py csl`: tests the output of the Haskell `citeproc` library
    using `harvard-university-of-bath.csl` via `pandoc`.
  - `./check.py csl-sync`: tests for variance between the output of the
    Haskell `citeproc` library and `citeproc-js` when using
    `harvard-university-of-bath.csl`.

Testing consistency:

  - `./check.py sync`: confirms whether the three implementations are
    all targeting the same set of LaTeX-formatted references.
