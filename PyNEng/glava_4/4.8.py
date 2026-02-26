ip = "192.168.3.1"

print(ip)
print(type(ip))
print()

#ip = list(ip)
#print(ip)
#print(type(ip))
#print()

ip = [192, 168, 3, 1]
print(ip)
print(type(ip))

#загатовка шаблона для любых данных (b-означает перевод в двоичный формат)
ip_template = '''
IP address:
{0:8} {1:8} {2:8} {3:8}
{0:08b} {1:08b} {2:08b} {3:08b}
'''

print('\n' + '-' * 40)

#выводим шаблон и подставляем в него даные из переменной ip
print(ip_template.format(ip[0], ip[1], ip[2], ip[3]))