from __future__ import annotations
import subprocess
from subprocess import PIPE
from io import StringIO
from enum import Enum

import vulture # type: ignore
import mypy.api
from pylint.lint import Run, pylinter
from pylint.reporters.text import TextReporter

from . import Utils
from .Utils import Func, Line

class LintResult(Enum):
    MYPY_ERR, VULTURE_ERR, VERMIN_ERR, PYLINT_ERR, NO_FUTURE_ANNOT_ERR, NO_FUNC_ANNOT_ERR = range(6)

def test_vulture(settings: dict) -> bool:
    # https://stackoverflow.com/a/59564370/7743427
    v = vulture.Vulture()
    v.scavenge(['.'])
    exclude = settings.get('NoVulture', [])
    return all(any(str(item.filename).endswith(x) for x in exclude) for item in v.get_unused_code())

def test_mypy() -> bool:
    result = mypy.api.run(['.'])
    return (result[0].endswith(f'Success: no issues found in {Utils.num_python_files()} source files\n') and
            result[1:] == ('', 0))
    # https://mypy.readthedocs.io/en/stable/extending_mypy.html#integrating-mypy-into-another-python-application

def test_vermin(settings: dict) -> bool:
    result = subprocess.run(['vermin', '.'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    expected_ending = (f"Minimum required versions: {settings['MinVersion']}\n" +
                       f"Incompatible versions:     {settings['NumIncompatibleVersions']}")
    return (result.stdout.strip().endswith(expected_ending) and
            (result.returncode, result.stderr) == (0, ''))

def test_pylint(settings: dict) -> bool:
    pylinter.MANAGER.clear_cache()
    pylint_output = StringIO()
    Run(["--disable=C0301, C0302, C0103, R0902, R0913, C0116, R0911, R0914, R0912, C0115, C0123, R0904, " +
         "C0114, I1101, W1510, W1514, W0108, C0304, E0401, W0719, R0801, R1729",
         settings.get('module', '.')], reporter=TextReporter(pylint_output), exit=False)
    lines = pylint_output.getvalue().split('\n')
    if any("Your code has been rated at 10.00/10" in line for line in lines):
        return True
    for line in lines:
        print(line)
    return False

def test_future_annotations(settings: dict) -> bool:
    for filename in Utils.get_python_filenames():
        assert filename.endswith(".py")
        if any(filename.endswith(x) for x in settings.get('NoFutureAnnot', [])):
            continue
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
    has_annotations = [func_has_annotations(lines, func) for func in Utils.find_funcs(lines)]
    # Using a list instead of a generator expression so that all functions without
    # annotations are printed to the screen in `func_has_annotations`.
    print('\n\n')
    return all(has_annotations)

def run_linters() -> list[LintResult]:
    settings: dict[str, float | int] = {'MinVersion': 3.8, 'NumIncompatibleVersions': 2}
    settings.update(Utils.read_json_file('.lintception'))
    Utils.assertions_for_settings_dict(settings)
    tests = (
        (test_future_annotations(settings), LintResult.NO_FUTURE_ANNOT_ERR),
        (test_function_annotations(), LintResult.NO_FUNC_ANNOT_ERR),
        (test_vulture(settings), LintResult.VULTURE_ERR),
        (test_mypy(), LintResult.MYPY_ERR),
        (test_vermin(settings), LintResult.VERMIN_ERR),
        (test_pylint(settings), LintResult.PYLINT_ERR),
    )
    return [x[1] for x in tests if not x[0]]