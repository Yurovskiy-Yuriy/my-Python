
"""
Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#

Для выполнения задания можно создавать любые дополнительные функции.
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