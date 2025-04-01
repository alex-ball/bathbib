# CSL implementation of the University of Bath's Harvard referencing style

As well as the CSL style itself, this repository also contains the apparatus for
testing its output against the [specification web page][bath-harvard]. You may
find it helpful to see how the examples from that page have been coded into a
[YAML database](bath-csl-test.yaml). The YAML format follows the same principles
as [CSL-JSON].

[bath-harvard]: https://library.bath.ac.uk/referencing/harvard-bath
[CSL-JSON]: https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html


## Tips when using the style

  - Things will automatically get tagged ‘\[Online]’ if you include a URL, DOI,
    or access date.

  - For many resource types, you can use `genre` to put something in square
    brackets after the title. The exceptions are `broadcast`, `motion_picture`,
    `thesis` and, if you supply a `number`, `bill`, `patent`, `report`, and
    `standard`.

  - For preprints, use resource type `article` or `report` and put the
    repository name under `archive`. Put the location and name of the
    institution that runs the repository (if known) under `publisher-place` and
    `publisher` respectively.

  - Use `article-newspaper` or `article-magazine` instead of `article-journal`
    to display the month and day.

  - With a `thesis`, use `genre` to record the type of thesis;

  - With a `report` or `patent`, record the report/patent series as
    `collection-title`, the report/patent type as `genre` and the report/patent
    number as `number`. The difference is that a series is typically plural and
    followed by a comma, while a type is typically singular and followed by a
    space.

  - Record a standard as a `standard` or, failing that, `report`. Include the
    identifier at the beginning of the `title`.

  - For unpublished materials, use the closest applicable entry type and put
    ‘Unpublished’ under `annote`. The `pamphlet` type is useful for many
    materials of this sort.

  - With a `graphic`, you can specify `archive` and `archive-place`, as in the
    Bowden bicycle example.

  - With a `map`, use `scale` for the scale.

  - With a `motion_picture`, use `medium` or `genre` to specify the type, e.g.
    ‘Film’.

  - With a `broadcast`, use `publisher` for the channel, `medium` or `genre` for
    ‘Radio’ or ‘TV’, and `annote` for the time. If it is an untitled episode of
    a series, put the series and episode number as the `title`, otherwise put
    the series in `container-title` and the episode number as ‘Episode
    *series*:*episode*’ in `number`.

  - Use `dataset` for database entries and datasets. Give the name of a
    containing database in `container-title`.

  - Use `software` for software. This type was introduced in CSL v1.0.2, so if
    your toolset doesn't support it, use `dataset` instead; unfortunately the
    ‘\[Online]’ won't be suppressed in this case.

  - When citing social media posts, there is no standard way of including the
    author's social media handle. As a workaround, you can include it as the
    `dropping-particle` name part, but you must supply the surrounding square
    brackets as part of the value. This works best with personal accounts; with
    corporate accounts you would have to use the `family` name part instead of
    `literal`, and you get a stray comma between the name and handle.
    Alternatively, you could include the handle as part of the `literal` name
    part, but depending on your software you might not be able to work around
    including it in your citations as well.

  - When citing works in non-English languages, use `original-title` for the
    English translation of the non-English title. This reverses the intended
    semantics of `title` and `original-title` but makes a sort of sense
    regarding the priority of the reference elements.

  - With transliterated works, provide the transliteration of names as the
    `dropping-particle` component for (inverted) names at the head of the
    reference and as the `suffix` for later (natural order) names. Provide
    transliterated titles directly within the respective `title` field.

  - Use the `legislation` type for primary legislation such as Acts of
    Parliament and EU Directives. For secondary legislation such as Statutory
    Instruments, use the `regulation` type if available, otherwise
    `legislation`. With Acts, use `chapter-number` for the chapter and, for
    statutes before 1963, use `collection-title` for the series. With
    directives, use `container-title` for the journal (OJ), `collection-title`
    for the series, `volume` for the volume and `page` for the starting page.

  - Use the `bill` type for House of Commons/Lords Bills but also for House of
    Commons/Lords Papers and Command Papers. Use `collection-title` for the
    series and session (e.g. ‘Bills | 1987/88’) or `genre` for the type (e.g.
    ‘Cm.’) and `number` for the printing.
  
  - Use `hearing` or `paper-conference` for Parliamentary debates, with the year
    in `issued`, the full date of the debate in `event-date`, and the Hansard
    volume in `volume`.

  - For legal cases, only approximate support is possible, especially now that
    Harvard (Bath) has introduced its own unique style. The following variations
    are available:

      - To get the legal case format introduced in 2024, you must supply both
        the `authority` (court) and `number` (case number). If citing a
        particular court division, you can add it manually to the end of
        `authority` or supply it separately in `division`. Use `container-title`
        for the reporting journal, and `volume`, `issue` and `page` for
        pinpointing within it.

      - To get the format for a Judgment of the European Court of Justice, (that
        is, with the case number in parentheses between the title and year),
        supply a `number` (case number) but no `authority`. To cite a case
        reported in ECR or equivalent, put the reporting journal in
        `collection-title`, and use `volume` and `page` for pinpointing. To cite
        a case in the OJ, put ‘OJ’ as the `container-title` and follow the
        instructions above for pinpointing EU Directives.

      - To cite any other case in the OJ, don't give a `number`; put ‘OJ’ as the
        `container-title` and follow the instructions above for pinpointing EU
        Directives.

      - To get the traditional or neutral legal case format, don't give a
        `number` or a `container-title`. Use `collection-title` (reporting
        journal or court abbreviation) and `page` (first page, or case number
        with or without division suffix). The year will be shown in square
        brackets unless `volume` is given, in which case it will be in
        parentheses.

    The use of `collection-title` in the above is quirky, but the simplifying
    principle behind it is that `container-title` is printed in italics and
    `collection-title` is not. One motivation for it is that CSL cannot detect
    ‘OJ’ as a special value, but Harvard (Bath) treats it specially.

