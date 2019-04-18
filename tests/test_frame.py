import pytest

from objects import frame


TEST_CASES = [
    ((None, None), (2, 2)),
    ((0, 0), (0, 0)),
    ((1, 3), (1, 3)),
]


@pytest.mark.parametrize("row_column,expected", TEST_CASES)
def test_override(row_column, expected):
    frame_instance = frame.Frame(None, " ", 2, 2)
    result = frame_instance._override_row_and_column(*row_column)
    assert result == expected
