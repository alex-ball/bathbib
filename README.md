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

You may find it helpful to see how the examples have been coded into a [YAML
database](csl/bath-csl-test.yaml). The YAML format follows the same
principles as [CSL-JSON].

Changes made here are submitted upstream to the [official repository][CSL Styles]
for CSL styles.

[Citation Style Language]: http://docs.citationstyles.org/en/stable/
[CSL-JSON]: https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html
[CSL Styles]: https://github.com/citation-style-language/styles

### Tips when using the style

  - Things will automatically get tagged ‘\[Online]’ if you include a URL or
    DOI.

  - For many resource types, you can use `genre` to put something in square
    brackets after the title, e.g. the Kindle version in the Hodds reference.
    The exceptions are `thesis`, `report`, `patent`, `motion_picture` and
    `bill`.

  - For preprints, use resource type `report` and put the repository name under
    `archive`.

  - Use `article-newspaper` or `article-magazine` instead of `article-journal`
    to display the month and day.

  - With a `thesis`, use `genre` to record the type of thesis;

  - With a `report` or `patent`, record the report/patent series as
    `collection-title`, the report/patent type as `genre` and the report/patent
    number as `number`. The difference is that a series is typically plural and
    followed by a comma, while a type is typically singular and followed by a
    space.

  - Record a standard as a `report`, with the identifier included at the
    beginning of the `title`.

  - For unpublished materials, use the closest applicable entry type and put
    ‘Unpublished’ under `annote`.

  - With a `graphic`, you can specify `archive` and `archive-place`, as in the
    Bowden bicycle example.

  - With a `map`, use `scale` for the scale.

  - With a `motion_picture`, use `genre` to specify the type, e.g. ‘Film’.

  - With a `broadcast`, use `publisher` for the channel, `medium` for ‘Radio’ or
    ‘TV’, and `annote` for the time.

  - Use `dataset` for database entries, datasets and software. Give the name of
    a containing database in `container-title`. Unfortunately there is no way to
    prevent ‘\[Online]’ appearing for software specifically.

  - When citing works in non-English languages, use `original-title` for the
    English translation of the non-English title. This reverses the intended
    semantics of `title` and `original-title` but makes a sort of sense
    regarding the priority of the reference elements.

  - With transliterated works, provide the transliteration of names as the
    `dropping-particle` component for (inverted) names at the head of the
    reference and as the `suffix` for later (natural order) names. Provide
    transliterated titles directly within the respective `title` field.

  - Use the `legislation` type for Acts of Parliament, Statutory Instruments and
    EU Directives. With Acts, use `chapter-number` for the chapter and, for
    statutes before 1963, use `collection-title` for the series. With
    directives, use `container-title` for the journal (OJ), `collection-title`
    for the series, `volume` for the volume and `page` for the starting page.

  - Use the `bill` type for House of Commons/Lords Bills but also for House of
    Commons/Lords Papers and Command Papers. Use `collection-title` for the
    series and session (e.g. ‘Bills | 1987/88’) or `genre` for the type (e.g.
    ‘Cm.’) and `number` for the printing.

  - For legal cases, only approximate support is possible. The year will be
    shown in square brackets unless `volume` is given, in which case it will be
    in parentheses. If you supply a number, it will be shown after the title in
    parentheses and the whole reference will be formatted as if for a Judgment
    of the European Court of Justice. You should normally supply the reporting
    journal in `collection-title` with the first `page`. For cases reported in
    the EU Official Journal, put ‘OJ’ in `container-title` instead, and
    OJ-specific formatting will be used.
