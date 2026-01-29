'''
Сделать копию скрипта задания 7.3a.
Переделать скрипт:
• Запросить у пользователя ввод номера VLAN.
• Выводить информацию только по указанному VLAN.
Пример работы скрипта:
Enter VLAN number: 10
10 0a1b.1c80.7000 Gi0/4
10 01ab.c5d0.70d0 Gi0/8
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
enter_vlan = input('Enter VLAN number: ')

with open(r'D:\CAM_table.txt') as f:
          lines = []  # Список для хранения нужных строк
        
          for line in f:
              if line.count('.') == 2: # Условие проверки наличия двух точек
                  parts = line.split()  # ['100', '01bb.c580.7000', 'DYNAMIC', 'Gi0/1']
                  vlan_number = int(parts[0])   # 100 
                  # Добавление кортежа: (номер VLAN, сама строка)
                  lines.append((vlan_number, line.rstrip())) # [(100, ' 100    01bb.c580.7000    DYNAMIC     Gi0/1')]
              
lines.sort(key=lambda x: x[0]) # Сортировка кортежа по номеру VLAN

for vlan_number, line in lines:  
    if int(vlan_number) == int(enter_vlan):
        print(line.replace('DYNAMIC', ''))  # игнорируем vlan_number

