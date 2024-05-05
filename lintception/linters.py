from __future__ import annotations
import subprocess
from subprocess import PIPE
import glob
import vulture # type: ignore
import mypy.api

from . import Utils

def test_vulture() -> None:
    v = vulture.Vulture()
    v.scavenge(['.'])
    assert not v.get_unused_code()
    # https://stackoverflow.com/a/59564370/7743427

def test_mypy() -> None:
    assert mypy.api.run(['.']) == (
        f'Success: no issues found in {Utils.num_python_files()} source files\n', '', 0
    )
    # https://mypy.readthedocs.io/en/stable/extending_mypy.html#integrating-mypy-into-another-python-application

def test_vermin(settings: dict) -> None:
    result = subprocess.run(['vermin', '.'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    expected_ending = (f"Minimum required versions: {settings['MinVersion']}\n" +
                       f"Incompatible versions:     {settings['NumIncompatibleVersions']}")
    assert result.stdout.strip().endswith(expected_ending)
    assert (result.returncode, result.stderr) == (0, '')

def test_future_annotations() -> None:
    for filename in glob.iglob('**/*.py', recursive=True):
        assert filename.endswith(".py")
        with open(filename) as file:
            first_code_line = next(
                (line.rstrip('\n') for line in file.readlines() if Utils.is_code_line(line)), None
            )
            if filename.endswith('__init__.py'):
                assert first_code_line is None
            else:
                assert first_code_line == "from __future__ import annotations"

def run_linters(settings: dict) -> None:
    Utils.assertions_for_settings_dict(settings)
    test_vulture()
    test_mypy()
    test_vermin(settings)
    print('vulture, mypy, and vermin found no errors!\n')
    test_future_annotations()
