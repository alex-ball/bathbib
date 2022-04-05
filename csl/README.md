# CSL implementation of the University of Bath's Harvard referencing style

As well as the CSL style itself, this repository also contains the apparatus
for testing its output against the [specification web page][bath-harvard].
You may find it helpful to see how the examples from that page have been
coded into a [YAML database](bath-csl-test.yaml). The YAML format follows
the same principles as [CSL-JSON].

[bath-harvard]: https://library.bath.ac.uk/referencing/harvard-bath
[CSL-JSON]: https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html


## Tips when using the style

  - Things will automatically get tagged ‘\[Online]’ if you include a URL,
    DOI, or access date.

  - For many resource types, you can use `genre` to put something in square
    brackets after the title. The exceptions are `thesis`, `report`, `patent`,
    `motion_picture` and `bill`.

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

  - With a `broadcast`, use `publisher` for the channel, `medium` for ‘Radio’ or
    ‘TV’, and `annote` for the time.

  - Use `dataset` for database entries and datasets. Give the name of a containing
    database in `container-title`.
  
  - Use `software` for software. This type was introduced in CSL v1.0.2, so if
    your toolset doesn't support it, use `dataset` instead; unfortunately the
    ‘\[Online]’ won't be suppressed in this case.

  - When citing social media posts, there is no standard way of including the
    author's social media handle. As a workaround, you can include it as the
    `dropping-particle` name part, but you must supply the surrounding square
    brackets as part of the value. This works best with personal accounts;
    with corporate accounts you would have to use the `family` name part
    instead of `literal`, and you get a stray comma between the name and
    handle. Alternatively, you could include the handle as part of the
    `literal` name part, but depending on your software you might not be able
    to work around including it in your citations as well.

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

  - For legal cases, only approximate support is possible. The year will be
    shown in square brackets unless `volume` is given, in which case it will be
    in parentheses. If you supply a number, it will be shown after the title in
    parentheses and the whole reference will be formatted as if for a Judgment
    of the European Court of Justice. You should normally supply the reporting
    journal in `collection-title` with the first `page`. For cases reported in
    the EU Official Journal, put ‘OJ’ in `container-title` instead, and
    OJ-specific formatting will be used.
