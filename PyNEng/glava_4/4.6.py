"""
Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:

Prefix 10.0.24.0/24
AD/Metric 110/41
Next-Hop 10.0.13.3
Last update 3d18h
Outbound Interface FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.
ospf_route = " 10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
"""

ospf_route = " 10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"



ospf_route = ospf_route.replace('[', '').replace(']', '').replace(',', '')  #удвляем лишние значения
print(ospf_route)
print('')

ospf_route = ospf_route.split()
print(ospf_route)
print(ospf_route[1])
print('')

#создаем словарь
ospf_route = {
	'Prefix': ospf_route[0],
	'AD/Metric': ospf_route[1],
	'Next-Hop': ospf_route[2],
	'Last update': ospf_route[3],
	'Outbound Interface': ospf_route[4],
}

for key, value in ospf_route.items():
    print(f"{key}: {value}")





