#! /usr/bin/env python3
from collections import deque, defaultdict
from gettext import ngettext
import html
import os
import re
import subprocess
import typing as t
from warnings import catch_warnings

import click
from lxml import html as lhtml

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def extract_dtx_targets(filepath: str) -> t.Dict[str, str]:
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


def extract_csl_targets(filepath: str) -> t.Dict[str, str]:
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

    # Ensure file exists and is up to date:
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    r = subprocess.run(["make", "-C", workdir, filename])
    if r.returncode and os.path.isfile(filepath):
        os.remove(filepath)
    if not os.path.isfile(filepath):
        raise click.FileError(filename, "Recipe failed to create file.")
    print()

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


def parse_bibitems(lines: t.List[str]) -> t.Dict[str, str]:
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
            if m := re.search(r"\\bibitem\[.*\]\{(?P<id>[^}]*)\}$", line):
                current_id = m.group("id")
                outputs[current_id] = ""
            continue
        elif line == "":
            outputs[current_id] = re.sub(
                r", (\d{4})[ab]\. ", r", \1. ", outputs[current_id]
            )
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
                elif char == "}":
                    if buffer == "\\relax":
                        buffer = ""
                    state.pop()
                    level -= 1
                    if level == exit_args[-1]:
                        exit_args.pop()
                    else:
                        continue
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


def parse_simple_bibitems(lines: t.List[str]) -> t.Dict[str, str]:
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
            outputs[current_id] = line.replace("’", "'").replace("–", "--")

    return outputs


def parse_csl_refs(
    filepath: str, only_fails: bool = False
) -> t.Tuple[t.Dict[str, str]]:
    """Extracts tests from CSL comparison document in a form that can
    be used by the `contrast_refs()` function.

    If `only_fails` is true, only the failed output is returned.
    """
    # Ensure file exists and is up to date:
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    r = subprocess.run(["make", "-C", workdir, filename])
    if r.returncode and os.path.isfile(filepath):
        os.remove(filepath)
    if not os.path.isfile(filepath):
        raise click.FileError(filename, "Recipe failed to create file.")
    print()

    parsed = list()
    targets = dict()
    outputs = dict()

    tree = lhtml.parse(filepath)
    root = tree.getroot()
    tests = root.find_class("test")

    if only_fails:
        for test in tests:
            target_divs = test.findall("./div[@class='target failure']")
            if not target_divs:
                continue

            output_divs = test.findall("./div[@class='references failure']")
            if not output_divs:
                continue

            parsed.append((target_divs, output_divs))
    else:
        for test in tests:
            target_divs = test.find_class("target")
            if not target_divs:
                continue

            output_divs = test.find_class("references")
            if not output_divs:
                continue

            parsed.append((target_divs, output_divs))

    for pair in parsed:
        (target_divs, output_divs) = pair
        assert len(target_divs) == len(output_divs)

        for i, target_div in enumerate(target_divs):
            target_p = target_div[0]
            target = html.unescape(
                lhtml.tostring(target_p).decode("utf-8").strip()[3:-4]
            )

            output_div_div = output_divs[i][0]
            current_id = output_div_div.get("id")[4:]
            output_p = output_div_div[0]
            output = html.unescape(
                lhtml.tostring(output_p).decode("utf-8").strip()[3:-4]
            )

            targets[current_id] = target
            outputs[current_id] = output

    return (targets, outputs)


def ignore_unfixable(
    outputs: t.Dict[str, str], compat: bool = False
) -> t.Dict[str, str]:
    """Provide specific overrides for BibTeX entries that cannot be
    fixed.
    """
    for key in ["crawford1965oim"]:
        if key in outputs:
            outputs[key] = outputs[key].replace(
                "Activation analysis: Proceedings", "Activation analysis: proceedings"
            )
    for key in ["deneulin.dinerstein2010hms"]:
        if key in outputs:
            outputs[key] = outputs[key].replace(
                "Hope movements: Social", "Hope movements: social"
            )
    for key in ["tkmmm2020ts"]:
        if key in outputs:
            outputs[key] = outputs[key].replace(
                "Tiger king: Murder", "Tiger king: murder"
            )
    for key in [
        "devlin.etal2021ipp",
        "steward.etal2020eys",
        "liontou.etal2019dra",
        "cogley2020ccs",
        "clark2004euk",
        "gb.hc2024rpc",
    ]:
        if key in outputs:
            outputs[key] = outputs[key].replace(" \\textup{[Online]}}", "} [Online]")
    for key in ["gb.wa1735", "gb.pa2014", "gb.hmr2012"]:
        if key in outputs:
            outputs[key] = re.sub(
                r"\\emph\{(.*?) (\d{4})\}", r"\\emph{\1} \\emph{\2}", outputs[key]
            )
    return outputs


def format_diff(label: str, primary: str, secondary: str) -> str:
    """Indicates first point of difference between primary and
    secondary string."""
    diff = " " * (len(label) + 2)
    for i, char in enumerate(list(primary)):
        if char != secondary[i : i + 1]:
            diff += "^"
            break
        diff += "-"
    return diff


