'''Создать функцию get_ints_without_description, которая ожидает 
как аргумент имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
    interface Ethernet0/2
     description To P_r9 Ethernet0/2
     ip address 10.0.19.1 255.255.255.0
     mpls traffic-eng tunnels
     ip rsvp bandwidth
     
Интерфейс без описания:
    interface Loopback0
     ip address 10.1.1.1 255.255.255.255
     
Проверить работу функции на примере файла config_r1.txt.'''

import re

def get_ints_without_description(name_config):
    result = []
    with open(name_config, 'r') as file:
        lines = file.readlines()

    i = 0    # номер строки
    while i < len(lines): # пока i не превысил общее колличество строк
        line = lines[i].strip() # берем текущую строку и удаляем робелы и символы перевода строки в начале и конце строки 
        # Ищем начало интерфейса
        if line.startswith('interface '): # начинается ли строка с interface (с пробелом)
            interface_name = re.search(r'^interface (.+)', line).group(1) # .group(1) — возвращает содержимое первой захватывающей группы, то есть имя интерфейса
            has_description = False # описание не найдено
            
            # Сканируем строки до следующего интерфейса или конца файла
            j = i + 1   # проверяем строки после того как нашли интерфейс


            while j < len(lines) and not lines[j].startswith('interface '): # пока не дошли до конца файла И пока следующая строка не начинается с interface
                if lines[j].strip().startswith('description '):
                    has_description = True
                    break
                j += 1
                
            if not has_description:
                result.append(interface_name)
                
            i = j - 1  # корректируем индекс, чтобы не пропустить следующий интерфейс
        i += 1

    return result

interfaces = get_ints_without_description('./config_r1.txt')
print(interfaces)

# ['Loopback0', 'Tunnel0', 'Ethernet0/1', 'Ethernet0/3.100', 'Ethernet1/0']
