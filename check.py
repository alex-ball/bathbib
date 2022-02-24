#! /usr/bin/env python3
from collections import deque, defaultdict
from gettext import ngettext
import os
import re
import subprocess
import typing as t

import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def extract_dtx_targets(filepath: str) -> t.Mapping[str, str]:
    """Parses a DTX file and returns a mapping of IDs to target output
    extracted from `bibexbox` environments.
    """

    targets = dict()

    current_id = None
    with open(filepath) as f:
        for line in f:
            if current_id is None:
                if m := re.search(r"\\begin\{bibexbox\}[^}]*\{(?P<id>[^}]*)\}", line):
                    current_id = m.group("id")
                    targets[current_id] = ""
                continue
            else:
                if line.startswith("%"):
                    continue
                if "\\tcblower" in line:
                    current_id = None
                    continue
                if targets[current_id]:
                    targets[current_id] += " "
                line = re.sub(r", (\d{4})[ab]\. ", r", \1. ", line)
                targets[current_id] += line.strip().replace("\\@", "").replace("~", " ")

    return targets


def extract_csl_targets(filepath: str) -> t.Mapping[str, str]:
    """Parses a TEX file and returns a mapping of IDs to target output
    extracted from the specially spaced LaTeX format.
    """

    targets = dict()

    current_ids = deque()
    current_line = list()
    with open(filepath) as f:
        for line in f:
            line = line.strip()

            if not line:
                if current_line:
                    current_id = current_ids.popleft()
                    targets[current_id] = " ".join(current_line)
                    current_line.clear()
                continue

            if not current_ids:
                matches = re.finditer(r"\\cite\{(?P<id>[^}]*)\}", line)
                for m in matches:
                    current_ids.append(m.group("id"))
                continue

            if line == "...":
                continue

            line = re.sub(r", (\d{4})[ab]\. ", r", \1. ", line)
            current_line.append(line.replace("\\@", "").replace("~", " "))

    return targets


def get_bibitems(filepath: str) -> t.List[str]:
    """From a text file, extracts and returns a list of lines in a
    recurring pattern such that there is a `\\bibitem` line, followed
    by a line containing a formatted reference, followed by a blank
    line signifying the end of the reference.
    """
    biblatex = True if filepath.endswith(".bbi") else False

    # Ensure file exists:
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    if not os.path.isfile(filepath):
        subprocess.run(["make", "-C", workdir, filename], check=True)
        if not os.path.isfile(filepath):
            raise click.FileError(f"Could not generate {filename}.")

    # Process BBL file:
    preamble = True
    lines = list()
    current_line = list()

    def finish_record():
        lines.append(" ".join(current_line).replace("\\url {", "\\url{"))
        lines.append("")
        current_line.clear()

    with open(filepath) as f:
        for line in f:
            # Ignore first few lines:
            if preamble:
                if line.startswith("\\bibitem"):
                    preamble = False
                else:
                    continue

            # Check for end of record
            clean_line = line.strip()
            is_eor = False
            if not clean_line:
                if biblatex:
                    # In biblatex, empty lines mean PDF page break
                    continue
                else:
                    is_eor = True
            elif clean_line in ["{}", "\\end{thebibliography}"] and biblatex:
                is_eor = True

            if is_eor:
                finish_record()
                continue

            current_line.append(clean_line)
            s = " ".join(current_line)
            if (
                s.startswith("\\bibitem")
                and s.count("[") == s.count("]")
                and s.count("{") == s.count("}")
            ):
                # `\\bibitem` line is syntactically complete
                lines.append(s)
                current_line.clear()
                continue

        if current_line:
            finish_record()

    return lines


def parse_bibitems(lines: t.List[str]) -> t.Mapping[str, str]:
    """Parses the output from BibTeX and returns a mapping of IDs to
    actual bibitem output.
    """

    outputs = dict()

    NORMAL = 0
    CS = 1
    GOBBLE = 2
    state = [NORMAL]
    level = 1
    exit_args = [0]
    exit_gobbles = [0]
    buffer = ""
    current_id = None
    for line in lines:
        if current_id is None:
            if m := re.search(r"\\bibitem\[[^\]]*\]\{(?P<id>[^}]*)\}", line):
                current_id = m.group("id")
                outputs[current_id] = ""
            continue
        elif line == "":
            outputs[current_id] = re.sub(r", (\d{4})[ab]\. ", r", \1. ", outputs[current_id])
            current_id = None
            state = [NORMAL]
            level = 1
            exit_args = [0]
            exit_gobbles = [0]
            continue

        line = (
            line.replace("\\@", "")
            .replace("\\newblock ", "")
            .replace("\\urlprefix", "Available from: ")
            .replace("\\urldateprefix{}", "Accessed ")
            .replace("\\#", "#")
            .replace("\\pounds ", "£")
            .replace("~", " ")
            .replace("\\noop{h}", "")
        )
        line = re.sub(r"\{\\natexlab\{([^}]*)\}\}", r"\1", line)

        if outputs[current_id]:
            outputs[current_id] += " "

        for char in line:
            if state[-1] == NORMAL:
                if char == "\\":
                    state.append(CS)
                    outputs[current_id] += buffer
                    buffer = ""
                if char == "{":
                    level += 1
                    continue
                elif char == "}":
                    level -= 1
                    if level == exit_args[-1]:
                        exit_args.pop()
                    else:
                        continue
            elif state[-1] == CS:
                if char == " ":
                    state.pop()
                    outputs[current_id] += buffer
                    buffer = ""
                elif char == "{":
                    state.pop()
                    if buffer == "\\bibinfo":
                        state.append(GOBBLE)
                        exit_gobbles.append(level)
                        level += 1
                        buffer = ""
                        continue
                    exit_args.append(level)
                    level += 1
                    outputs[current_id] += buffer
                    buffer = ""
            elif state[-1] == GOBBLE:
                if char == "{":
                    level += 1
                elif char == "}":
                    level -= 1
                    if level == exit_gobbles[-1]:
                        exit_gobbles.pop()
                        state.pop()
                continue

            buffer += char

        outputs[current_id] += buffer
        buffer = ""

    return outputs


