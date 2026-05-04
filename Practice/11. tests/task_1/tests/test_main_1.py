import pytest
from src.main_1 import solution

@pytest.mark.parametrize('a,b,c,expected',
                         ((1, 8, 15, (-3.0, -5.0)),
                          (1, -13, 12, (12.0, 1.0)),
                         (-4, 28, -49, 3.5),
                         (1, 1, 1, 'корней нет'),
                         ))

def test_finding_discriminant(a, b, c, expected):
    result = solution(a, b, c)
    assert result == expected, \
        f'Ожидаемое значение {expected} не соответствует рассчитанному {result}'
