"""
В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также должна выполняться проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать
исключение ValueError с соответствующим текстом (вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра:
ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

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



try:
    ip1 = IPAddress('10.1.1.1/24')
    print(ip1.ip)   # 10.1.1.1
    print(ip1.mask) # 24
except ValueError as e:
    print(e)
