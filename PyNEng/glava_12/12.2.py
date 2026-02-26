'''
Функция ping_ip_addresses из задания 12.1 принимает только список адресов, но бы-
ло бы удобно иметь возможность указывать адреса с помощью диапазона, например,
192.168.100.1-10.
В этом задании необходимо создать функцию convert_ranges_to_ip_list, которая конвертирует
список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.
Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.
Элементы списка могут быть в формате:
• 10.1.1.1
• 10.1.1.1-10.1.1.10
• 10.1.1.1-10
Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая
последний адрес диапазона. Для упрощения задачи, можно считать, что в диапазоне всегда
меняется только последний октет адреса.

Функция возвращает список IP-адресов.
Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
'172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']
'''
import subprocess
import re

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

# r'^(\S+)\s+(\w+\s\S+)\s+\d+\s+(\w\s\w)\s+(\S+)\s*(?:\w+\s\S+)$'

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

            
ip_list = ['8.8.8.8', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
list_ping = convert_ranges_to_ip_list(ip_list) # ['8.8.8.8', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128', '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

result_tuple = ping_ip_addresses(list_ping)

print("Доступные IP:", result_tuple[0])
print("Недоступные IP:", result_tuple[1])

