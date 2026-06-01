"""
Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""

import re

class IPAddress:
    def __init__(self, ip_address):
       
        # Проверяем формат и извлекаем адрес и маску
        match = re.fullmatch(r'(\d+\.\d+\.\d+\.\d+)/(\d+)', ip_address)
        if not match:
            raise ValueError('Incorrect IPv4 address')
        
        ip_str, mask_str = match.groups()
        
        # Проверка и преобразование маски
        mask = int(mask_str)
        if not (8 <= mask <= 32):
            raise ValueError('Incorrect mask')
        self.mask = mask
        
        # Проверка и сохранение IP-адреса
        octets = ip_str.split('.')
        if len(octets) != 4:
            raise ValueError('Incorrect IPv4 address')
        
        for octet in octets:
            if not octet.isdigit():
                raise ValueError('Incorrect IPv4 address')
            num = int(octet)
            if not (0 <= num <= 255):
                raise ValueError('Incorrect IPv4 address')
        
        self.ip = ip_str
        
    def __str__(self):
        return f'IP address {self.ip}/{self.mask}'

    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"


try:
    ip1 = IPAddress('10.1.1.1/24')
    # print(ip1.ip)   # 10.1.1.1
    # print(ip1.mask) # 24
    
    print(str(ip1))      # IP address 10.1.1.1/24
    print(ip1)           # IP address 10.1.1.1/24
    print(repr(ip1))     # IPAddress('10.1.1.1/24')
    
    ip_list = [ip1]
    print(ip_list)       # [IPAddress('10.1.1.1/24')]
    
except ValueError as e:
    print(e)
