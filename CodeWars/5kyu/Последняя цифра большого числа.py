'''Определите функцию, которая принимает на вход два неотрицательных целых числа.
а и б, и возвращает последнюю десятичную цифру
а ^ б. Обратите внимание, что а и б. Может быть, очень большим!

Например, последняя десятичная цифра 9^7, является 9. 9^7 = 4782969
Также, пожалуйста, возьмите 0^0 быть 1.

Примеры
last_digit(4, 1)                # returns 4
last_digit(4, 2)                # returns 6
last_digit(9, 7)                # returns 9
last_digit(10, 10 ** 10)        # returns 0
last_digit(2 ** 200, 2 ** 300)  # returns 6'''

def last_digit(n1, n2):
    if n2 == 0:
        return 1
    return pow(n1, n2, 10) 

print(last_digit(4, 1))                # returns 4
print(last_digit(4, 2))                # returns 6
print(last_digit(9, 7))                # returns 9
print(last_digit(10, 10 ** 10))        # returns 0
print(last_digit(2 ** 200, 2 ** 300))  # returns 6'''

