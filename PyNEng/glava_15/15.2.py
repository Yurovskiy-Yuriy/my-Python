'''Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент имя файла, в котором
находится вывод команды show ip int br
Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
• Interface
• IP-Address
• Status
• Protocol
Информация должна возвращаться в виде списка кортежей:
[("FastEthernet0/0", "10.0.1.1", "up", "up"),
("FastEthernet0/1", "10.0.2.1", "up", "up"),
("FastEthernet0/2", "unassigned", "down", "down")]
Для получения такого результата, используйте регулярные выражения.
Проверить работу функции на примере файла sh_ip_int_br.txt.'''

import re

result = []
def parse_sh_ip_int_br(name_config):
    
    with open(name_config, 'r') as file:
        for line in file:
            match = re.match(r'(\w+\d+/\d+|\w+\d+)\s+(\d+.\d+.\d+.\d+|\w+)\s+\w+\s+\w+\s+(up|administratively down)\s+(up|down)', line)
            if match:
                result.append(match.groups())
    print(result)

parse_sh_ip_int_br('./sh_ip_int_br.txt')

# [('FastEthernet0/0', '15.0.15.1', 'up', 'up'), 
#  ('FastEthernet0/1', '10.0.12.1', 'up', 'up'),
#  ('FastEthernet0/2', '10.0.13.1', 'up', 'up'), 
#  ('FastEthernet0/3', 'unassigned', 'administratively down', 'down'),
#  ('Loopback0', '10.1.1.1', 'up', 'up'), 
#  ('Loopback100', '100.0.0.1', 'up', 'up')]