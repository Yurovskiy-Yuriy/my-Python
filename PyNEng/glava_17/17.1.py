'''Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод команды show
dhcp snooping binding из разных файлов и записывает обработанные данные в csv файл.

Аргументы функции:
    • filenames - список с именами файлов с выводом show dhcp snooping binding
    • output - имя файла в формате csv, в который будет записан результат
    
Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress IpAddress Lease(sec) Type VLAN Interface
------------------ --------------- ---------- ------------- ---- --------------------
00:E9:BC:3F:A6:50 100.1.1.6 76260 dhcp-snooping 3 FastEthernet0/20
00:E9:22:11:A6:50 100.1.1.7 76260 dhcp-snooping 3 FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла, остальные - из
содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.'''

import re
import csv

def write_dhcp_snooping_to_csv(filenames, output):
    data = ['switch','mac','ip','vlan','interface']
    with open(output, 'w', newline='') as f:  # открываем файл для записи шапки
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
        writer.writerow(data)

    for filename in filenames:  # перебираем файлы
        match2 = re.search(r'^(?P<device>[^_]+)_', filename)
        if not match2:
            print(f"Не удалось найти имя файла: {filename}")
            
        with open(f'./{filename}', 'r') as f: # открываем поочередно файлы
            for line in f:
                match = re.match(r'(?P<mac>\w+:\w+:\w+:\w+:\w+:\w+)\s+'
                                 r'(?P<ip>\d+.\d+.\d+.\d+)\s+'
                                 r'(\d+)\s+([^ ]+)\s+'
                                 r'(?P<vlan>\d+)\s+'
                                 r'(?P<interface>[^ ]+)', line)
                if match:
                    with open(output, 'a') as file_out: # открываем файл для записи строки
                        line = (                         
                            f'{match2.group('device')}'
                            f'{match.group('mac')},'
                            f'{match.group('ip')},'
                            f'{match.group('vlan')},'
                            f'{match.group('interface')}'
                        )  # формируем строку
                        
                        file_out.write(line ) # записываем строку в .csv

    
write_dhcp_snooping_to_csv(['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt'], 'result_17.1.csv')

# sw1_dhcp_snooping.txt:

# MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
# ------------------  ---------------  ----------  -------------  ----  --------------------
# 00:09:BB:3D:D6:58   10.1.10.2        86250       dhcp-snooping   10    FastEthernet0/1
# 00:04:A3:3E:5B:69   10.1.5.2         63951       dhcp-snooping   5     FastEthernet0/10
# 00:05:B3:7E:9B:60   10.1.5.4         63253       dhcp-snooping   5     FastEthernet0/9
# 00:07:BC:3F:A6:50   10.1.10.6        76260       dhcp-snooping   10    FastEthernet0/3
# 00:09:BC:3F:A6:50   192.168.100.100  76260       dhcp-snooping   1     FastEthernet0/7
# Total number of bindings: 5

# result:

# switch,mac,ip,vlan,interface
# sw1,00:09:BB:3D:D6:58,10.1.10.2,10,FastEthernet0/1
# sw1,00:04:A3:3E:5B:69,10.1.5.2,5,FastEthernet0/10
# sw1,00:05:B3:7E:9B:60,10.1.5.4,5,FastEthernet0/9
# sw1,00:07:BC:3F:A6:50,10.1.10.6,10,FastEthernet0/3
# sw1,00:09:BC:3F:A6:50,192.168.100.100,1,FastEthernet0/7
# sw2,00:A9:BB:3D:D6:58,10.1.10.20,10,FastEthernet0/7
# sw2,00:B4:A3:3E:5B:69,10.1.5.20,5,FastEthernet0/5
# sw2,00:C5:B3:7E:9B:60,10.1.5.40,5,FastEthernet0/9
# sw2,00:A9:BC:3F:A6:50,10.1.10.60,20,FastEthernet0/2
# sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
# sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21
