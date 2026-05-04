import pytest
from src.main_2 import vote

@pytest.mark.parametrize('list_numbers,expected',
                         (([1,1,1,2,3], 1),
                          ([1,5,1,5,5], 5),
                         ([3,3,1,2,3], 3),
                         ([1,9,9,9,3], 9),
                         ))

def test_finding_discriminant(list_numbers, expected):
    result = vote(list_numbers)
    assert result == expected, \
        f'Ожидаемое значение {expected} не соответствует рассчитанному {result}'
