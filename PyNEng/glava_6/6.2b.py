'''
Сделать копию скрипта задания 6.2a.
Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


is_valid_ip = False

while is_valid_ip == False:
            
    ip_address = input('Введите IP-адрес в формате 10.0.1.1: ')
    octets = ip_address.split('.')

    is_valid_ip = True

    # Проверка наличия ровно трех точек и 4 октетов
    if len(octets) != 4 or ip_address.count('.') != 3:
        is_valid_ip = False

    # Проверка диапазона октетов (каждый должен быть числом от 0 до 255)
    for octet in octets:
        try:
            # Пробуем конвертировать каждый сегмент в целое число
            num_octet = int(octet)
            
            # Проверяем диапазон значений
            if not (0 <= num_octet <= 255):
                is_valid_ip = False
                break   # <-- Первый случай: выход из цикла for, если октет вне диапазона
                
        except ValueError:
            # Если сегменту нельзя присвоить целочисленное значение
            is_valid_ip = False
            break  # <-- Второй случай: выход из цикла for, если октет не преобразуется в число

    # Если IP некорректен, выводим сообщение
    if not is_valid_ip:
        print('Неправильный IP-адрес')
    else:
        # Здесь начинаем классификацию IP-адреса
        first_octet = int(octets[0])
        
        if first_octet >= 1 and first_octet <= 223:
            print('unicast')
        elif first_octet >= 224 and first_octet <= 239:
            print('multicast')
        elif ip_address == '255.255.255.255':
            print('local broadcast')
        elif ip_address == '0.0.0.0':
            print('unassigned')
        else:
            print('unused')



