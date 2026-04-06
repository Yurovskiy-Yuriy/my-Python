'''
Создать функцию send_show_command.
Функция подключается по SSH (с помощью netmiko) к ОДНОМУ 
устройству и выполняет указанную команду.

Параметры функции:
    • device - словарь с параметрами подключения к устройству
    • command - команда, которую надо выполнить
    
Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла 
devices.yaml с помощью функции send_show_command (эта часть кода написана).

import yaml

if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        
    for dev in devices:
        print(send_show_command(dev, command))
'''

from pprint import pprint
import yaml
from netmiko import ConnectHandler

def send_show_command(device_params, commands):
    result = {}
    with ConnectHandler(**device_params) as ssh:
        ssh.enable() # Netmiko по умолчанию сам отключает постраничный вывод (terminal length 0)
        # for cmd in commands:
        output = ssh.send_command(commands)
        result[commands] = output
        
    return result

if __name__ == "__main__":
    command = "sh ip int br"
    
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        
    for dev in devices:
        output = send_show_command(dev, command)
        pprint(output)

    
