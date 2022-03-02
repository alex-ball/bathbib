#!/usr/bin/env python3

"""
This processes the output of a conversion from LaTeX to HTML by pandoc, using
its in-built citeproc implementation.

This output changed slightly at about the same time as pandoc switched from
using an external `pandoc-citeproc` executable to a built-in copy of the
Haskell `citeproc` library, so this code now requires pandoc version 2.11+
(or thereabouts).

"""

import os
import sys
import re

infile = "bath-csl-test-raw.html"
outfile = "bath-csl-test.html"

if not os.path.isfile(infile):
    print(f"Please generate {infile} before running this script.")
    sys.exit(1)

print("Checking test output for variance...")

output = ""

state_n = "normal"
state_t = "test"
state_u = "target"
state_r = "refs"
state_s = "generated"

state = state_n

target_strings = list()
output_string = ""

with open(infile, "r") as f:
    i = 0
    for line in f:
        i += 1
        if state == state_n:
            if '<span class="citation"' in line:
                output += '<div class="test">\n<div class="citation">\n'
                output += line
                output += "</div>\n"
                state = state_t
            elif line.startswith("<p>...</p>"):
                continue
            else:
                output += line
        elif state == state_t:
            if line.startswith("<p>...</p>"):
                continue
            if line.startswith("<p>"):
                target_strings.append(line)
                state = state_u
        elif state == state_u:
            if line.startswith("<p>...</p>"):
                continue
            if line.startswith("<p>"):
                target_strings.append(line)
            elif line.startswith('<div id="refs"'):
                state = state_r
        elif state == state_r:
            if line.startswith('<div id="ref-'):
                state = state_s
                output_string += line
            elif line.startswith("</div>"):
                output += line
                state = state_n
            else:
                output_string += line
        elif state == state_s:
            if line.startswith("</div>"):
                output += line
                output += line
                state = state_r
            else:
                line = line.replace('href="https://lis-link@', 'href="lis-link@')
                line = re.sub(r"<span>([“‘].*?[’”])</span>", r"\1", line)
                line = re.sub(r'<span class="nocase">([^<]*)</span>', r"\1", line)
                line = re.sub(r'<a href="(.*?)">', r'<a href="\1" class="uri">', line)
                line = f"<p>{line.strip()}</p>\n"
                output_string += line
                for target in target_strings:
                    if line == target:
                        target_strings.remove(target)
                        output += '<div class="target success">\n'
                        output += target
                        output += "</div>\n"
                        output += '<div class="references success">\n'
                        output += output_string
                        break
                else:
                    target = target_strings.pop(0)
                    output += '<div class="target failure">\n'
                    output += target
                    output += "</div>\n"
                    output += '<div class="references failure">\n'
                    output += output_string
                output_string = ""
        else:
            output += line

with open(outfile, "w") as f:
    f.write(output)

print("Finished!")
