'''
Сделать копию скрипта задания 7.3a.
Переделать скрипт:
• Запросить у пользователя ввод номера VLAN.
• Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10      0a1b.1c80.7000      Gi0/4
10      01ab.c5d0.70d0      Gi0/8
'''

vl = input('Введите номер VLAN: ')

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
#print(lines[0][0])

i = 0    
for __, line in lines: 
    if int(lines[i][0]) == int(vl):
       # print(lines[i][0])
        print(line.replace('DYNAMIC', ''))
    i += 1
        



            