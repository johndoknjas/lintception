from __future__ import annotations

from . import linters
from . import my_linter

def main() -> None:
    if not __debug__:
        raise RuntimeError("Python isn't running in the default debug mode.")
    my_linter.main()
    if errors := linters.run_linters():
        for error in errors:
            print(f"Error: {error.name}")
    else:
        print('\nvulture, mypy, vermin, and pylint found no errors.')
        print('Also, all python files have a future annotations import at the top, and ', end='')
        print('all functions have a return type annotation.\n')

if __name__ == '__main__':
    main()
