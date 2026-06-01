"""
Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""
from netmiko import ConnectHandler

class CiscoSSH:
    def __init__(self, ip, username, password, secret=None):
        # 1. Формируем словарь с параметрами подключения для Netmiko
        device_params = {
            "device_type": "cisco_ios", 
            "ip": ip,
            "username": username,
            "password": password,
            "secret": secret, # Пароль для enable
        }

        # 2. открываем соединение и переходим в enable
        self.ssh = ConnectHandler(**device_params)
        self.ssh.enable() 
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
        
    
    # отправляем команду
    def send_show_command(self, command):
        output = self.ssh.send_command(command)
        return output
      
    # закрываем соединение
    def close(self):
        self.ssh.disconnect()
        
# mos = CiscoSSH('10.161.6.6', 'root', 'qwerty12')
# print(mos.send_show_command('show configuration'))
# mos.close()


r1_params = {
    'ip': '10.161.6.6',
    'username': 'root',
    'password': 'qwerty12',
    'secret': 'cisco'
}

# Теперь соединение закроется автоматически после выхода из блока with
with CiscoSSH(**r1_params) as r1:
    print(r1.send_show_command('sh clock'))

# На этой строке соединение уже гарантированно закрыто.