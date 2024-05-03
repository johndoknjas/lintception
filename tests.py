from __future__ import annotations
import subprocess
from subprocess import PIPE
import glob
import vulture # type: ignore
import mypy.api

class Tests:
    """
    @pytest.fixture
    def example_fixture(self):
        pass
    """

    def test_vulture(self):
        v = vulture.Vulture()
        v.scavenge(['.'])
        assert not v.get_unused_code()
        # https://stackoverflow.com/a/59564370/7743427

    def test_mypy(self):
        assert mypy.api.run(['.']) == ('Success: no issues found in 19 source files\n', '', 0)
        # https://mypy.readthedocs.io/en/stable/extending_mypy.html#integrating-mypy-into-another-python-application

    def test_vermin(self):
        result = subprocess.run(['vermin', 'lintception'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        expected_output = """Tips:
            - Generic or literal annotations might be in use. If so, try using: --eval-annotations
            But check the caveat section: https://github.com/netromdk/vermin#caveats
            - You're using potentially backported modules: dataclasses, enum, typing
            If so, try using the following for better results: --backport dataclasses --backport enum --backport typing
            - Since '# novm' or '# novermin' weren't used, a speedup can be achieved using: --no-parse-comments
            (disable using: --no-tips)

            Minimum required versions: 3.8
            Incompatible versions:     2"""
        assert (
            [line.strip() for line in expected_output.splitlines()] ==
            [line.strip() for line in result.stdout.splitlines()]
        )
        assert (result.returncode, result.stderr) == (0, '')

    def test_future_annotations(self):
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

if __name__ == '__main__':
    raise RuntimeError("Should call with pytest")
