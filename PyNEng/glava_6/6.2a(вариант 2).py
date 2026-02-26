'''
Сделать копию скрипта задания 6.2.
Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
• состоит из 4 чисел (а не букв или других символов)
• числа разделенны точкой
• каждое число в диапазоне от 0 до 255
Если адрес задан неправильно, выводить сообщение: «Неправильный IP-адрес». Сообщение
«Неправильный IP-адрес» должно выводиться только один раз, даже если несколько пунктов
выше не выполнены.
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


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
            break
            
    except ValueError:
        # Если сегменту нельзя присвоить целочисленное значение
        is_valid_ip = False
        break

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



'''
ip_adress = input('введите IP-адреса в формате 10.0.1.1: ')
bits = ip_adress.split('.')

try:
    first_byte = int(bits[0])
    first_byte_1 = int(bits[1])
    first_byte_2 = int(bits[2])
    first_byte_3 = int(bits[3])
    
    if ip_adress.count('.') == 3 and len(bits) == 4 and 0 <= first_byte <= 255 and 0 <= first_byte_1 <= 255 and 0 <= first_byte_2 <= 255 and 0 <= first_byte_3 <= 255:    
                
        if first_byte >=  1 and first_byte <= 223:
            print ('unicast')
        elif first_byte >= 224 and first_byte <= 239:
            print ('multicast')
        elif ip_adress == '255.255.255.255':
            print ('local broadcast')
        elif ip_adress == '0.0.0.0':
            print ('unassigned')
        else:
            print('unused')
    else:
        print('Неправильный IP-адрес')
except ValueError:
    print("Неправильный IP-адрес")
'''