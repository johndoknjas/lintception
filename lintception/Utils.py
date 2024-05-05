from __future__ import annotations

import glob
from typing import Type

def is_list_of(lst: list, type_name: Type) -> bool:
    return isinstance(lst, list) and all(isinstance(x, type_name) for x in lst)

def assertions_for_settings_dict(settings: dict) -> None:
    assert (settings.keys() == {'ModuleNames', 'MinVersion', 'NumIncompatibleVersions'} and
            is_list_of(settings['ModuleNames'], str) and
            isinstance(settings['MinVersion'], float) and
            isinstance(settings['NumIncompatibleVersions'], int))

def is_code_line(line: str) -> bool:
    return (bool(line.strip()) and not line.lstrip().startswith(('#', '"""')) and
            not line.rstrip().endswith('"""'))

def num_python_files() -> int:
    return len(list(glob.iglob('**/*.py', recursive=True)))