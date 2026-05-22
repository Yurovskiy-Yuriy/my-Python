"""
Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""
# Задание выполнено используя netmiko, подключение идет по ssh

from netmiko import ConnectHandler
import textfsm
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor, as_completed


# ввод команды
def input_comand():
# получаем необходимую команду
    print('1. show cdp neighbors detail\n2. show clock\n3. show ip interface brief\n4. show ip route ospf\n5. show version')
    dic_command = {1:'show cdp neighbors detail', 2:'show clock', 3:'show ip interface brief', 4:'show ip route ospf', 5:'show version',}
    print()
    number_command = int(input('Введите номер команды: '))
    
    while  number_command > 5 or number_command <= 0 :
        number_command = int(input('Неправильная команда, повотрите: '))
    command = dic_command[number_command]
    
    return command


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
    
    
    
    
    # отправляем команду
    def send_show_command(self, command, parse, templates, index,):
        
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
      
      
    # закрываем соединение
    def close(self):
        self.ssh.disconnect()
        
    
         
                
if __name__ == '__main__':
    
    command = input_comand()
    # parse = False
    parse = True
    templates = '22.2a/templates/'    # путь к каталогу с шаблонами.
    index = 'index'                   # имя файла, где хранится соответствие между командами и шаблонами.
    
    mos = CiscoSSH('192.168.1.10', 'admin', 'admin')
    print(mos.send_show_command(command, parse, templates, index))
    mos.close()