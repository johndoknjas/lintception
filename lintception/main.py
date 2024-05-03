from __future__ import annotations
from typing import Optional
import sys

from . import linters
from . import my_linter

def main(argv: Optional[list[str]] = None) -> None:
    """When called as a script, `argv` is left as None and `sys.argv` is used.
       If calling main() programatically from another python file though, pass the args
       you want via `argv`."""
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")
    if argv is None:
        argv = sys.argv
    linters.run_linters(argv[1:])
    my_linter.main()

if __name__ == '__main__':
    main()
