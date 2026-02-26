"""
Преобразовать строку в переменной mac из формата XXXX:XXXX:XXXX в формат
XXXX.XXXX.XXXX Полученную новую строку вывести на стандартный поток вывода (stdout) с помощью print.
Ограничение: Все задания надо выполнять используя только пройденные темы.
mac = "AAAA:BBBB:CCCC"

"""

mac = "AAAA:BBBB:CCCC"

new_mac = mac.replace(":", ".")
print(new_mac)