def parse_simple_bibitems(lines: t.List[str]) -> t.Mapping[str, str]:
    """Parses the output from biblatex2bibitem and returns a mapping of
    IDs to actual bibitem output.
    """
    outputs = dict()

    current_id = None
    for line in lines:
        if current_id is None:
            if m := re.search(r"\\bibitem\{(?P<id>[^}]*)\}", line):
                current_id = m.group("id")
        elif line == "":
            current_id = None
        else:
            line = re.sub(r"‘(.*?)’", r"\\enquote{\1}", line)
            line = re.sub(r", (\d{4})[ab]\. ", r", \1. ", line)
            # Hack to fix truncated output
            line = line.replace(
                "everything-you-should-know-about-the-c",
                "everything-you-should-know-about-the-coronavirus-outbreak/"
                "20207629.article}"
            )
            outputs[current_id] = line.replace("’", "'").replace("–", "--")

    return outputs


def contrast_refs(**kwargs: t.Mapping[str, t.Mapping[str, str]]) -> None:
    """Performs a comparison between different sets of mappings from
    bib database IDs to formatted references.

    Arguments should be given in the form of label=mapping. The label
    is used in the output printed to screen, to show the source of the
    reference text.
    """
    if not kwargs:
        raise click.ClickException("No contrast to make.")

    labels = list(kwargs.keys())

    for id, target in kwargs[labels[0]].items():
        errors = list()
        for label in labels[1:]:
            if id not in kwargs[label]:
                errors.append(f"{label} is missing ID {id}.")
            elif kwargs[label][id] != target:
                errors.append(f"{label}: {kwargs[label][id]}")
        if errors:
            click.secho(id, bold=True)
            click.echo(f"{labels[0]}: {target}")
            for error in errors:
                click.echo(error)
            print()


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Performs unit tests on LaTeX output from the Bath (Harvard)
    bibliography styles, and ensures the target output is aligned
    between the LaTeX and CSL styles.
    """
    pass


@main.command(context_settings=CONTEXT_SETTINGS)
def biblatex():
    """Performs unit tests on output from the biblatex bath style."""
    targets = extract_dtx_targets("biblatex/biblatex-bath.dtx")
    lines = get_bibitems("biblatex/test-output.bbi")
    outputs = parse_simple_bibitems(lines)
    contrast_refs(Target=targets, Output=outputs)


@main.command(context_settings=CONTEXT_SETTINGS)
def bst():
    """Performs unit tests on output from the bathx.bst BibTeX style."""
    targets = extract_dtx_targets("bst/bath-bst.dtx")
    lines = get_bibitems("bst/bath-bst.bbl")
    outputs = parse_bibitems(lines)
    contrast_refs(Target=targets, Output=outputs)


@main.command(context_settings=CONTEXT_SETTINGS)
def bst_old():
    """Performs unit tests on output from the bath.bst BibTeX style."""
    targets = extract_dtx_targets("bst/bath-bst.dtx")
    lines = get_bibitems("bst/bath-bst-v1.bbl")
    outputs = parse_bibitems(lines)
    contrast_refs(Target=targets, Output=outputs)


@main.command(context_settings=CONTEXT_SETTINGS)
def sync():
    """Checks that the target texts for BibTeX, biblatex and CSL are
    synchronised.
    """
    biblatex_targets = extract_dtx_targets("biblatex/biblatex-bath.dtx")
    bibtex_targets = extract_dtx_targets("bst/bath-bst.dtx")
    csl_targets = extract_csl_targets("csl/bath-csl-test.tex")
    contrast_refs(
        Biblatex=biblatex_targets,
        BibTeX__=bibtex_targets,
        CSL_____=csl_targets,
    )
    missing = defaultdict(set)
    for key in bibtex_targets.keys():
        if key not in biblatex_targets:
            missing[key].add("Biblatex")
        if key not in csl_targets:
            missing[key].add("CSL")
    for key in csl_targets.keys():
        if key not in biblatex_targets:
            missing[key].add("Biblatex")
        if key not in bibtex_targets:
            missing[key].add("BibTeX")
    for key, sources in missing.items():
        click.echo(
            f"{' and '.join(sources)} {ngettext('is', 'are', sources)} missing ID {id}."
        )


if __name__ == "__main__":
    main()
