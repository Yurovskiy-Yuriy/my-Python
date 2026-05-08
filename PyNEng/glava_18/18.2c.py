'''Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким обра-
зом: Если при выполнении команды возникла ошибка, спросить пользователя надо ли выпол-
нять остальные команды.

Варианты ответа [y]/n:
    • y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой
комбинации воспринимается как y
    • n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
    • первый словарь с выводом команд, которые выполнились без ошибки
    • второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
    • ключ - команда
    • значение - вывод с выполнением команд
Проверить работу функции можно на одном устройстве.
Пример работы функции:
In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker.
,→" на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
{'logging': 'config term\n'
            'Enter configuration commands, one per line. End with CNTL/Z.\n'
            'R1(config)#logging\n'
            '% Incomplete command.\n'
            '\n'
            'R1(config)#',
'logging 0255.255.1': 'config term\n'
            'Enter configuration commands, one per line. End with '
            'CNTL/Z.\n'
            'R1(config)#logging 0255.255.1\n'
            ' ^\n'
            "% Invalid input detected at '^' marker.\n"
            '\n'
            'R1(config)#'})

Списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
correct_commands = ['logging buffered 20010', 'ip http server']

commands = commands_with_errors + correct_commands
'''

# скрипт написан для DionisNX

from pprint import pprint
import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def send_config_commands(device, config_commands):
    
    # Создаем словарь для подключения, совместимый с Netmiko
    netmiko_device = {
        'device_type': 'linux',  # Dionis NX — Linux-based устройство
        'host': device['host'],
        'username': device['username'],
        'password': device['password'],
        'timeout': device.get('timeout', 10),
    }

    good_commands = {}
    bad_commands = {}

    try:
        # Устанавливаем соединение с устройством
        with ConnectHandler(**netmiko_device) as ssh:
            print(f"\nПодключение к {device['host']}...")
        
            for command in config_commands:
                print(f"\nВыполнение команды '{command}'...")
                
                try:
                    # Отправляем команду и получаем вывод
                    output = ssh.send_command(command)
                    good_commands[command] = output
                    
            
                except Exception as e:
                    bad_commands[command] = str(e)
                    
                    #Отправляем Ctrl+C (очищаем строку)
                    output = ssh.send_command_timing('\x03')
                    
                    print(f'Команда выполнилась с ошибкой')
                    
                    user_input = input("Продолжать выполнять команды? [y]/n: ")
                    if user_input.lower() in ['n', 'no']:
                        print("Выполнение команд прервано пользователем.")
                        break   
            
    except NetMikoTimeoutException:
        return {'status': 'error', 'code': 'timeout', 'message': f'Превышено время ожидания соединения {device["host"]}'}
    except NetMikoAuthenticationException:
        return {'status': 'error', 'code': 'auth_error', 'message': f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)'}

    return (good_commands, bad_commands)


if __name__ == "__main__":

    try:
        with open("devices_4.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_4.yaml не найден.")
        exit(1)
    
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['show', 'show version']
    commands = commands_with_errors + correct_commands

    # Проверяем работу на первом устройстве из списка
    for device in devices:
        result = send_config_commands(device, commands)
        print("\nРезультат выполнения:")
        pprint(result)
        
        

        

 