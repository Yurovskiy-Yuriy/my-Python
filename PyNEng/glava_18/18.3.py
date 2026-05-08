'''Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
    • device - словарь с параметрами подключения к одному устройству
    • show - одна команда show (строка)
    • config - список с командами, которые надо выполнить в конфигурационном режиме
    
Аргументы show и config должны передаваться только как ключевые. При передачи этих ар-
гументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands(r1, 'sh clock')
---------------------------------------------------------------------------
TypeError                                   Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands(r1, 'sh clock')

TypeError: send_commands() takes 1 positional argument but 2 were given


В зависимости от того, какой аргумент был передан, функция вызывает разные функции
внутри. При вызове функции send_commands, всегда должен передаваться только один из
аргументов show, config. Если передаются оба аргумента, должно генерироваться исключе-
ние ValueError.

Далее комбинация из аргумента и соответствующей функции:
    • show - функция send_show_command из задания 18.1
    • config - функция send_config_commands из задания 18.2
    
Функция возвращает строку с результатами выполнения команд или команды.
Проверить работу функции:
    • со списком команд commands
    • командой command
    
Пример работы функции:
In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: commands = ['username user5 password pass5', 'username user6 password pass6']

In [16]: send_commands(r1, config=commands)
Out[16]: 'config term\nEnter configuration commands, one per line. End with CNTL/Z.\
,→nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\
,→nR1(config)#end\nR1#'


commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
command = "sh ip int br"
'''


# скрипт написан для DionisNX

from pprint import pprint
import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import time

# функция для команды show
def send_show_command(device_params, command):
        
    try:
        with ConnectHandler(**device_params) as ssh:
            output = ssh.send_command(command)
            return output
    except (NetMikoTimeoutException, NetMikoAuthenticationException, Exception) as e:
        print(f"Ошибка подключения к {device_params['host']}: {e}")
        return None

# функция для списка команд 
def send_config_commands(device_params, config_commands):

    # device_params = device.copy()
    # Устанавливаем правильный тип устройства
    dionis_device = device.copy()
    dionis_device['device_type'] = 'linux'
    # Увеличиваем таймаут, так как вход в режим конфигурирования может быть долгим
    dionis_device['global_delay_factor'] = 2 

    try:
        with ConnectHandler(**dionis_device) as ssh:
            # 1. Входим в режим конфигурирования
            # Используем expect_string, чтобы Netmiko знало, когда есть "#" значит команда выполнена
            ssh.send_command('configure terminal', expect_string=r'#')
            
            # 2. Отправляем список команд конфигурации
            # Используем send_config_set, так как это список команд
            output = ssh.send_config_set(config_commands, exit_config_mode=False)
            
            # 3. Выходим из режима конфигурирования
            ssh.send_command('exit', expect_string=r'#')
            
            return output
            
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"Ошибка подключения к {device_params['host']}: {e}")
        return None
    except Exception as e:
        # Отлавливаем ошибку с "Pattern not detected"
        print(f"Неожиданная ошибка на {device_params['host']}: {e}")
        return None


# функция-обертка 
def send_commands(device, *, show=None, config=None):
    
    # Проверка: передан ровно один из аргументов
    if show and config:
        raise ValueError("Оба аргумента переданы. Нужно передавать только один: show или config.")
    
    if not show and not config:
        raise ValueError("Не передан ни один из аргументов. Нужно передать show или config.")

    # Логика выбора действия
    if show:
        print(device['host'], show)
        # Вызываем функцию для команды show
        return send_show_command(device, show)
    
    if config:
        # Вызываем функцию для списка команд конфигурации
        return send_config_commands(device, config)


if __name__ == "__main__":

    try:
        with open("devices_4.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_4.yaml не найден.")
        exit(1)
        
    # commands = ('interface ethernet 2')
    commands = ('interface ethernet 2', 'description PRIMER', 'ip address 192.168.55.1/24')
    show_comand = ['show version']
  

    # Проверяем работу на первом устройстве из списка
    for device in devices:
        
        result = send_commands(device, show='show version')
        print("\nРезультат выполнения команды show:")
        pprint(result)
        
        print("\nРезультат выполнения команды config:")
        result_config = send_commands(device, config=commands)
        
        if result_config is not None:
            pprint(result_config)

        
        
