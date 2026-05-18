"""
Создать функцию send_command_to_devices, которая отправляет список указанных
команд show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой
команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Для выполнения задания можно создавать любые дополнительные функции,
а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
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

# функция-обертка 
# Теперь функция сама формирует результат и сохраняет его в файл.
def send_commands(device, filename, *, show=None, config=None):
    
    # Проверка: передан ровно один из аргументов
    if show and config:
        raise ValueError("Оба аргумента переданы. Нужно передавать только один: show или config.")
    
    if not show and not config:
        raise ValueError("Не передан ни один из аргументов. Нужно передать show или config.")

    # Получаем имя хоста из словаря устройства
    hostname = device['host']

    # Логика выбора действия
    if show:
        print(f'выполнение команды: "{show}" на {device["host"]}...')
        results = send_show_command(device, show)

        # Сохранение резульатта в файл
        try:    
            with open(filename, 'a', encoding='utf-8') as file_out:
                file_out.write(f"{hostname}#{show}\n")
              
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
        
    show_comand = ['show ip arp', 'show']
    
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
                
        # Обрабатываем результаты по мере их готовности
        for future in as_completed(futures):
            # Получаем результат выполнения (или исключение)
            try:
                future.result() # Проверяем, не было ли исключений внутри потока
            except Exception as e:
                print(f"Произошла ошибка в одном из потоков: {e}")