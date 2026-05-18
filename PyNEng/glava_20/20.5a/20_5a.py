"""
Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

# Задание изменено: - мы настраваем не тунели между устройствами, 
# а настраиваем порты на маршрутизаторами для их связанности 


import yaml
import re
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from jinja2 import Environment, FileSystemLoader

# функция для команды show
def send_show_command(device_params, command):
    
    print(f'выполнение команды: "{command}"...')
    
    try:
        with ConnectHandler(**device_params) as ssh:
            output = ssh.send_command(command)
            return output
    except (NetMikoTimeoutException, NetMikoAuthenticationException, Exception) as e:
        print(f"Ошибка подключения к {device_params['host']}: {e}")
        return None

# функция для отправки конфигурационных команд на маршрутизатор
def send_config_commands(device_params, config_commands):

    # Создаем копию, чтобы не менять исходный словарь
    dionis_device = device_params.copy()
    
    # Устанавливаем правильный тип устройства
    dionis_device['device_type'] = 'linux'
    # Увеличиваем таймаут, так как вход в режим конфигурирования может быть долгим
    dionis_device['global_delay_factor'] = 2 
    
    print()
    print(f'Подключение к {dionis_device['host']}...')
    print(f'Отправка коданд: {config_commands}...')
    try:
        with ConnectHandler(**dionis_device) as ssh:
            # 1. Входим в режим конфигурирования
            # Используем expect_string, чтобы Netmiko знало, когда есть "#" значит команда выполнена
            ssh.send_command('configure terminal', expect_string=r'#')
            
            # 2. Отправляем список команд конфигурации
            # Используем send_config_set, так как это список команд
            output = ssh.send_config_set(config_commands, exit_config_mode=False)
            
            # 3. Выходим из режима конфигурирования
            ssh.send_command('exit', expect_string=r'#')
            
            return output
            
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"Ошибка подключения к {device_params['host']}: {e}")
        return None
    except Exception as e:
        # Отлавливаем ошибку с "Pattern not detected"
        print(f"Неожиданная ошибка на {device_params['host']}: {e}")
        return None



# используем шаблон Jinja2 для получения команд и отправляем команды
def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    
    # Указываем, что шаблоны лежат в папке '.'
    env = Environment(loader=FileSystemLoader("."))
    
    # Загружаем шаблон из файла template внутри папки '.'
    templ_1 = env.get_template(src_template)  
    templ_2 = env.get_template(dst_template) 
    
    #  получаем сплошной текст из готовых команд
    result_1 = templ_1.render(vpn_data_dict)
    result_2 = templ_2.render(vpn_data_dict)
    
    # из сплошного текста, получаем список команд
    src_commands = result_1.splitlines()
    dst_commands = result_2.splitlines()
    
    # отправляем конфигурационные команды на маршрутизаторы поочередно
    send_config_commands(src_device_params, src_commands)
    send_config_commands(dst_device_params, dst_commands)
    
    return None




if __name__ == "__main__":
    
    show_comand = ['show']
    ports = []  # список используемых интерфейсов
    
    # получаем лог/пас маршрутизаторов с файла
    try:
        with open("20.5a/data_files/devices.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices.yaml не найден.")
        exit(1)
    
    # подключаемся поочередно к маршрутизаторам
    for device in devices:
        results = []
        print(f"Подключение к {device['host']}... ")
        
        for cmd in show_comand:  # Перебираем команды
            result = send_show_command(device, cmd)
            if result is not None:
                results.append(f"=== Команда: {cmd} ===")
                results.append(result)
    
        # Сохранение результата каждого устройства в отдельный файл
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
             
        filename = f"test_{device['host']}.txt"
        print(f'Сохранение результата в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e:  # Если запись в файл не удалась (например, нет прав), выводим в консоль
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}') 
        print('')
    
        # Читаем сохраненный файл и ищем существующие порты
        with open(f'test_{device['host']}.txt', 'r') as file:
            for line in file:
                match = re.search(r'interface ethernet (\d+)', line)
                if match:
                    ports.append(match.group(1)) # сохраняем найденные порты
    
    # определяем свободный порт на обоих маршрутизаторах
    common_ports = set(map(int, ports)) 

    for i in range(27):
        if i not in common_ports:
            unique_port = i
            break
    print(f"Найден свободный порт: {unique_port}")

         
    data = {
    "tun_num": None,
    "int_ip_1": "192.168.100.1/30",
    "int_ip_2": "192.168.100.2/30",
    "des_ip_1": "NAME_TEST_1",
    "des_ip_2": "NAME_TEST_2",
    "unique_port": unique_port 
    }
    
    
    template_file_1 = "20.5a/templates/src_template.txt"
    template_file_2 = "20.5a/templates/dst_template.txt"
    
    
    
    if len(devices) >= 2:
        src_device = devices[0]  # Первое устройство из YAML-файла
        dst_device = devices[1]  # Второе устройство из YAML-файла

        configure_vpn(
            src_device,      # Передаем словарь с параметрами!
            dst_device,      # Передаем словарь с параметрами!
            template_file_1,
            template_file_2,
            data
        )
    else:
        print("В файле devices.yaml должно быть минимум 2 устройства.")
        
        
# Подключение к 192.168.55.1... 
# выполнение команды: "show"...
# Сохранение результата в файл "test_192.168.55.1.txt"...

# Подключение к 192.168.55.2... 
# выполнение команды: "show"...
# Сохранение результата в файл "test_192.168.55.2.txt"...

# Найден свободный порт: 9

# Подключение к 192.168.55.1...
# Отправка коданд: ['interface ethernet 9', 'description NAME_TEST_1', 'ip address 192.168.100.1/30']...

# Подключение к 192.168.55.3...
# Отправка коданд: ['interface ethernet 9', 'description NAME_TEST_2', 'ip address 192.168.100.2/30']...
    
   