'''Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.
Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
ip address 10.255.2.2 255.255.255.0
ip address 10.254.2.2 255.255.255.0 secondary

    А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1 
соответствует только один из них (второй).
    Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом,
чтобы она возвращала список кортежей для каждого интерфейса. Если на интерфейсе назначен
только один адрес, в списке будет один кортеж. Если же на интерфейсе настроены несколько
IP-адресов, то в списке будет несколько кортежей.
    Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу Ethernet0/1
соответствует список из двух кортежей.
Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса, диа-
'''

import re

result = {}
def get_ip_from_cfg(name_config):
    
    with open(name_config, 'r') as file:
        for line in file:
            match_int = re.match(r'^interface (?P<int>.+)', line)
            match_ip = re.match(r'^\s+ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)(?:\s+secondary)?$', line)

            if match_int:
                int = match_int.group('int')
                
            if match_ip:
                if int in result:
                    result[int].append(match_ip.groups())
                else:
                    result[int] = [match_ip.groups()]

    print(result)

get_ip_from_cfg('./config_r2.txt')

# {'Loopback0': [('10.2.2.2', '255.255.255.255')], 
#  'Ethernet0/0': [('10.0.23.2', '255.255.255.0')], 
#  'Ethernet0/1': [('10.255.2.2', '255.255.255.0'), ('10.254.2.2', '255.255.255.0')], 
#  'Ethernet0/2': [('10.0.29.2', '255.255.255.0')]}