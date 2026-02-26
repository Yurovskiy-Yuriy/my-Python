"""
Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24
Затем вывести информацию о сети и маске в таком формате:

Network:
10 	 1 	  1  	   0
00001010 00000001 00000001 00000000

Mask:
/24
255	 255  	  255 	   0
11111111 11111111 11111111 00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: "11111111111111111111111111110000"

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
network = input('Введите сеть в формате 10.10.10.0/24: ')

# Заменяем "." и "/" на ","
network = network.replace('.', ',').replace('/', ',')
network_parts = network.split(",")


# Получаем IP-адрес и маску
ip_address = list(map(int, network_parts[:4]))  # Преобразуем первые четыре части в int
mask_length = int(network_parts[4])  # Пятая часть - это длина маски
print(ip_address)
print(mask_length)

# Создаем двоичную маску
mask_binary = "1" * mask_length + "0" * (32 - mask_length)
print('mask: ', mask_binary)

# Преобразуем двоичную маску в десятичный формат
mask_01 = int(mask_binary[0:8], 2)
mask_02 = int(mask_binary[8:16], 2)
mask_03 = int(mask_binary[16:24], 2)
mask_04 = int(mask_binary[24:32], 2)

print('\n' + '-' * 40)

ip_template = '''
Network:
{0:<11} {1:<11} {2:<11} {3:<11}
{0:<011b} {1:<011b} {2:<011b} {3:<011b}

Mask:
/{4:<11}
{9:<11} {10:<11} {11:<11} {12:<11}
{5:<011} {6:<011} {7:<011} {8:<011}
'''

#выводим шаблон и подставляем в него даные из переменной ip
print(ip_template.format(ip_address[0], ip_address[1], ip_address[2], ip_address[3], mask_length, mask_binary[0:8], mask_binary[8:16], mask_binary[16:24], mask_binary[24:32], mask_01, mask_02, mask_03, mask_04))

