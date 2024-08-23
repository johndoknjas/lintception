from __future__ import annotations
import sys

from . import linters
from . import my_linter

def main() -> None:
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")
    if (result := linters.run_linters()) != linters.LintResult.SUCCESS:
        print(f"Error: {result.name}")
        sys.exit(0)
    print('\nvulture, mypy, vermin, and pylint found no errors.')
    print('Also, all python files have a future annotations import at the top, and ', end='')
    print('all functions have a return type annotation.\n')
    my_linter.main()

if __name__ == '__main__':
    main()
