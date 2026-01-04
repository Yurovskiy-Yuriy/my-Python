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

with open(r'D:\soft\DAEMON_Tools\5\7\CAM_table.txt') as f:
          lines = []  # Список для хранения нужных строк
        
          for line in f:
              if str(line.count('.')) == str(2): # Условие проверки наличия двух точек
                  parts = line.split()
                  vlan_number = int(parts[0])   # Преобразование первой части строки (VLAN) в целое число
                  
                  # Добавление кортежа: (номер VLAN, сама строка)
                  lines.append((vlan_number, line.rstrip()))
                 

# Сортировка по номеру VLAN
lines.sort(key=lambda x: x[0])

for _, line in lines:
    print(line.replace('DYNAMIC', ''))



                  
#                  vlans.append(line.strip().replace('DYNAMIC', '').rstrip())
#                  number = vlans.split()
                  #print(line.rstrip().replace('DYNAMIC', ''))
#output = "\n".join(vlans)

#print(vlans)
#print(output)
