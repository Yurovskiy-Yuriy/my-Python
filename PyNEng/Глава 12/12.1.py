'''
    Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса. Функция
ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
    • список доступных IP-адресов
    • список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
import subprocess

def ping_ip_addresses(ip_list):
    available = []
    unavailable = []
    
    for ip in ip_list:
        result = subprocess.run(["ping", "/n", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
           available.append(ip)
        else:
            unavailable.append(ip)
    
    return tuple([available, unavailable])
            
list_ping = ['8.8.8.8', 'ya.ru', '4.2.1.3']
result_tuple = ping_ip_addresses(list_ping)

print("Доступные IP:", result_tuple[0])
print("Недоступные IP:", result_tuple[1])

