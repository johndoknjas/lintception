from __future__ import annotations
import glob
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class LineLoc:
    line_index: int
    filename: str

@dataclass
class Func:
    name: str
    line_loc: LineLoc

@dataclass
class Line:
    line_loc: LineLoc
    line_str: str

def assertions_for_settings_dict(settings: dict) -> None:
    assert (isinstance(settings['MinVersion'], float) and
            isinstance(settings['NumIncompatibleVersions'], int))

def is_code_line(line: str) -> bool:
    return (bool(line.strip()) and not line.lstrip().startswith(('#', '"""')) and
            not line.rstrip().endswith('"""'))

def get_python_filenames() -> list[str]:
    return list(glob.iglob('**/*.py', recursive=True))

def num_python_files() -> int:
    return len(get_python_filenames())

def read_json_file(filename: str) -> dict:
    """Returns the dict represented by the json. If the file doesn't exist, returns an empty dict."""
    try:
        with open(filename, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}

def get_lines_all_py_files(filenames_exclude: Optional[list[str]] = None) -> list[Line]:
    lines = []
    for filename in get_python_filenames():
        if filenames_exclude and filename in filenames_exclude:
            continue
        with open(filename) as file:
            for i, line_str in enumerate(file.read().splitlines()):
                lines.append(Line(LineLoc(i+1, filename), line_str))
    return lines

def find_funcs(lines: list[Line]) -> list[Func]:
    """`lines` are all the lines in all the .py files. The function will go through it and find all
        function definitions, putting each function name and line location into the list that's returned."""
    funcs: list[Func] = []
    for line in lines:
        words = line.line_str.split()
        if not words or words[0] != 'def':
            continue
        assert '(' in words[1]
        funcs.append(Func(words[1].split('(')[0], line.line_loc))
    return funcs