#! /usr/bin/env python3
import os
import re
import subprocess
import sys

# Get mapping of IDs to target output from DTX file:

targets = dict()

current_id = None
with open("bath-bst.dtx") as f:
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


if not os.path.isfile("bath-bst.bbl"):
    subprocess.run(["make", "bath-bst.pdf"], check=True)
    if not os.path.isfile("bath-bst.bbl"):
        print("Could not generate bbl file.")
        sys.exit(1)

# Process BBL file so we get a pattern of
# 1. \bibitem line
# 2. Formatted output lines
# 3. Blank line

preamble = True
lines = list()
current_line = list()
with open("bath-bst.bbl") as f:
    for line in f:
        # Ignore first few lines:
        if preamble:
            if line.startswith("\\bibitem"):
                preamble = False
            else:
                continue

        # Combine most recent lines:
        current_line.append(line.strip())
        l = " ".join(current_line)
        if l.count("[") == l.count("]") and l.count("{") == l.count("}"):
            # Line is (probably!) syntactically complete
            lines.append(l)
            current_line.clear()
            continue

# Process lines again to get mapping of IDs to actual output

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
                outputs[current_id] = outputs[current_id].replace(m.group(0), replacement)
        current_id = None
        state = [NORMAL]
        level = 1
        exit_arg = 0
        exit_gobble = 0
        continue

    line = (
        line
        .replace("\\@", "")
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

for id, target in targets.items():
    if id not in outputs:
        print(f"Missing output for {id}.\n")
        continue
    elif outputs[id] == target:
        continue

    print(id)
    print(f"Target: {target}")
    print(f"Output: {outputs[id]}\n")
