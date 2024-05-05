from __future__ import annotations
from typing import Optional
import sys
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

def main(module_names: Optional[list[str]] = None) -> None:
    """When called as a script, `module_names` is left as None and `sys.argv[:1]` is used.
       If calling main() programatically from another python file though, pass the args
       you want via `module_names`."""
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")
    if module_names is None:
        module_names = sys.argv[1:]

    settings: dict[str, float | int | list[str]] = {
        'ModuleNames': [],
        'MinVersion': 3.8,
        'NumIncompatibleVersions': 2
    }
    settings.update(read_settings_file())
    if module_names:
        settings['ModuleNames'] = module_names
    assert settings['ModuleNames']
    linters.run_linters(settings)
    my_linter.main()

if __name__ == '__main__':
    main()
