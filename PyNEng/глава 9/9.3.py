'''Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл 
коммутатора и возвращает кортеж из двух словарей:

1. словарь портов в режиме access, где ключи номера портов, а значения access VLAN (числа):
{"FastEthernet0/12": 10,
"FastEthernet0/14": 11,
"FastEthernet0/16": 17}

2. словарь портов в режиме trunk, где ключи номера портов, а значения список разрешен-
ных VLAN (список чисел):
{"FastEthernet0/1": [10, 20],
"FastEthernet0/2": [11, 30],
"FastEthernet0/4": [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя
конфигурационного файла.
Проверить работу функции на примере файла config_sw1.txt
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):   
    with open(config_filename, 'r') as file:
        lines = file.readlines()
        cleaned_lines = [line.strip() for line in lines] # убираем \n
    
    result_access = {}
    result_trunk = {}
    result = ()
    for x in cleaned_lines:
        if 'FastEthernet' in x:
            port = x[-15:]   # FastEthernet0/0
        if 'access vlan' in x:
            access = int(x[-2:])  #30
            result_access[port] = access
        elif 'trunk allowed vlan' in x:
            list_trank = x[30:]   #'100,300,400,500,600'
            list_trank = list(map(int, list_trank.split(',')))   # [100, 300, 400, 500, 600]
            result_trunk[port] = list_trank
    result = (result_access, result_trunk) # кортеж
    return result

print(get_int_vlan_map('d:/test/config_sw1.txt'))
