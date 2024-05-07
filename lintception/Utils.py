from __future__ import annotations
import glob
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class Func:
    name: str
    line_index: int

def assertions_for_settings_dict(settings: dict) -> None:
    assert (settings.keys() == {'MinVersion', 'NumIncompatibleVersions'} and
            isinstance(settings['MinVersion'], float) and
            isinstance(settings['NumIncompatibleVersions'], int))

def is_code_line(line: str) -> bool:
    return (bool(line.strip()) and not line.lstrip().startswith(('#', '"""')) and
            not line.rstrip().endswith('"""'))

def num_python_files() -> int:
    return len(list(glob.iglob('**/*.py', recursive=True)))

def read_json_file(filename: str) -> dict:
    """Returns the dict represented by the json. If the file doesn't exist, returns an empty dict."""
    try:
        with open(filename, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}

def get_lines_all_py_files(filenames_exclude: Optional[list[str]] = None) -> list[str]:
    lines = []
    for filename in glob.iglob('**/*.py', recursive=True):
        if filenames_exclude and filename in filenames_exclude:
            continue
        with open(filename) as file:
            lines.extend(file.read().splitlines())
    return lines

def find_funcs(lines: list[str]) -> list[Func]:
    """`lines` are all the lines of code. The function will go through it and find all function definitions,
       putting each function name and line index into the list that's returned."""
    funcs: list[Func] = []
    for i, code_line in enumerate(lines):
        words = code_line.split()
        if not words or words[0] != 'def':
            continue
        assert '(' in words[1]
        funcs.append(Func(words[1].split('(')[0], i))
    return funcs