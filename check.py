#! /usr/bin/env python3
import os
import re
import subprocess
import sys
import typing as t

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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
                targets[current_id] += line.strip().replace("\\@", "")

    return targets


def get_bibitems(filepath: str) -> t.List[str]:
    """Return a list of lines in a recurring pattern such that there is a
    `\\bibitem` line, followed by a line containing a formatted reference,
    followed by a blank line signifying the end of the reference.
    """
    biblatex = True if filepath.endswith(".bbi") else False

    # Ensure file exists:
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    if not os.path.isfile(filepath):
        subprocess.run(["make", filename], cwd=workdir, check=True)
        if not os.path.isfile(filepath):
            print("Could not generate bbl file.")
            sys.exit(1)

    # Process BBL file:
    preamble = True
    lines = list()
    current_line = list()
    with open(filepath) as f:
        for line in f:
            # Ignore first few lines:
            if preamble:
                if line.startswith("\\bibitem"):
                    preamble = False
                else:
                    continue

            # Combine most recent lines:
            current_line.append(line.strip())
            s = " ".join(current_line)
            if s.count("[") == s.count("]") and s.count("{") == s.count("}"):
                # Line is (probably!) syntactically complete
                lines.append(s)
                current_line.clear()
                continue

    return lines


def parse_bibitems(lines: t.List[str]) -> t.Mapping[str, str]:
    """Returns a mapping of IDs to actual bibitem output."""

    outputs = dict()

    NORMAL = 0
    CS = 1
    GOBBLE = 2
    state = [NORMAL]
    level = 1
    exit_arg = 0
    exit_gobble = 0
    buffer = ""
    current_id = None
    for line in lines:
        line = line.strip()

        if current_id is None:
            if m := re.search(r"\\bibitem\[[^\]]*\]\{(?P<id>[^}]*)\}", line):
                current_id = m.group("id")
                outputs[current_id] = ""
            continue
        elif line == "\\newblock":
            continue
        elif line == "":
            if m := re.search(r"\\emph\{.*?\} \\emph\{.*?\}", outputs[current_id]):
                if m.group(0).count("{") == m.group(0).count("}"):
                    replacement = m.group(0).replace("} \\emph{", " ")
                    outputs[current_id] = outputs[current_id].replace(
                        m.group(0), replacement
                    )
            current_id = None
            state = [NORMAL]
            level = 1
            exit_arg = 0
            exit_gobble = 0
            continue

        line = (
            line.replace("\\@", "")
            .replace("\\newblock ", "")
            .replace("\\urlprefix", "Available from: ")
            .replace("\\urldateprefix{}", "Accessed ")
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
                    if level == exit_arg:
                        exit_arg = 0
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
                        exit_gobble = level
                        level += 1
                        buffer = ""
                        continue
                    exit_arg = level
                    level += 1
                    outputs[current_id] += buffer
                    buffer = ""
            elif state[-1] == GOBBLE:
                if char == "{":
                    level += 1
                elif char == "}":
                    level -= 1
                    if level == exit_gobble:
                        exit_gobble = 0
                        state.pop()
                continue

            buffer += char

        outputs[current_id] += buffer
        buffer = ""

    return outputs


def contrast_refs(**kwargs: t.Mapping[str, t.Mapping[str, str]]) -> None:
    """Performs a comparison between different sets of mappings from
    bib database IDs to formatted references.

    Arguments should be given in the form of label=mapping. The label
    is used in the output printed to screen, to show the source of the
    reference text.
    """
    if not kwargs:
        click.echo("No contrast to make.")
        click.Abort
        return

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


if __name__ == "__main__":
    main()
