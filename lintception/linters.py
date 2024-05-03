from __future__ import annotations
import subprocess
from subprocess import PIPE
import glob
import vulture # type: ignore
import mypy.api

from typing import Optional

def test_vulture() -> None:
    v = vulture.Vulture()
    v.scavenge(['.'])
    assert not v.get_unused_code()
    # https://stackoverflow.com/a/59564370/7743427

def test_mypy() -> None:
    assert mypy.api.run(['.']) == (f'Success: no issues found in {num_python_files()} source files\n', '', 0)
    # https://mypy.readthedocs.io/en/stable/extending_mypy.html#integrating-mypy-into-another-python-application

def test_vermin(module_names: Optional[list[str]]) -> None:
    if not module_names:
        return
    result = subprocess.run(['vermin', module_names[0]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    expected_ending = "Minimum required versions: 3.8\nIncompatible versions:     2"
    assert result.stdout.strip().endswith(expected_ending)
    assert (result.returncode, result.stderr) == (0, '')
    test_vermin(module_names[1:])

def test_future_annotations() -> None:
    for filename in glob.iglob('**/*.py', recursive=True):
        assert filename.endswith(".py")
        with open(filename) as file:
            first_code_line = next(
                (line.rstrip('\n') for line in file.readlines() if is_code_line(line)), None
            )
            if filename.endswith('__init__.py'):
                assert first_code_line is None
            else:
                assert first_code_line == "from __future__ import annotations"

# Helpers:

def is_code_line(line: str) -> bool:
    return (bool(line.strip()) and not line.lstrip().startswith(('#', '"""')) and
            not line.rstrip().endswith('"""'))

def num_python_files() -> int:
    return len(list(glob.iglob('**/*.py', recursive=True)))

def run_linters(module_names: Optional[list[str]] = None) -> None:
    test_vulture()
    test_mypy()
    test_vermin(module_names)
    test_future_annotations()
