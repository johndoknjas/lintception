from __future__ import annotations
from typing import Optional
import sys

from . import linters
from . import my_linter

def main(module_names: Optional[list[str]] = None) -> None:
    """When called as a script, `module_names` is left as None and `sys.argv[:1]` is used.
       If calling main() programatically from another python file though, pass the args
       you want via `module_names`."""
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")

    if module_names is None:
        module_names = sys.argv[1:]
    linters.run_linters(module_names)
    my_linter.main()

if __name__ == '__main__':
    main()
