'''
Напишите функцию, которая принимает на вход 
неотрицательное целое число (секунды) и возвращает время 
в удобочитаемом формате ( HH:MM:SS).

HH= часы, дополненные до 2 цифр, диапазон: 00 - 99
MM= минуты, дополненные до 2 цифр, диапазон: 00 - 59
SS= секунды, дополненные до 2 цифр, диапазон: 00 - 59
Максимальное время никогда не превышает 359999 ( 99:59:59)
'''

def make_readable(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds - (hours * 3600)) / 60)
    second = seconds - (hours * 3600 + minutes * 60)
    return f'{hours:02}:{minutes:02}:{second:02}'


print(make_readable(0)) # "00:00:00")
print(make_readable(59)) # "00:00:59")
print(make_readable(60)) # "00:01:00")
print(make_readable(3599)) # "00:59:59")
print(make_readable(3600)) # "01:00:00")
print(make_readable(86399)) # "23:59:59")
print(make_readable(86400)) #"24:00:00")
print(make_readable(359999)) #"99:59:59")

