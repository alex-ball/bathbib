#! /usr/bin/env python3
import json
import re

import click
import yaml

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-o",
    "--output",
    type=click.File(mode="w", lazy=True),
    default="-",
    help="Output file (default: STDOUT).",
)
@click.option(
    "-s",
    "--style",
    type=click.File(mode="r", lazy=True),
    help="CSL style file to bundle.",
)
@click.argument("input", type=click.File())
def main(output, style, input):
    """
    Converts a pandoc-compatible CSL-YAML database into
    citeproc-js-server-compatible CSL-JSON data.

    If "-" is given as the YAML input filename, the database will be
    read from STDIN.
    """

    # Error handling from https://stackoverflow.com/a/30407093
    try:
        y_refs = yaml.load(input, Loader=yaml.CSafeLoader)
    except yaml.YAMLError as exc:
        click.echo("Error while parsing YAML file:")
        if hasattr(exc, "problem_mark"):
            if exc.context is None:
                click.echo(
                    f"  parser says\n{exc.problem_mark}\n  {exc.problem}\n"
                    "Please correct data and retry."
                )
            else:
                click.echo(
                    f"  parser says\n{exc.problem_mark}\n  {exc.problem} "
                    f"{exc.context}\nPlease correct data and retry."
                )
        else:
            click.echo("Something went wrong while parsing yaml file")
        click.Abort()
        return

    if not isinstance(y_refs, dict) or "references" not in y_refs:
        raise click.ClickException(
            message="YAML input should be an object/hash/dictionary with "
            "a 'references' key."
        )

    if not isinstance(y_refs["references"], list):
        raise click.ClickException(
            message="YAML input should be an object/hash/dictionary with "
            "a 'references' key that maps to an array/list of entries."
        )

    j_refs = {"items": list(), "citationClusters": list()}
    for i, ref in enumerate(y_refs["references"], start=1):
        if "id" not in ref:
            raise click.ClickException(
                message="All entries must have an 'id' key/value pair."
            )
        # Remove pandoc-specific workaround for escaping underscores in URLs
        url = ref.get("URL")
        if url:
            ref["URL"] = url.replace(r"\_", "_")
        j_refs["items"].append(ref)
        j_refs["citationClusters"].append(
            {
                "citationItems": [{"id": ref["id"]}],
                "properties": {"noteIndex": i},
            }
        )

    if style is not None:
        xml_str = style.read()
        j_refs["styleXML"] = re.sub(r"\n\s*", "", xml_str)

    json.dump(j_refs, output, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

"""
Then:


"""
