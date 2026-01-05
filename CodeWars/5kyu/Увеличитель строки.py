'''Ваша задача — написать функцию, которая увеличивает 
значение строки для создания новой строки.

Если строка уже заканчивается числом, это число следует
 увеличить на 1.
Если строка не заканчивается числом, к новой строке 
следует добавить число 1.
Примеры:
foo -> foo1
foobar23 -> foobar24
foo0042 -> foo0043
foo9 -> foo10
foo099 -> foo100
Внимание: если число содержит нули в начале,
 следует учитывать количество цифр.'''

def increment_string(strng):
    number = ''
    len_ = len(strng)
    for current_number in range(1, len_ + 1):
        if not strng[-current_number].isdigit():
            break
        number += strng[-current_number]
    
    if number:
        new_number = str(int(number[::-1]) + 1).zfill(len(number))
        new_strng = strng[:-(len(number))]
        return new_strng + new_number

    return strng + '1'
    
    

print(increment_string("1"))# "2")
print(increment_string("foo"))# "foo1")
print(increment_string("foobar001"))# "foobar002")
print(increment_string("foobar1"))# "foobar2")
print(increment_string("foobar00"))# "foobar01")
print(increment_string("foobar199"))#"foobar200")
print(increment_string("foobar099"))# "foobar100")
print(increment_string("fo99obar99"))#"fo99obar100")
print(increment_string(""))# "1")