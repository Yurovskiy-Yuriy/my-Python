"""
Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

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

    # Создаем список для строк файла. Заголовок добавляем сразу.
    results = [f"--- Конфигурация устройства {device['host']} ---"]

    # Логика выбора действия
    if show:
        print(f'выполнение команды: "{show}" на {device["host"]}...')
        command_output = send_show_command(device, show)
        results.append(f"=== Команда: {show} ===")
        results.append(command_output or "Нет вывода / Ошибка при выполнении команды")

    # Сохранение резульатта в файл
    try:    
        with open(filename, 'a', encoding='utf-8') as file_out:
            file_out.write('\n'.join(results))
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