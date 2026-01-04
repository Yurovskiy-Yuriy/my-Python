"""
Используя подготовленную строку nat, получить новую строку, в которой в имени интерфей-
са вместо FastEthernet написано GigabitEthernet. Полученную новую строку вывести на стан-
дартный поток вывода (stdout) с помощью print.
Ограничение: Все задания надо выполнять используя только пройденные темы.
nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"

"""

nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"
nat2 = nat.replace('Fast', 'Gigabit')

print(nat2)