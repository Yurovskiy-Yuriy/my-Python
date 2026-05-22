
"""
Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""

from netmiko import ConnectHandler
from pprint import pprint
import textfsm
import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor, as_completed



class CiscoSSH:
    def __init__(self, ip, username, password, secret=None):
        # 1. Формируем словарь с параметрами подключения для Netmiko
        device_params = {
            "device_type": "linux", 
            "ip": ip,
            "username": username,
            "password": password,
            "secret": secret, # Пароль для enable
        }

        # 2. открываем соединение и переходим в enable
        self.ssh = ConnectHandler(**device_params)
        self.ssh.enable() 
    
    
    # отправляем команду show
    def send_show_command(self, parse, templates, index,):
       
         # ввод команды
         print('1. show cdp neighbors detail\n2. show clock\n3. show ip interface brief\n4. show ip route ospf\n5. show version')
         dic_command = {1:'show cdp neighbors detail', 2:'show clock', 3:'show ip interface brief', 4:'show ip route ospf', 5:'show version',}
         print()
         number_command = int(input('Введите номер команды: '))

         while  number_command > 5 or number_command <= 0 :
            number_command = int(input('Неправильная команда, повотрите: '))
         command = dic_command[number_command]
        
         # получаем нужный шаблон .template в зависимости от команды
         with open((templates + index), 'r') as file:
               output = file.readlines()
               for out in output:
                  out_split = out.split(',')
                  if command in out_split[3]:
                     file_templates = out_split[0]     # sh_cdp_n_det.template
         
         # отправдяем команду
         output = self.ssh.send_command(command)
         if parse == False:
               output = self.ssh.send_command(command)
               return output
         else:
               #парсим вывод команды
               # 1. Загружаем шаблон
               with open(templates + file_templates) as f:
                  re_table = textfsm.TextFSM(f)

               # 2. Парсим текст с помощью шаблона
               structured_data = re_table.ParseText(output)
               
               # 3. Формируем список словарей
               result = []

               for item in structured_data:
                  row = dict(zip(re_table.header, item)) # Создаём словарь
                  result.append(row)
                  
               return result
         
         
    # функция для списка команд config
    def send_config_commands(self, config_commands):


         self.ssh.send_command('configure terminal', expect_string=r'#')
         
         # 2. Отправляем список команд конфигурации
         # Используем send_config_set, так как это список команд
         output = self.ssh.send_config_set(config_commands, exit_config_mode=False)
         
         # 3. Выходим из режима конфигурирования
         self. ssh.send_command('exit', expect_string=r'#')
         
         return output

      
    # закрываем соединение
    def close(self):
        self.ssh.disconnect()
        
        
     
                
if __name__ == '__main__':
    
    # parse = False
    parse = True
    templates = '22.2a/templates/'    # путь к каталогу с шаблонами.
    index = 'index'                   # имя файла, где хранится соответствие между командами и шаблонами.
    
    config_commands = ('interface ethernet 9', 'description TEST_TEST_TEST', 'ip address 192.168.55.1/24')
    
    
    mos = CiscoSSH('192.168.10.10', 'admin', 'admin')
   #  print(mos.send_show_command(parse, templates, index))
    mos.send_config_commands(config_commands)
    mos.close()
