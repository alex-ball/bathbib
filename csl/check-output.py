#!/usr/bin/env python3

"""
This script processes the output of a CSL conversion process to generate a
tidy HTML page; classes are applied according to whether the expected output
was produced.

Usage: check-output.py INPUT-FILE OUTPUT-FILE

Two modes of operation are supported:

1.  INPUT-FILE = *.html

    The input file must be the output of a conversion from LaTeX to HTML by
    pandoc, using its in-built citeproc implementation.

    Pandoc's output changed slightly at about the same time as it switched
    from using an external `pandoc-citeproc` executable to a built-in copy of
    the Haskell `citeproc` library, so this code requires pandoc version 2.11+
    (or thereabouts).

2.  INPUT-FILE = <stem>-output.json

    The input file must be the output of a JSON-to-JSON conversion by
    citeproc-js (via citeproc-js-server). In the same directory as the
    INPUT-FILE there should also be <stem>-raw.html (the pandoc output
    used as the INPUT-FILE in mode 1, above) and <stem>-input.json
    (the JSON that was sent to citeproc-js).

    What happens is that <stem>-raw.html is processed just the same as in
    mode 1, except that the generated content in it is ignored in favour of the
    content from <stem>-output.json. The <stem>-input.json is used to resolve
    citation order, as this isn't preserved in the conversion.
"""

import argparse
import json
import os
import re
import sys

argparser = argparse.ArgumentParser(
    description="Performs checks on input and generates HTML output."
)
argparser.add_argument(
    "infile", metavar="FILE", help="Input file (HTML or JSON)", action="store"
)
argparser.add_argument("outfile", metavar="FILE", help="HTML file to generate")
args = argparser.parse_args()

if not os.path.isfile(args.infile):
    print(f"Please generate {args.infile} before running this script.")
    sys.exit(1)

print("Checking test output for variance...")

refs = dict()
"""Generated references."""
cites = dict()
"""Generated citations."""

pandoc_raw = args.infile

if args.infile.endswith(".json"):
    pandoc_raw = args.infile.replace("-output.json", "-raw.html")
    if not os.path.isfile(pandoc_raw):
        print(f"Please generate {pandoc_raw} before running this script.")
        sys.exit(1)

    json_in = args.infile.replace("-output", "-input")
    if not os.path.isfile(json_in):
        print(f"Please generate {json_in} before running this script.")
        sys.exit(1)
    with open(json_in) as f:
        in_data = json.load(f)

    citation_order = [item["id"] for item in in_data["items"]]

    with open(args.infile) as f:
        cpjs_output = f.read()

    if cpjs_output.startswith("Error"):
        os.remove(args.infile)
        raise RuntimeError(
            f"citeproc-js-server conversion failed: {cpjs_output.strip()}"
        )

    cpjs_output = (
        cpjs_output.replace(r"  <div class=\"csl-entry\">", "<p>")
        .replace("&#38;", "&amp;")
        .replace("1981-01–07", "1981-01-07")
        .replace("https://doi.org/lis-link", "lis-link")
        .replace("</div>", "</p>")
    )
    cpjs_output = re.sub(
        r'<a href=\\"([^"]+)\\">', r'<a href=\\"\1\\" class=\\"uri\\">', cpjs_output
    )
    cpjs_output = re.sub(r"<(/?)i>", r"<\1em>", cpjs_output)
    cpjs_output = re.sub(
        r'<em>([^<]*)<span style=\\"font-style:normal;\\">([^<]*)</span>([^<]*)</em>',
        r"<em>\1<em>\2</em>\3</em>",
        cpjs_output,
    )

    out_data = json.loads(cpjs_output)

    bibliography_order = [item[0] for item in out_data["bibliography"][0]["entry_ids"]]
    references = out_data["bibliography"][1]
    citations = [item[1] for item in out_data["citations"]]

    for i, entryid in enumerate(bibliography_order):
        cpjs_output = references[i]
        if "British National Formulary" in cpjs_output:
            cpjs_output = re.sub(r"(\d{4})[ab]\.", r"\1.", cpjs_output)
        refs[entryid] = cpjs_output

    for i, entryid in enumerate(citation_order):
        cpjs_output = citations[i]
        if "British National Formulary" in cpjs_output:
            cpjs_output = re.sub(r"(\d{4})[ab]\)", r"\1)", cpjs_output)
        cites[entryid] = cpjs_output


output = ""
"""Complete text for writing to file."""

state_n = "normal"
state_t = "target"
state_r = "refs"
state_s = "generated"
state_c = "citations"

state = state_n
"""Parser state."""

entryid = "error"
"""Current entry key."""
targets = dict()
"""Literal reference list entries that the generated text should match."""
current_cite_div = ""
"""Buffer for saving the opening of the test div and citation div."""
saved_cite_divs = dict()
"""Lookup for accumulating citation divs."""
current_ref_div = ""
"""Buffer for saving a generated reference text."""
div_depth = 0
"""For keeping track of divs added to output."""

