"""
Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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
    
    
    mos = CiscoSSH('192.168.10.3', 'admin', 'admin')
   #  print(mos.send_show_command(parse, templates, index))
    mos.send_config_commands(config_commands)
    mos.close()
