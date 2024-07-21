from __future__ import annotations
import subprocess
from subprocess import PIPE
import vulture # type: ignore
import mypy.api
from enum import Enum

from . import Utils
from .Utils import Func, Line

class LintResult(Enum):
    SUCCESS, MYPY_ERR, VULTURE_ERR, VERMIN_ERR, NO_FUTURE_ANNOT_ERR, NO_FUNC_ANNOT_ERR = range(6)

def test_vulture(settings: dict) -> bool:
    # https://stackoverflow.com/a/59564370/7743427
    v = vulture.Vulture()
    v.scavenge(['.'])
    exclude = settings.get('NoVulture', [])
    return all(any(str(item.filename).endswith(x) for x in exclude) for item in v.get_unused_code())

def test_mypy() -> bool:
    return mypy.api.run(['.']) == (
        f'Success: no issues found in {Utils.num_python_files()} source files\n', '', 0
    )
    # https://mypy.readthedocs.io/en/stable/extending_mypy.html#integrating-mypy-into-another-python-application

def test_vermin(settings: dict) -> bool:
    result = subprocess.run(['vermin', '.'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    expected_ending = (f"Minimum required versions: {settings['MinVersion']}\n" +
                       f"Incompatible versions:     {settings['NumIncompatibleVersions']}")
    return (result.stdout.strip().endswith(expected_ending) and
            (result.returncode, result.stderr) == (0, ''))

def test_future_annotations() -> bool:
    for filename in Utils.get_python_filenames():
        assert filename.endswith(".py")
        with open(filename) as file:
            first_code_line = next(
                (line.rstrip('\n') for line in file.readlines() if Utils.is_code_line(line)), None
            )
            if filename.endswith('__init__.py'):
                if first_code_line is not None:
                    return False
            elif first_code_line != "from __future__ import annotations":
                return False
    return True

def func_has_annotations(lines: list[Line], func: Func) -> bool:
    lines = sorted([l for l in lines if l.line_loc.filename == func.line_loc.filename and
                                        l.line_loc.line_index >= func.line_loc.line_index],
                   key=lambda l: l.line_loc.line_index)
    if ') -> ' not in next(l.line_str for l in lines if ')' in l.line_str):
        print(f"{str(func)} doesn't have a return type annotation")
        return False
    return True

def test_function_annotations() -> bool:
    lines = Utils.get_lines_all_py_files(['tests.py'])
    return all([func_has_annotations(lines, func) for func in Utils.find_funcs(lines)])
    # Using a list comprehension instead of a generator expression so that all functions without
    # annotations are printed to the screen in `func_has_annotations`.

def run_linters() -> LintResult:
    settings: dict[str, float | int] = {'MinVersion': 3.8, 'NumIncompatibleVersions': 2}
    settings.update(Utils.read_json_file('.lintception'))
    Utils.assertions_for_settings_dict(settings)
    tests = (
        (lambda: test_vulture(settings), LintResult.VULTURE_ERR),
        (test_mypy, LintResult.MYPY_ERR),
        (lambda: test_vermin(settings), LintResult.VERMIN_ERR),
        (test_future_annotations, LintResult.NO_FUTURE_ANNOT_ERR),
        (test_function_annotations, LintResult.NO_FUNC_ANNOT_ERR),
    )
    return next((x[1] for x in tests if not x[0]()), LintResult.SUCCESS)