def contrast_refs(
    **kwargs: t.Dict[str, t.Dict[str, str]],
) -> t.DefaultDict[str, t.Set[str]]:
    """Performs a comparison between different sets of mappings from
    bib database IDs to formatted references.

    Arguments should be given in the form of label=mapping. The label
    is used in the output printed to screen, to show the source of the
    reference text.

    Returns a defaultdict that maps keys from the first source that
    do not appear in at least one of the other sources; but keys are
    only added if no contrast between available outputs is found.
    """
    if not kwargs:
        raise click.ClickException("No contrast to make.")

    labels = list(kwargs.keys())
    label_width = max([len(s) for s in labels])

    missing = defaultdict(set)
    found_errors = False
    for key, target in kwargs[labels[0]].items():
        errors = list()
        for label in labels[1:]:
            if key not in kwargs[label]:
                missing[key].add(label)
            elif kwargs[label][key] != target:
                dededupl = re.sub(r" (\d{4})[a-c]\.", r" \1.", kwargs[label][key])
                if dededupl != target:
                    errors.append(f"{label}: {dededupl}")
                    errors.append(format_diff(label, target, dededupl))
        if errors:
            found_errors = True
            click.secho(key, bold=True)
            click.echo(f"{labels[0].ljust(label_width)}: {target}")
            for error in errors:
                click.echo(error)
            sources = missing.pop(key, None)
            if sources:
                click.echo(f"Not present in {' or '.join(sources)}.")
            print()

    if not (found_errors or missing):
        click.echo(f"No discrepancies found.")

    return missing


def print_missing(missing: t.DefaultDict[str, t.Set[str]]) -> None:
    """Prints out information on missing keys."""
    for key, labels in missing.items():
        click.echo(
            f"{' and '.join(labels)} {ngettext('is', 'are', len(labels))} "
            f"missing ID {key}."
        )


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Performs unit tests on LaTeX and CSL output from the Bath
    (Harvard) bibliography styles, and ensures the target output is
    aligned between the LaTeX and CSL styles, and between two different
    CSL implementations.
    """
    pass


@main.command(context_settings=CONTEXT_SETTINGS)
def biblatex():
    """Performs unit tests on output from the biblatex bath style."""
    targets = extract_dtx_targets("biblatex/biblatex-bath.dtx")
    lines = get_bibitems("biblatex/test-output.bbi")
    outputs = parse_simple_bibitems(lines)
    print_missing(contrast_refs(Target=targets, Output=outputs))


@main.command(context_settings=CONTEXT_SETTINGS)
def bst():
    """Performs unit tests on output from the bathx.bst BibTeX style."""
    targets = extract_dtx_targets("bst/bath-bst.dtx")
    lines = get_bibitems("bst/bath-bst.bbl")
    outputs = ignore_unfixable(parse_bibitems(lines))
    print_missing(contrast_refs(Target=targets, Output=outputs))


@main.command(context_settings=CONTEXT_SETTINGS)
def bst_old():
    """Performs unit tests on output from the bath.bst BibTeX style."""
    targets = extract_dtx_targets("bst/bath-bst.dtx")
    lines = get_bibitems("bst/bath-bst-v1.bbl")
    outputs = ignore_unfixable(parse_bibitems(lines))
    print_missing(contrast_refs(Target=targets, Output=outputs))


@main.command(context_settings=CONTEXT_SETTINGS)
def compat():
    """Checks biblatex bath style using BibTeX bib file."""
    targets = extract_dtx_targets("biblatex/biblatex-bath.dtx")

    filepath = "bst/bath-bst.bib"
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    r = subprocess.run(["make", "-C", workdir, filename])
    if r.returncode and os.path.isfile(filepath):
        os.remove(filepath)
    if not os.path.isfile(filepath):
        raise click.FileError(filename, "Recipe failed to create file.")

    lines = get_bibitems("biblatex/test-compat.bbi")
    outputs = parse_simple_bibitems(lines)
    print_missing(contrast_refs(Target=targets, Output=outputs))


@main.command(context_settings=CONTEXT_SETTINGS)
def csl():
    """Performs unit tests on output from the CSL style using Pandoc.

    Unlike with the LaTeX styles, the actual testing is delegated to
    the makefile and script in the `csl/` directory.
    """
    targets, outputs = parse_csl_refs("csl/bath-csl-test.html", only_fails=True)
    print_missing(contrast_refs(Target=targets, Output=outputs))


@main.command(context_settings=CONTEXT_SETTINGS)
def csl_impl():
    """Contrasts CSL output from pandoc and citeproc-js.

    Requires citeproc-js-server to be running on http://127.0.0.1:8085/.
    """
    _, outputs = parse_csl_refs("csl/bath-csl-test.html")
    _, cpjs_outputs = parse_csl_refs("csl/bath-csl-test-js.html")
    print_missing(contrast_refs(Pandoc=outputs, CiteprocJS=cpjs_outputs))


@main.command(context_settings=CONTEXT_SETTINGS)
def sync():
    """Contrasts the target texts for BibTeX, biblatex and CSL."""
    biblatex_targets = extract_dtx_targets("biblatex/biblatex-bath.dtx")
    bibtex_targets = extract_dtx_targets("bst/bath-bst.dtx")
    csl_targets = extract_csl_targets("csl/bath-csl-test.tex")
    missing = contrast_refs(
        Biblatex=biblatex_targets,
        BibTeX=bibtex_targets,
        CSL=csl_targets,
    )
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
        labels = sorted(sources)
        click.echo(
            f"{' and '.join(labels)} {ngettext('is', 'are', len(labels))} "
            f"missing ID {key}."
        )


if __name__ == "__main__":
    main()
