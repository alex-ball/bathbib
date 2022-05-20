#!/usr/bin/env python3

"""
This processes the output of a conversion from LaTeX to HTML by pandoc, using
its in-built citeproc implementation.

This output changed slightly at about the same time as pandoc switched from
using an external `pandoc-citeproc` executable to a built-in copy of the
Haskell `citeproc` library, so this code now requires pandoc version 2.11+
(or thereabouts).

"""
import argparse
from collections import deque
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
cites = dict()

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

state_n = "normal"
state_t = "test"
state_u = "target"
state_r = "refs"
state_s = "generated"

state = state_n

entryid = "error"
targets = dict()
target_strings = dict()
output_string = ""
div_depth = 0

with open(pandoc_raw, "r") as f:
    i = 0
    for line in f:
        i += 1
        if state == state_n:
            if '<span class="citation"' in line:
                m1 = re.search(
                    r'data-cites="(?P<id>[^"]+)">(?P<gen>\(.+\))</span>', line
                )
                if m1:
                    entryid = m1.group("id")
                    gen = m1.group("gen")
                    if entryid in cites:
                        line = line.replace(f">{gen}</span>", f">{cites[entryid]}</span>")
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
                output_string += (
                    f'<div class="test">\n<div class="citation{cite_comp}">\n'
                )
                output_string += line
                output_string += "</div>\n"
                state = state_t
            elif line.startswith('<div id="refs"'):
                state = state_r
            else:
                output += line
        elif state == state_t:
            if line.startswith("<p>"):
                targets[entryid] = line
            else:
                targets[entryid].replace("\n", " " + line)
            if line.endswith("</p>\n"):
                target_strings[entryid] = output_string
                output_string = ""
                state = state_n
        elif state == state_r:
            if line.startswith('<div id="ref-'):
                while div_depth:
                    output += "</div>\n"
                    div_depth -= 1
                m = re.search(r'id="ref-(?P<id>[^"]+)"', line)
                if m:
                    entryid = m.group("id")
                    output += target_strings.get(entryid, "")
                    div_depth += 1
                state = state_s
                output_string += line
            elif line.startswith("</div>"):
                output += line
                div_depth -= 1
                state = state_n
            else:
                output_string += line
        elif state == state_s:
            if line.startswith("</div>"):
                ref_comp = ""
                if entryid in targets:
                    ref_comp = (
                        " success" if targets[entryid] == refs[entryid] else " failure"
                    )
                output += f'<div class="target{ref_comp}">\n'
                output += targets.get(entryid, "")
                output += "</div>\n"
                output += f'<div class="references{ref_comp}">\n'
                output += output_string
                output += refs.get(entryid, "")
                output += line
                output += line
                output_string = ""
                state = state_r
            elif entryid not in refs:
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
            output += line

with open(args.outfile, "w") as f:
    f.write(output)

print("Finished!")
