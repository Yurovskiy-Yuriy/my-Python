'''
Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режи-
ма, задавались разные вопросы в запросе о номере VLANа или списка VLANов:
• для access: «Введите номер VLAN:»
• для trunk: «Введите разрешенные VLANы:»
Ограничение: Все задания надо выполнять используя только пройденные темы. То есть эту
задачу можно решить без использования условия if и циклов for/while

access_template = [
"switchport mode access", "switchport access vlan {}",
"switchport nonegotiate", "spanning-tree portfast",
"spanning-tree bpduguard enable"
]
trunk_template = [
"switchport trunk encapsulation dot1q", "switchport mode trunk",
"switchport trunk allowed vlan {}"
]

'''

mode = input('Введите режим работы интерфейса (access/trunk): ')
interface = input('Введите тип и номер интерфейса: ')
vlan = input('Введите номер влан(ов): ')

switchport_access = 'switchport access vlan ' + vlan
switchport_trunk = 'switchport trunk allowed vlan ' + vlan

template = {
    "access": [
        "switchport mode access", switchport_access,
        "switchport nonegotiate", "spanning-tree portfast",
        "spanning-tree bpduguard enable"
    ],
    "trunk": [
"switchport trunk encapsulation dot1q", "switchport mode trunk",
switchport_trunk, "", ""
    ]
}

ip_template = '''
interface {0}
{1}
{2}
{3}
{4}
{5}
'''

print(ip_template.format(interface, template[mode][0], template[mode][1], template[mode][2],
                         template[mode][3], template[mode][4]))
