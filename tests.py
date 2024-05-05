from __future__ import annotations

import lintception.main

class Tests:
    """
    @pytest.fixture
    def example_fixture(self):
        pass
    """

    def test_self(self):
        lintception.main.main()

if __name__ == '__main__':
    raise RuntimeError("Should call with pytest")
