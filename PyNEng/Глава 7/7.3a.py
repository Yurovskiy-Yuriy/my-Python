'''
Сделать копию скрипта задания 7.3.
Переделать скрипт: Отсортировать вывод по номеру VLAN В результате должен получиться
такой вывод:
10 01ab.c5d0.70d0 Gi0/8
10 0a1b.1c80.7000 Gi0/4
100 01bb.c580.7000 Gi0/1
200 0a4b.c380.7c00 Gi0/2
200 1a4b.c580.7000 Gi0/6
300 0a1b.5c80.70f0 Gi0/7
300 a2ab.c5a0.700e Gi0/3
500 02b1.3c80.7b00 Gi0/5
1000 0a4b.c380.7d00 Gi0/9

'''

with open(r'D:\CAM_table.txt') as f:
          lines = []  # Список для хранения нужных строк
        
          for line in f:
              if line.count('.') == 2: # Условие проверки наличия двух точек
                  parts = line.split()  # ['100', '01bb.c580.7000', 'DYNAMIC', 'Gi0/1']
                  vlan_number = int(parts[0])   # 100 
                  # Добавление кортежа: (номер VLAN, сама строка)
                  lines.append((vlan_number, line.rstrip())) # [(100, ' 100    01bb.c580.7000    DYNAMIC     Gi0/1')]
              
lines.sort(key=lambda x: x[0]) # Сортировка кортежа по номеру VLAN

for vlan_number, line in lines:  #
    print(line.replace('DYNAMIC', ''))  # игнорируем vlan_number

