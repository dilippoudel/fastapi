import pytest
from app.calculation import add

@pytest.mark.parametrize("x, y, result", [
    (2, 4, 6),
    (5, -3, 2),
    (8, 0, 8)
])
def test_add(x, y, result):
    assert add(x, y) == result

