from __future__ import annotations

from lintception import linters

class Tests:
    """
    @pytest.fixture
    def example_fixture(self):
        pass
    """

    def test_self(self):
        assert linters.run_linters() == linters.LintResult.SUCCESS

if __name__ == '__main__':
    raise RuntimeError("Should call with pytest")
