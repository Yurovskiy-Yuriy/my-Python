'''
Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-
адресов.
Функция ожидает как аргументы два списка:
• список доступных IP-адресов
• список недоступных IP-адресов
Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable   Unreachable
----------- -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9 
'''
import subprocess
import re
from tabulate import tabulate

def ping_ip_addresses(ip_list):
    available = []
    unavailable = []
    
    for ip in ip_list:
        result = subprocess.run(["ping", "/n", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'ping {ip}...')
        if result.returncode == 0:
           available.append(ip)
        else:
            unavailable.append(ip)

    return tuple([available, unavailable])

def convert_ranges_to_ip_list(ip_list):
    list_ping = []
    ip_1 = r'\d+.\d+.\d+.\d+$'
    ip_2 = r'(\d+.\d+.\d+.)(\d+)-(\d+)$'
    ip_3 = r'(\d+.\d+.\d+.)(\d+)-\d+.\d+.\d+.(\d+)$'

    for ip in ip_list:
        match = re.match(ip_1, ip)
        match_2 = re.match(ip_2, ip)
        match_3 = re.match(ip_3, ip)
        if match:
            list_ping.append(ip)
        if match_2 :
            prefix, start, finish = match_2.groups()  # присваиваем значение каждой
            for n in range(int(start), int(finish) + 1):
                list_ping.append(f'{prefix}{n}')
        if match_3:
            prefix, start, finish = match_3.groups()  # присваиваем значение каждой
            for n in range(int(start), int(finish) + 1):
                list_ping.append(f'{prefix}{n}')   
    return list_ping

def print_ip_table(Reachable, Unreachable):
    result = []
    colums = [Reachable, Unreachable]
    max_len = max(len(colums[0]), len(colums[1]))
    min_len = min(len(colums[0]), len(colums[1]))

    for i in range(max_len): # перебираем числа (позиции)
        if i < min_len:   # пока позиция не превысила максимальную позицию минимального списка
            val1 = colums[0][i]  # присваиваем каждому значению, соответсвующие значения в списках
            val2 = colums[1][i]
        else:   #  если число (позиция) превысила максимальную позицию минимального списка
            if len(colums[0]) > len(colums[1]): # определяем минимальный список
                val1 = colums[0][i]
                val2 = ''            # добавляем новое пустое значение в минимальный список
            else:
                val1 = ''
                val2 = colums[1][i]
                
        result.append([val1, val2])
    colums_name = ['Reachable', 'Unreachable']
    print(tabulate(result, headers=colums_name))
                
ip_list = ['8.8.8.8', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
list_ping = convert_ranges_to_ip_list(ip_list) # ['8.8.8.8', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128', '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

result_tuple = ping_ip_addresses(list_ping)
print()
print(print_ip_table(result_tuple[0], result_tuple[1]))

