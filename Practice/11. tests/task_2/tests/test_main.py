import pytest
from src.main import create_folder

import requests
import os
from dotenv import load_dotenv

'''
ВНИМАНИЕ! для проверки необхоимо создать файл .env
с текстом формата: token=<токен_от_Yandex_диска>
'''
load_dotenv()  # Загружаем переменные окружения из .env

token = os.getenv("token")

if not token:
    raise ValueError("Не найден Yandex-токен в .env")


@pytest.mark.parametrize('token,expected,description', [
    (token, [201, 409], "Корректный токен - папка создана или уже существует"),
    ("invalid_token", [401], "Неверный токен"),
    ("", [401], "Пустой токен"),
    (None, [401], "None вместо токена"),
])

def test_finding_discriminant(token, expected, description):
    result = create_folder(token)
    assert result in  expected, \
        f'Ожидаемое значение {expected} не соответствует рассчитанному {result}'
