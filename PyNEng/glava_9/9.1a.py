'''Сделать копию функции generate_access_config из задания 9.1.
Дополнить скрипт: ввести дополнительный параметр, который контролирует будет ли 
настроен port-security:
• имя параметра «psecurity»
• по умолчанию значение None
• для настройки port-security, как значение надо передать список команд port-security (на-
ходятся в списке port_security_template)

    Функция должна возвращать список всех портов в режиме access с конфигурацией на осно-
ве шаблона access_mode_template и шаблона port_security_template, если он был передан. В
конце строк в списке не должно быть символа перевода строки.

    Проверить работу функции на примере словаря access_config, с генерацией конфигурации
port-security и без.

Пример вызова функции:
print(generate_access_config(access_config, access_mode_template))
print(generate_access_config(access_config, access_mode_template, port_security_template))

Ограничение: Все задания надо выполнять используя только пройденные темы.

access_mode_template = [
"switchport mode access", "switchport access vlan",
"switchport nonegotiate", "spanning-tree portfast",
"spanning-tree bpduguard enable"
]
port_security_template = [
"switchport port-security maximum 2",
"switchport port-security violation restrict",
"switchport port-security"
]
access_config = {"FastEthernet0/12": 10, "FastEthernet0/14": 11, "FastEthernet0/16": 17}
'''


access_config = {
    "FastEthernet0/12": 10,
    "FastEthernet0/14": 11,
    "FastEthernet0/16": 17
    }

port_security_template = [
    "switchport port-security maximum 2",
    "switchport port-security violation restrict",
    "switchport port-security"
    ]

access_mode_template = [
    "switchport mode access", "switchport access vlan",
    "switchport nonegotiate", "spanning-tree portfast",
    "spanning-tree bpduguard enable"
    ]

result = []
def generate_access_config(intf_vlan_mapping, access_template, port_security=None):
        for port, vl in intf_vlan_mapping.items():
            result.append('interface FastEthernet' + port[-4:])
            for x in access_template:
                if 'vlan' in x:
                    x += ' ' + str(vl)
                    result.append(x)
                else:
                    result.append(x) 
            if port_security != None:
                for y in port_security:
                    result.append(y)                
        return result
        
print(generate_access_config(access_config, access_mode_template))
print()
print(generate_access_config(access_config, access_mode_template, port_security_template))

'''РЕЗУЛЬТАТ:
['interface FastEthernet0/12', 'switchport mode access', 'switchport access vlan 10', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable', 
'interface FastEthernet0/14', 'switchport mode access', 'switchport access vlan 11', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable',
'interface FastEthernet0/16', 'switchport mode access', 'switchport access vlan 17', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable']

['interface FastEthernet0/12', 'switchport mode access', 'switchport access vlan 10', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable',
'interface FastEthernet0/14', 'switchport mode access', 'switchport access vlan 11', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable', 
'interface FastEthernet0/16', 'switchport mode access', 'switchport access vlan 17',
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable', 
'interface FastEthernet0/12', 'switchport mode access', 'switchport access vlan 10', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable', 
'switchport port-security maximum 2', 'switchport port-security violation restrict', 
'switchport port-security', 'interface FastEthernet0/14', 'switchport mode access', 
'switchport access vlan 11', 'switchport nonegotiate', 'spanning-tree portfast', 
'spanning-tree bpduguard enable', 'switchport port-security maximum 2', 
'switchport port-security violation restrict', 'switchport port-security', 
'interface FastEthernet0/16', 'switchport mode access', 'switchport access vlan 17', 
'switchport nonegotiate', 'spanning-tree portfast', 'spanning-tree bpduguard enable',
'switchport port-security maximum 2', 'switchport port-security violation restrict',
'switchport port-security']     
PS C:\Users\user> '''