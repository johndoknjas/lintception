from __future__ import annotations

from . import linters
from . import my_linter
from . import Utils

def main() -> None:
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")
    settings: dict[str, float | int] = {'MinVersion': 3.8, 'NumIncompatibleVersions': 2}
    settings.update(Utils.read_json_file('.lintception'))
    linters.run_linters(settings)
    my_linter.main()

if __name__ == '__main__':
    main()
