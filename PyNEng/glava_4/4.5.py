"""
Из строк command1 и command2 получить список VLANов, которые есть и в команде
command1 и в команде command2 (пересечение).
В данном случае, результатом должен быть такой список: ['1', '3', '8']
Записать итоговый список в переменную result. (именно эта переменная будет проверяться
в тесте)
Полученный список result вывести на стандартный поток вывода (stdout) с помощью print.
Ограничение: Все задания надо выполнять используя только пройденные темы.

command1 = "switchport trunk allowed vlan 1,2,3,5,8"
command2 = "switchport trunk allowed vlan 1,3,8,9"

"""

command1 = "switchport trunk allowed vlan 1,2,3,5,8"  
command2 = "switchport trunk allowed vlan 1,3,8,9"

commands1 = command1.split()  #разделяется в список строк по пробельным символам

commands2 = command2.split()

vlans1 = commands1[-1].split(',') #остается только последний эллемент в списке
vlans2 = commands2[-1].split(',')

print(vlans1)
print(vlans2)

vlans1 = set(vlans1)
vlans2 = set(vlans2)

vlans3 = vlans1 & vlans2
vlans3 = sorted(vlans3)
print(vlans3)



"""
Вот как скрипт написал ИИ:
# Извлекаем VLANы из каждой строки после ключевого слова 'vlan'
vlan_list1 = command1.split()[-1].split(",")
vlan_list2 = command2.split()[-1].split(",")

# Получаем пересечение списков, сортируем по числовому значению
result = sorted(list(set(vlan_list1) & set(vlan_list2)), key=int)
"""