"""
Скрипт многопоточно подключается сразу к нескольким устройсвам (DionisNX),
и выполняет рад команд, результат сохраняет в txt файл

Примечаение, если нужно выполнить команы в конфигорационом режиме,
тогда отправляем команды с переменной commands, а если .... тогда с show_comand 
"""


# скрипт написан для DionisNX

import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

from concurrent.futures import ThreadPoolExecutor, as_completed

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
# Теперь функция сама формирует результат и сохраняет его в файл.
def send_commands(device, filename, *, show=None, config=None):
    
    # Проверка: передан ровно один из аргументов
    if show and config:
        raise ValueError("Оба аргумента переданы. Нужно передавать только один: show или config.")
    
    if not show and not config:
        raise ValueError("Не передан ни один из аргументов. Нужно передать show или config.")

    # Получаем имя хоста из словаря устройства
    # results = device['host']
    results = [f"--- Конфигурация устройства {device['host']} ---"]

    # Логика выбора действия
    if show:
        print(f'выполнение команды: "{show}" на {device["host"]}...')
        results = send_show_command(device, show)

        # Сохранение резульатта в файл
        try:    
            with open(filename, 'a', encoding='utf-8') as file_out:
                file_out.write(f"{results}#{show}\n")
              
                if results is not None:
                    file_out.write(results)
                else:
                    # Если results is None, значит произошла ошибка подключения
                    file_out.write("Команда не выполнена из-за ошибки подключения.\n")
            
            print(f'Сохранение результата в файл "{filename}"... УСПЕШНО')
        except OSError as e:
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')
        
        return
    
    if config:
        print(f'выполнение команды: "{config}" на {device["host"]}...')
        results = send_config_commands(device, config)
        
        # Сохранение резульатта в файл
        try:    
            with open(filename, 'a', encoding='utf-8') as file_out:
                file_out.write(f"{results}#{show}\n")
              
                if results is not None:
                    file_out.write(results)
                else:
                    # Если results is None, значит произошла ошибка подключения
                    file_out.write("Команда не выполнена из-за ошибки подключения.\n")
            
            print(f'Сохранение результата в файл "{filename}"... УСПЕШНО')
        except OSError as e:
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')
        
        return


if __name__ == "__main__":

    try:
        with open("devices_4 copy.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_4 copy.yaml не найден.")
        exit(1)
        
    # commands = ('interface ethernet 2', 'description TEST_TEST_TEST', 'ip address 192.168.55.1/24')
    # show_comand = ['show ip arp', 'show version']
    show_comand = ['show']
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Создаём список будущих результатов
        futures = []
        
        # выполнение команды show
        for device in devices:
            for command in show_comand:
                filename = f"test_{device['host']}.txt"
                
                # выполнение команды show
                future = executor.submit(send_commands, device, filename, show=command)
                
                futures.append(future)
                
        # выполнение команды configure
        # for device in devices:
        #     filename = f"test_{device['host']}.txt"   
        #     future = executor.submit(send_commands, device, filename, config=commands)
        #     futures.append(future)   
                
        # Обрабатываем результаты по мере их готовности
        for future in as_completed(futures):
            # Получаем результат выполнения (или исключение)
            try:
                future.result() # Проверяем, не было ли исключений внутри потока
            except Exception as e:
                print(f"Произошла ошибка в одном из потоков: {e}")