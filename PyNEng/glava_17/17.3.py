'''Создать функцию parse_sh_cdp_neighbors, которая обрабатывает вывод
команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между 
устройствами.

Например, если как аргумент был передан такой вывод:
    R4>show cdp neighbors
    Device ID   Local Intrfce   Holdtme      Capability      Platform    Port ID
    R5          Fa 0/1           122          R S I         2811         Fa 0/1
    R6          Fa 0/2           143          R S I         2811         Fa 0/0

Функция должна вернуть такой словарь:
{"R4": {"Fa 0/1": {"R5": "Fa 0/1"},
"Fa 0/2": {"R6": "Fa 0/0"}}}

Интерфейсы должны быть записаны с пробелом. 
То есть, так Fa 0/0, а не так Fa0/0.
Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt'''

import re
import os

result = {} 

def parse_sh_cdp_neighbors(file_in):
    global result 
    for line in file_in:
        match = re.match(r'(\w+)\s+(\S+\s\S+)\s+\d+\s+\w\s\w\s\w\s+\d+\s+(\S+\s\S+)', line)
        if match:
            device, sport, dport = match.groups()
            dport_dict = {device : dport} # cоздаем словарь с именем соседа и его портом
            sport_dict = {sport : dport_dict} # cоздаем словарь для нашего интерфейса
            result[hostname].update(sport_dict)
    print(result)
            
     
filename = 'sh_cdp_n_sw1.txt'

# Извлекаем hostname из имени файла
hostname = os.path.splitext(os.path.basename(filename))[0].split('_')[-1]

#создаем пустой ключ, далее будем все в него добавлять
result[hostname] = {}

with open(filename) as f:
    output = f.readlines()
    parse_sh_cdp_neighbors(output)
    
   