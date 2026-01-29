'''Создать функцию generate_trunk_config, которая генерирует конфигурацию для trunk-портов.
У функции должны быть такие параметры:
1. intf_vlan_mapping: ожидает как аргумент словарь с соответствием интерфейс-VLANы та-
кого вида:
{"FastEthernet0/1": [10, 20],
"FastEthernet0/2": [11, 30],
"FastEthernet0/4": [17]}
2. trunk_template: ожидает как аргумент шаблон конфигурации trunk-портов в виде списка
команд (список trunk_mode_template)
Функция должна возвращать список команд с конфигурацией на основе указанных портов
и шаблона trunk_mode_template. В конце строк в списке не должно быть символа перевода
строки.
Проверить работу функции на примере словаря trunk_config и списка команд
trunk_mode_template. Если эта проверка прошла успешно, проверить работу функции
еще раз на словаре trunk_config_2 и убедится, что в итоговом списке правильные номера
интерфейсов и вланов.
Пример итогового списка (перевод строки после каждого элемента сделан для удобства чте-
ния):
[
"interface FastEthernet0/1",
"switchport mode trunk",
"switchport trunk native vlan 999",
"switchport trunk allowed vlan 10,20,30",
"interface FastEthernet0/2",
"switchport mode trunk",
"switchport trunk native vlan 999",
"switchport trunk allowed vlan 11,30",
...]
Ограничение: Все задания надо выполнять используя только пройденные темы.
trunk_mode_template = [
"switchport mode trunk", "switchport trunk native vlan 999",
"switchport trunk allowed vlan"
]
trunk_config = {
"FastEthernet0/1": [10, 20, 30],
"FastEthernet0/2": [11, 30],
"FastEthernet0/4": [17]
}'''

intf_vlan_mapping = {"FastEthernet0/1": [10, 20, 30],
                     "FastEthernet0/2": [11, 30],
                     "FastEthernet0/4": [17]
                     }

trunk_mode_template = ["switchport mode trunk",
                       "switchport trunk native vlan 999",
                       "switchport trunk allowed vlan"
                       ]

def generate_trunk_config(intf_vlan_mapping, trunk_template):
    result = []
    for port, vl in intf_vlan_mapping.items():
        result.append('interface FastEthernet' + port[-3:])
        for x in trunk_template:
            if 'allowed vlan' in x:
                x += ' '
                for z in vl:
                    x += str(z) + ','
                result.append(x)
            else:
                result.append(x)               
    return result

print(generate_trunk_config(intf_vlan_mapping, trunk_mode_template))

for x in generate_trunk_config(intf_vlan_mapping, trunk_mode_template):
    print(x)
