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
implementation of the Bath Harvard style in [Citation Style Language].

Changes made here are submitted upstream to the [official repository][CSL Styles]
for CSL styles.

[Citation Style Language]: http://docs.citationstyles.org/en/stable/
[CSL Styles]: https://github.com/citation-style-language/styles