with open(pandoc_raw, "r") as f:
    i = 0
    for line in f:
        i += 1
        if state == state_n:
            # Looking for a citation line or generated reference.
            if '<span class="citation"' in line:
                # Found citation line.
                m1 = re.search(
                    r'data-cites="(?P<id>[^"]+)">(?P<gen>\(.+\))</span>', line
                )
                if m1:
                    entryid = m1.group("id")
                    gen = m1.group("gen")
                    if entryid in cites:
                        line = line.replace(
                            f">{gen}</span>", f">{cites[entryid]}</span>"
                        )
                        gen = cites[entryid]
                cite_comp = ""
                m2 = re.search(r"(?P<exp>\(.+\)) = ", line)
                test_gen = gen.replace('<span class="nocase">', "").replace(
                    "</span>", ""
                )
                if m2:
                    cite_comp = (
                        " success" if test_gen == m2.group("exp") else " failure"
                    )
                current_cite_div += (
                    f'<div class="test">\n<div class="citation{cite_comp}">\n'
                )
                current_cite_div += line
                current_cite_div += "</div>\n"
                state = state_t
            elif line.startswith('<div id="refs"'):
                # Found generated reference. Swallow this div opener.
                state = state_r
            elif "Test citations</h1>" in line:
                output += line
                state = state_c
            else:
                # Intermediate line, add to output.
                output += line
        elif state == state_c:
            # Looking for a citation line or div tag.
            m1 = re.search(
                r'\w\w: (?P<exp>.*) = (?P<cite><span class="citation".*</span>)</p>',
                line,
            )
            if m1:
                # Found citation line.
                while div_depth:
                    output += "</div>\n"
                    div_depth -= 1
                exp = m1.group("exp")
                gen = re.sub(
                    r'<span class="citation"[^>]*>(.*?)</span>', r"\1", m1.group("cite")
                )
                cite_comp = " success" if gen == exp else " failure"
                output += f'<div class="test">\n<div class="citation{cite_comp}">\n'
                output += line
                output += "</div>\n"
                div_depth += 1
            elif line.startswith("<div"):
                # Found opening tag
                div_depth += 1
                if line.startswith('<div id="refs"'):
                    output += '<div class="target">\n'
                else:
                    output += line
            elif closers := line.count("</div>"):
                # Found closing tag
                div_depth -= closers
                output += line
            elif line.startswith("</body"):
                # End of document, need to close any open divs
                while div_depth:
                    output += "</div>\n"
                    div_depth -= 1
                output += line
            else:
                # Intermediate line, add to output.
                output += line
        elif state == state_t:
            # Looking for a complete target reference text
            # corresponding to the entryid in the most recent citation.
            if line.startswith("<p>"):
                # Found start.
                targets[entryid] = line
            else:
                # Found subsequent line: remove line break.
                targets[entryid] = targets[entryid].strip() + f" {line}"
            if line.endswith("</p>\n"):
                # Found end. Save and clear current cite div.
                saved_cite_divs[entryid] = current_cite_div
                current_cite_div = ""
                state = state_n
        elif state == state_r:
            # Identifying generated reference texts.
            if line.startswith('<div id="ref-'):
                # Found start of generated reference text.
                while div_depth:
                    # This is a second or later ref in a block.
                    # We'll need to close the outer "test" div ourselves.
                    output += "</div>\n"
                    div_depth -= 1
                # Dump out corresponding cite div to output;
                # this contains opener of outer "test" div.
                m = re.search(r'id="ref-(?P<id>[^"]+)"', line)
                if m:
                    entryid = m.group("id")
                    output += saved_cite_divs.get(entryid, "")
                    div_depth += 1
                # Save line for later.
                current_ref_div += line
                state = state_s
            elif line.startswith("</div>"):
                # Found end of raw "refs" div.
                # Use this to close the outer "test" div.
                output += line
                div_depth -= 1
                state = state_n
            else:
                # Shouldn't happen, but for safety add to saved text.
                current_ref_div += line
        elif state == state_s:
            # Inside a generated reference div "ref-x"
            if line.startswith("</div>"):
                # Found end of div.
                # Compare generated and target text.
                ref_comp = ""
                if entryid in targets:
                    ref_comp = (
                        " success" if targets[entryid] == refs[entryid] else " failure"
                    )
                # Output target text wrapped in div
                output += f'<div class="target{ref_comp}">\n'
                output += targets.get(entryid, "")
                output += "</div>\n"
                # Output generated div wrapped in div
                output += f'<div class="references{ref_comp}">\n'
                output += current_ref_div
                output += refs.get(entryid, "")
                output += line
                output += "</div>\n"
                # Clear buffer and see if there's another one.
                current_ref_div = ""
                state = state_r
            elif entryid not in refs:
                # Actual generated reference text. Should be complete on this line.
                line = line.replace('href="https://lis-link@', 'href="lis-link@')
                line = re.sub(r"<span>([“‘].*?[’”])</span>", r"\1", line)
                line = re.sub(r'<span class="nocase">([^<]*)</span>', r"\1", line)
                line = re.sub(r'<a href="(.*?)">', r'<a href="\1" class="uri">', line)
                line = re.sub(
                    r"<em>([^<]*)<i>([^<]*)</i>([^<]*)</em>",
                    r"<em>\1<em>\2</em>\3</em>",
                    line,
                )
                line = f"<p>{line.strip()}</p>\n"
                if entryid not in refs:
                    refs[entryid] = line
        else:
            # Intermediate line, add to output.
            output += line

with open(args.outfile, "w") as f:
    f.write(output)

print("Finished!")
