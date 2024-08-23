from __future__ import annotations
from . import Utils
from .Utils import Func, Line

def find_func_references(lines: list[Line], func: Func) -> list[Line]:
    """Note that this doesn't include the function's definition."""
    return [l for l in lines if func.name in l.line_str and func.line_loc != l.line_loc]

def func_ref_distance(elem: tuple[Func, Line]) -> tuple[int, int, int]:
    """Returns a 'greater' tuple if the 'distance' between the function and reference is greater.
       Order of properties by importance: being in diff files, the reference being before the function,
       and the line distance between the two. The latter properties are only considered if the func and ref
       are in the same file."""
    in_same_file = elem[0].line_loc.filename == elem[1].line_loc.filename
    if not in_same_file:
        return (1,1,1)
    ref_after_func = elem[0].line_loc.line_index < elem[1].line_loc.line_index
    line_abs_dist = abs(elem[0].line_loc.line_index - elem[1].line_loc.line_index)
    return (-1, (-1 if ref_after_func else 1), line_abs_dist)

def main() -> None:
    lines = Utils.get_lines_all_py_files(["tests.py"])
    funcs: list[Func] = Utils.find_funcs(lines)
    funcs_used_once: list[tuple[Func, Line]] = []
    print("\n\nUnused functions:\n")
    for func in funcs:
        references = find_func_references(lines, func)
        if len(references) == 0:
            print(f"******{func} is unused******")
        elif len(references) == 1:
            funcs_used_once.append((func, references[0]))
    funcs_used_once.sort(key=func_ref_distance)
    print("\n\nFunctions used only once:\n")
    for f in funcs_used_once:
        print(f"Func {f[0].name} (line {f[0].line_loc.line_index} of {f[0].line_loc.filename}) " +
              f"is only referenced at line {f[1].line_loc.line_index} of {f[1].line_loc.filename}")
    print('\n\n\n')