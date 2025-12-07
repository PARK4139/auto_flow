import re


def extract_def_name(line):
    match = re.match(r'^\s*def\s+(\w+)\(', line)
    return match.group(1) if match else None
