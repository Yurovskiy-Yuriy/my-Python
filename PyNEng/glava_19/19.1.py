"""
Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""


import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def ping_device(ip):
    # Пингует один IP-адрес.
    reply = subprocess.run(["ping", "-n", "1", ip], 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # returncode == 0 означает, что команда выполнена успешно
    return (ip, reply.returncode == 0)
    

def ping_ip_addresses(ip_list, limit=3):
    
    reachable = []  # Список доступных IP
    unreachable = [] # Список недоступных IP
    
    with ThreadPoolExecutor(max_workers=limit) as executor:
        # Запускаем функцию ping_device для каждого IP в отдельном потоке
        future_list = [executor.submit(ping_device, ip) for ip in ip_list]
    
        # Обрабатываем результаты по мере их поступления
        for future in as_completed(future_list):
            ip, is_reachable = future.result()
            if is_reachable:
                reachable.append(ip)
            else:
                unreachable.append(ip)

    # Возвращаем результат в виде кортежа из двух списков
    return (reachable, unreachable)

if __name__ == "__main__":        
    ip_list = [f'8.8.8.{i}' for i in range(1, 41)]
    
    result = ping_ip_addresses(ip_list, limit=20)
    
    print(result)