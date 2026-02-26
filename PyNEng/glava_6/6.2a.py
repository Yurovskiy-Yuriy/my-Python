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
    print("Неправильный IP-адрес2")


            
           
    


    
'''
  for bit in bits[i]:
        if int(bit) >= 0 and int(bit) <=255:
            й
            first_byte = int(bits[0])
'''