from __future__ import annotations
import glob
import json

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