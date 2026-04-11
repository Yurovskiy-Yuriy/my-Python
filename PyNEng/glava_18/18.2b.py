'''Скопировать функцию send_config_commands из задания 18.2a и 
добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат 
на такие ошибки:
    • Invalid input detected
    • Incomplete command
    • Ambiguous command
    
Если при выполнении какой-то из команд возникла ошибка, функция 
должна выводить сообщение на стандартный поток вывода с информацией 
о том, какая ошибка возникла, при выполнении какой команды и на каком
устройстве, например: Команда «logging» выполнилась с ошибкой
«Incomplete command.» на устройстве 192.168.100.1 

Ошибки должны выводиться всегда, независимо от значения параметра log. 
При этом, log по-прежнему должен контролировать будет ли выводиться 
сообщение: Подключаюсь к 192.168.100.1…

Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
    • первый словарь с выводом команд, которые выполнились без ошибки
    • второй словарь с выводом команд, которые выполнились с ошибками
    
Оба словаря в формате (примеры словарей ниже):
    • ключ - команда
    • значение - вывод с выполнением команд
Проверить работу функции можно на одном устройстве..'''


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
            return {'status': 'success', 'output': output}
    except NetMikoTimeoutException:
        return {'status': 'error', 'code': 'timeout', 'message': f'Превышено время ожидания соединения {device["host"]}'}
    except NetMikoAuthenticationException:
        return {'status': 'error', 'code': 'auth_error', 'message': f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)'}
    except Exception as e:
        return {'status': 'error', 'code': 'unknown', 'message': f'Не удалось подключиться к {device["host"]}: {e}'}

if __name__ == "__main__":
    try:
        with open("devices_4.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_3.yaml не найден.")
        exit(1)
    
    commands = ['xxx', 'show version', 'yyy']  # Список команд для выполнения

    for device in devices:
        good = {}
        bad = {}
        print(f"Подключение к {device['host']}... ")
        
        for cmd in commands:  # Перебираем команды
            result = send_config_commands(device, cmd)
            if result['status'] == 'success':
                good[cmd] = result['output']
            else:
                bad[cmd] = result['message']
            
        result_tuple = bad, good
        print(result_tuple)
        
        
        

 