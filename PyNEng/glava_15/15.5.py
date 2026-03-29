'''Создать функцию generate_description_from_cdp, которая ожидает как аргумент имя файла,
в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать на осно-
вании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
    R1>show cdp neighbors
    Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
    S - Switch, H - Host, I - IGMP, r - Repeater
    Device ID    Local Intrfce  Holdtme     Capability   Platform    Port ID
    SW1          Eth 0/0        140         S I W        S-C3750-    Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание description Connected to SW1
port Eth 0/1.

Функция должна возвращать словарь, в котором ключи - имена интерфейсов, а значения -
команда задающая описание интерфейса:
    "Eth 0/0": "description Connected to SW1 port Eth 0/1"

Проверить работу функции на файле sh_cdp_n_sw1.txt.'''

import re

def generate_description_from_cdp(name_config):
    with open(name_config, 'r') as file_in:
        for line in file_in:
            match = re.match(r'(?P<Device>\w+)\s+(?P<sport>\S+\s\S+)\s+\d+\s+(\w\s\w\s\w)\s+\d+\s+(?P<dport>\S+\s\S+)', line)
            if match:
                print(f'"{match.group('sport')}": "description Connected to {match.group('Device')} port {match.group('dport')}"')
    
generate_description_from_cdp('./sh_cdp_n_sw1.txt')

# "Eth 0/1": "description Connected to R1 port Eth 0/0"
# "Eth 0/2": "description Connected to R2 port Eth 0/0"
# "Eth 0/3": "description Connected to R3 port Eth 0/0"
# "Eth 0/5": "description Connected to R6 port Eth 0/1"