from __future__ import annotations
import json

from . import linters
from . import my_linter

def read_settings_file() -> dict:
    """Returns the dict represented by the json in `.lintception`.
       If the file doesn't exist, returns an empty dict."""
    try:
        with open('.lintception', 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}

def main() -> None:
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")

    settings: dict[str, float | int] = {'MinVersion': 3.8, 'NumIncompatibleVersions': 2}
    settings.update(read_settings_file())
    linters.run_linters(settings)
    my_linter.main()

if __name__ == '__main__':
    main()
