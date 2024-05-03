"""This file is used to run main from this dir as a dev."""

from __future__ import annotations

import lintception.main
import sys

def main() -> None:
    lintception.main.main(sys.argv[1:])

if __name__ == '__main__':
    main()