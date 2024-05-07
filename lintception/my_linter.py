from __future__ import annotations
from . import Utils
from .Utils import Func

def find_func_references(lines: list[str], func: Func) -> list[int]:
    """Note that this doesn't include the function's definition."""
    return [i for (i, line) in enumerate(lines) if func.name in line and i != func.line_index]

def main() -> None:
    lines = Utils.get_lines_all_py_files(["tests.py"])
    funcs: list[Func] = Utils.find_funcs(lines)
    funcs_used_once: list[tuple[Func, int]] = []
    print("\n\nUnused functions:\n")
    for func in funcs:
        references = find_func_references(lines, func)
        if len(references) == 0:
            print(f"******{func} is unused******")
        elif len(references) == 1:
            funcs_used_once.append((func, references[0]))
    funcs_used_once.sort(key=lambda f:
                         ((defined_vs_used := f[0].line_index-f[1]) < 0, -abs(defined_vs_used)),
                         reverse=True)
    print("\n\nFunctions used only once:\n")
    for f in funcs_used_once:
        print(f"{f[0]} is only referenced at line index {f[1]}")