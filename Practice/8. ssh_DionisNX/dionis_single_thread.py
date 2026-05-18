'''
Скрипт поочередно подключается к устройсвам (DionisNX), и выполняет рад команд, результат сохраняет в txt файл

Примечаение, если нужно выполнить команы в конфигорационом режиме, тогда отправляем команды с переменной 
commands, а если .... тогда с show_comand 
'''

# скрипт написан для DionisNX

import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


# функция для команды show
def send_show_command(device_params, command):
        
    try:
        with ConnectHandler(**device_params) as ssh:
            output = ssh.send_command(command)
            return output
    except (NetMikoTimeoutException, NetMikoAuthenticationException, Exception) as e:
        print(f"Ошибка подключения к {device_params['host']}: {e}")
        return None

# функция для списка команд 
def send_config_commands(device_params, config_commands):

    # device_params = device.copy()
    # Устанавливаем правильный тип устройства
    dionis_device = device.copy()
    dionis_device['device_type'] = 'linux'
    # Увеличиваем таймаут, так как вход в режим конфигурирования может быть долгим
    dionis_device['global_delay_factor'] = 2 

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


# функция-обертка 
def send_commands(device, *, show=None, config=None):
    
    # Проверка: передан ровно один из аргументов
    if show and config:
        raise ValueError("Оба аргумента переданы. Нужно передавать только один: show или config.")
    
    if not show and not config:
        raise ValueError("Не передан ни один из аргументов. Нужно передать show или config.")

    # Логика выбора действия
    if show:
        print(f'выполнение команды: "{show}"...')
        # Вызываем функцию для команды show
        return send_show_command(device, show)
    
    if config:
        # Вызываем функцию для списка команд конфигурации
        return send_config_commands(device, config)


if __name__ == "__main__":

    try:
        with open("devices_4 copy.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_4 copy.yaml не найден.")
        exit(1)
        

    # commands = ('interface ethernet 2', 'description PRIMER', 'ip address 192.168.55.1/24')
    show_comand = ['show ip arp', 'show version']
  

    # Проверяем работу на первом устройстве из списка
    for device in devices:
        results = []
        print(f"Подключение к {device['host']}... ")
        
        for cmd in show_comand:  # Перебираем команды
            result = send_commands(device, show=cmd)
            if result is not None:
                results.append(f"=== Команда: {cmd} ===")
                results.append(result)
                results.append('')
                
        # Заголовок добавляем один раз, если есть хоть какой-то результат
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
            
        # Сохранение каждого устройства в отдельный файл
        filename = f"test_{device['host']}.txt"
        print(f'Сохранение результата в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e:  # Если запись в файл не удалась (например, нет прав), выводим в консоль
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')       
        print('')
                
 
    
        # print("\nРезультат выполнения команды config:")
        # result_config = send_commands(device, config=commands)
        
        # if result_config is not None:
        #     pprint(result_config)

        
        
