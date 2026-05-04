import pytest
from src.main_3 import solve

@pytest.mark.parametrize('list_numbers,expected',
                         (([15, 23, 47, 58, 61, 74, 82, 93, 36, 49], ([47, 74, 36], 3)),
                          ([7, 18, 29, 41, 53, 64, 75, 86], ([29, 64], 2)),
                         ([3, 11, 24, 37, 42, 56, 68, 79, 85, 94, 20, 31], ([24, 56, 85, 31], 4)),
                         ([91, 52, 73, 14, 35, 66], ([73, 66], 2)),
                         ))

def test_finding_discriminant(list_numbers, expected):
    result = solve(list_numbers)
    assert result == expected, \
        f'Ожидаемое значение {expected} не соответствует рассчитанному {result}'
