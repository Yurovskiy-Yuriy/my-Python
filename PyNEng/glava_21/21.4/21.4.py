"""
Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

import textfsm
import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


'''************парсим вывод команды*****************'''
def parse_command_dynamic(template, command_output):

    # 1. Загружаем шаблон
    with open(template) as f:
        re_table = textfsm.TextFSM(f)

    # 2. Парсим текст с помощью шаблона
    structured_data = re_table.ParseText(command_output)
    
    # 3. Формируем список словарей
    result = []

    for item in structured_data:
        row = dict(zip(re_table.header, item)) # Создаём словарь

        result.append(row)
    
    return result

"**********отправляем команды на маршрутизатор**************"
def send_command_to_device(device, command):
    # Создаем словарь для подключения, совместимый с Netmiko
    netmiko_device = {
        'device_type': 'linux',  # Dionis NX — Linux-based устройство
        'host': device['host'],
        'username': device['username'],
        'password': device['password'],
        'timeout': device.get('timeout', 10),
    }

    try:
        # Устанавливаем соединение с устройством
        with ConnectHandler(**netmiko_device) as ssh:
            # Отправляем команду и получаем вывод
            output = ssh.send_command(command)
            return output
    except NetMikoTimeoutException:
        print(f'Превышено время ожидания соединения {device["host"]}')
    except NetMikoAuthenticationException:
        print(f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)')
    except Exception as e:
        print(f'Не удалось подключиться к {device["host"]}: {e}')
    return None


"**********подключение к маршрутизатору**************"
def connect_to_device(command, file_yaml, tracer):
    
    try:
        with open(file_yaml) as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Файл {file_yaml} не найден.")
        exit(1)

    for device in devices:
        results = []
        print(f"Подключение к {device['host']}... ")
        
        # for cmd in commands:  # Перебираем команды
        #     print(cmd)
        result = send_command_to_device(device, command) 
        if result is not None:
            results.append(f"=== Команда: {command} ===")
            results.append(result)
            results.append('')
        
        # Заголовок добавляем один раз, если есть хоть какой-то результат
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
            
        # Сохранение каждого устройства в отдельный файл
        filename = f"{tracer}log_{device['host']}.txt"
        print(f'Сохранение конфигурации в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e:  # Если запись в файл не удалась (например, нет прав), выводим в консоль
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')
        
        return result
    
    

if __name__ == "__main__":
    
    # получаем необходимую команду
    print('1. show cdp neighbors detail\n2. show clock\n3. show ip interface brief\n4. show ip route ospf\n5. show version')
    dic_command = {1:'show cdp neighbors detail', 2:'show clock', 3:'show ip interface brief', 4:'show ip route ospf', 5:'show version',}
    print()
    number_command = int(input('Введите номер команды: '))
    
    while  number_command > 5 or number_command <= 0 :
        number_command = int(input('Неправильная команда, повотрите: '))
    command = dic_command[number_command]
    
    # получаем нужный шаблон .template в зависимости от команды
    with open('21.4/templates/index', 'r') as file:
        output = file.readlines()
        for out in output:
            out_split = out.split(',')
            if command in out_split[3]:
                file_templates = out_split[0]     # sh_cdp_n_det.template

    # подключаемся к устройсву, отправляем команду и получаем результат
    tracer = "21.4/log/"
    file_yaml = "21.4/log/devices_cisco.yaml"
    
    output = connect_to_device(command, file_yaml, tracer)
  
    
    # file_output = file_templates.replace('template', 'txt')  # sh_cdp_n_det.txt
    # with open(f'21.3/output/{file_output}', 'r') as file:
    #     output = file.read() # Читаем весь файл как одну строку
       
    result = parse_command_dynamic(f'21.4/templates/{file_templates}', output)
    
    print()
    print('Результат: ')
    for row in result:
        print(row)
        
        
# 1. show cdp neighbors detail
# 2. show clock
# 3. show ip interface brief
# 4. show ip route ospf
# 5. show version

# Введите номер команды: 2
# Подключение к 192.168.1.10... 
# Сохранение конфигурации в файл "21.4/log/log_192.168.1.10.txt"...

# Результат: 
# {'time': '13:39:17', 'timezone': 'UTC', 'weekday': 'Tue', 'month': 'May', 'monthday': '19', 'year': '2025'}