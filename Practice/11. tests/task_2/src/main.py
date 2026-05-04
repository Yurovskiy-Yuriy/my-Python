import requests
import os
from dotenv import load_dotenv

def create_folder(token): 
    #Создаем папку:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': 'PY-144'}
    headers = {'Authorization': f'OAuth {token}'}

    print('Cоздаем папку на Яндекс.Диске....')

    response = requests.put(url, params=params, headers=headers)
    
    if response.status_code == 201:
        print('Папка "PY-144" успешно создана!')
    
    elif response.status_code == 409:
        print('Папка "PY-144" уже существует')
    
    elif response.status_code == 401:
        print('Ошибка авторизации! Проверьте токен')
    
    else:
        print(f'Не удалось создать папку "PY-144". Код ошибки: {response.status_code}')
    
    return response.status_code  
   

if __name__ == '__main__':

    load_dotenv()  # Загружаем переменные окружения из .env

    token = os.getenv("token")

    if not token:
        raise ValueError("Не найден Yandex-токен в .env")

    print(create_folder(token))
    
