'''Сделать копию функции get_int_vlan_map из задания 9.3.
Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта вы-
глядит так:
interface FastEthernet0/20
switchport mode access
duplex auto
То есть, порт находится в VLAN 1
В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
{"FastEthernet0/12": 10,
"FastEthernet0/14": 11,
"FastEthernet0/20": 1}
У функции должен быть один параметр config_filename, который ожидает как аргумент имя
конфигурационного файла.
Проверить работу функции на примере файла config_sw2.txt
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
        
        if 'mode access' in x:
            result_access[port] = 'switchport mode access'

        if 'access vlan' in x:
            access = int(x[-2:])  #30
            result_access[port] = access   # перезаписывает 'mode access' на 30
        elif 'trunk allowed vlan' in x:
            list_trank = x[30:]   #'100,300,400,500,600'
            list_trank = list(map(int, list_trank.split(',')))   # [100, 300, 400, 500, 600]
            result_trunk[port] = list_trank
    result = (result_access, result_trunk) # кортеж
    return result

print(get_int_vlan_map('d:/test/config_sw2.txt'))
