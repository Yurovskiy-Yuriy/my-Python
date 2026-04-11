'''
Создать функцию send_config_commands

Функция подключается по SSH (с помощью netmiko) к одному устройству
и выполняет перечень команд в конфигурационном режиме на основании
переданных аргументов.

Параметры функции:
• device - словарь с параметрами подключения к устройству
• config_commands - список команд, которые надо выполнить

Функция возвращает строку с результатами выполнения команды:
In [7]: r1
Out[7]:
{'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
        'password': 'cisco',
    'secret': 'cisco'}
    
In [8]: commands
Out[8]: ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']

In [9]: result = send_config_commands(r1, commands)

In [10]: result
Out[10]: 'config term\nEnter configuration commands, one per line. End with CNTL/Z.\
,→nR1(config)#logging 10.255.255.1\nR1(config)#logging buffered 20010\nR1(config)#no␣
,→logging console\nR1(config)#end\nR1#'

In [11]: print(result)

config term
Enter configuration commands, one per line. End with CNTL/Z.
R1(config)#logging 10.255.255.1
R1(config)#logging buffered 20010
R1(config)#no logging console
R1(config)#end
R1#

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с по-
мощью функции send_config_commands.
commands = [
'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
]
'''

import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def send_config_commands(device, command):
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

if __name__ == "__main__":
    try:
        with open("devices_3.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_3.yaml не найден.")
        exit(1)
    
    commands = ['show', 'show version']  # Список команд для выполнения

    for device in devices:
        results = []
        print(f"Подключение к {device['host']}... ")
        
        for cmd in commands:  # Перебираем команды
            result = send_config_commands(device, cmd)
            if result is not None:
                results.append(f"=== Команда: {cmd} ===")
                results.append(result)
                results.append('')
        
        # Заголовок добавляем один раз, если есть хоть какой-то результат
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
            
        # Сохранение каждого устройства в отдельный файл
        filename = f"test_{device['host']}.txt"
        print(f'Сохранение конфигурации в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e:  # Если запись в файл не удалась (например, нет прав), выводим в консоль
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')