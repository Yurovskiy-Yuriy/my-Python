"""
Скрипт позволяет выбрать команду, отправить её одновременно на несколько устройств 
(используя многопоточность) и получить результат в виде структурированных данных,
(производится парсинга текстовых выводов команд по шаблонам).

1. пользователь выбирает нужную команду из интерактивного меню.

2. Многопоточность: быстрая параллельная работа с большим количеством устройств.

3. Структурированный вывод: парсинг полученных данных в формат списка словарей 
   для удобства дальнейшей обработки.
"""

from pprint import pprint
import textfsm
import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor, as_completed



'''************парсим вывод команды*****************'''
def parse_command_dynamic(template, command_output):

    # 1. Загружаем шаблон
    with open(template) as f:
        re_table = textfsm.TextFSM(f)

    # 2. Парсим текст с помощью шаблона
    structured_data = re_table.ParseText(command_output)
    
    # 3. Формируем список словарей
    result = []

    for item in structured_data:
        row = dict(zip(re_table.header, item)) # Создаём словарь

        result.append(row)
    
    return result

"**********отправляем команды на маршрутизатор**************"
def send_command_to_device(device, command):
    # Создаем словарь для подключения, совместимый с Netmiko
    netmiko_device = {
        'device_type': 'linux',  # Dionis NX — Linux-based устройство
        'host': device['host'],
        'username': device['username'],
        'password': device['password'],
        'timeout': device.get('timeout', 10),
    }

    try:
        # Устанавливаем соединение с устройством
        with ConnectHandler(**netmiko_device) as ssh:
            # Отправляем команду и получаем вывод
            output = ssh.send_command(command)
            return output
    except NetMikoTimeoutException:
        print(f'Превышено время ожидания соединения {device["host"]}')
    except NetMikoAuthenticationException:
        print(f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)')
    except Exception as e:
        print(f'Не удалось подключиться к {device["host"]}: {e}')
    return None


"**********подключение к маршрутизатору**************"
def connect_to_device(device, command, template_path):
    print(f"Подключение к {device['host']}...")
        
    result = send_command_to_device(device, command) 
    
    if result is not None:
        # Парсим вывод
        parsed_result = parse_command_dynamic(template_path, result)
        return {
            'host': device['host'],
            'command': command,
            'result': parsed_result
        }
        
    return None
    
    

if __name__ == "__main__":
    
    # получаем необходимую команду
    print('1. show cdp neighbors detail\n2. show clock\n3. show ip interface brief\n4. show ip route ospf\n5. show version')
    dic_command = {1:'show cdp neighbors detail', 2:'show clock', 3:'show ip interface brief', 4:'show ip route ospf', 5:'show version',}
    print()
    number_command = int(input('Введите номер команды: '))
    
    while  number_command > 5 or number_command <= 0 :
        number_command = int(input('Неправильная команда, повотрите: '))
    command = dic_command[number_command]
    
    # получаем нужный шаблон .template в зависимости от команды
    with open('21.5/templates/index', 'r') as file:
        output = file.readlines()
        for out in output:
            out_split = out.split(',')
            if command in out_split[3]:
                file_templates = out_split[0]     # sh_cdp_n_det.template

    # подключаемся к устройсву, отправляем команду и получаем результат
    file_yaml = "21.5/log/devices_cisco.yaml"
    template_path = f'21.5/templates/{file_templates}'
    
    #читаем yaml-файл
    try:
        with open(file_yaml) as f:
                devices = yaml.safe_load(f)
    except FileNotFoundError:
            print(f"Файл {file_yaml} не найден.")
            exit(1) 
        
        
    # Многопоточное выполнение
    results = []
    dic_result = {}
    final_results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Создаём список будущих результатов
        futures = []

        for device in devices:
            future = executor.submit(connect_to_device, device, command, template_path) 
            futures.append(future)
                    
        # Обрабатываем результаты по мере их готовности
        for future in as_completed(futures):
            res = future.result()
            if res:
                results.append(res) 
                dic_result[res['host']] = res['result'] # создаем словарь со значениями
                final_results.append(dic_result)
    print()
    pprint(final_results)
    

# 1. show cdp neighbors detail
# 2. show clock
# 3. show ip interface brief
# 4. show ip route ospf
# 5. show version

# Введите номер команды: 2
# Подключение к 192.168.1.10...
# Подключение к 192.168.1.11...
# Подключение к 192.168.1.12...

# [{'192.168.1.10': [{'month': 'May',
#                   'monthday': '19',
#                   'time': '15:45:21',
#                   'timezone': 'UTC',
#                   'weekday': 'Tue',
#                   'year': '2026'}]},
#  {'192.168.1.11': [{'month': 'May',
#                   'monthday': '19',
#                   'time': '15:45:21',
#                   'timezone': 'UTC',
#                   'weekday': 'Tue',
#                   'year': '2026'}]},
#  {'192.168.1.12': [{'month': 'May',
#                   'monthday': '19',
#                   'time': '15:45:21',
#                   'timezone': 'UTC',
#                   'weekday': 'Tue',
#                   'year': '2026'}]}]
            
           
            
            