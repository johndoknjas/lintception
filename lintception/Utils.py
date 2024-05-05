from __future__ import annotations
import glob

def assertions_for_settings_dict(settings: dict) -> None:
    assert (settings.keys() == {'MinVersion', 'NumIncompatibleVersions'} and
            isinstance(settings['MinVersion'], float) and
            isinstance(settings['NumIncompatibleVersions'], int))

def is_code_line(line: str) -> bool:
    return (bool(line.strip()) and not line.lstrip().startswith(('#', '"""')) and
            not line.rstrip().endswith('"""'))

def num_python_files() -> int:
    return len(list(glob.iglob('**/*.py', recursive=True)))