## Testing the style

The technique used here to test the CSL style follows these steps:

 1. Use `pandoc` to convert the reference examples from the companion LaTeX
    styles into HTML.

 2. Use `pandoc` and its built-in `citeproc` library to convert
    `bath-csl-test.yaml` into HTML formatted references.

 3. Convert `bath-csl-test.yaml` into JSON and use `citeproc-js-server` (hence
    `citeproc-js`) to convert it again into HTML formatted references.

 4. Compare the target (LaTeX-derived) references against the `pandoc`-generated
    references, and the `pandoc`-generated references against the
    `citeproc-js`-generated references.

This process is automated as much as possible, which unfortunately means a
dependency on a wide range of utilities. Some trivial or irreconcilable
discrepancies are erased at different points in this process, so some potential
quirks with real-life implementations won't show up.


### Pandoc-based testing

Dependencies:

- GNU Make
- `bash`, `awk`, `sed`
- `pandoc` v2.11+
- Python v3.8+

An HTML document comparing the expected and actual output from `pandoc` can be
generated like so:

```bash make bath-csl-test.html ```

This invokes the `check-output.py` script to tidy up the raw output and perform
the comparison.


### Citeproc-js testing

Dependencies are the same as for Pandoc-based testing, plus:

- `curl`
- `citeproc-js-server` running at `http://127.0.0.1:8085`
- Python packages `click` and `pyyaml`
- LibYAML

An HTML document containing the output from `citeproc-js` can be generated like
so:

```bash make bath-csl-test-js.html ```

This invokes the `yaml2json.py` script to generate the correct input to
`citeproc-js-server`; the `check-output.py` script is then used to inject
the results into the raw output from `pandoc`.


## Validating the style

CSL processors can be quite forgiving, so before submitting changes upstream,
the style should be checked with the official [CSL Validator].

[CSL Validator]: https://validator.citationstyles.org/
