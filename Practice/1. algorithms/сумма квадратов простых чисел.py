'''Напишите функцию calculate_special_sum(numbers), которая принимает список целых положительных чисел
и возвращает сумму квадратов тех чисел, которые являются простыми числами. Простым называется число,
большее единицы, которое делится нацело только на единицу и на себя.

Например:

    Число 2 простое, потому что оно делится только на 1 и 2.
    Число 4 не простое, потому что кроме 1 и 4 оно также делится на 2.

Если простых чисел среди заданных нет, вернуть ноль.

Входные данные:
Список целых положительных чисел numbers, где количество элементов находится 
в диапазоне от 1 до 100 включительно, сами числа находятся в диапазоне от 1 до 1000 включительно.

Выходные данные:
Сумма квадратов всех простых чисел из списка.
Примеры:

    calculate_special_sum([2, 3, 4]) → 13 (потому что 2^2 + 3^2=4+9=13).
    calculate_special_sum([4, 6, 8]) → 0 (простых чисел нет).
    calculate_special_sum([11, 13, 17]) → 579 (11^2 + 13^2+17^2=121+169+289=579).'''
    
    
def calculate_special_sum(numbers):
    #return sum(int(x) ** 2 for x in numbers)
    result = []
    for x in numbers:
        zirro = True
        index = 2
        while index < int(x):
            if int(x) % index == 0:
                zirro = False
                #print(x, index, zirro)
                break
            else:
                index += 1
        if zirro == True:
            x = str(x)
            result.append(x)
            
    if len(result) != 0:
        return sum(int(x) ** 2 for x in result)
    else:
        result = ('простых чисел нет')
        return result
                               
            
print(calculate_special_sum([2, 3, 4])) # 13 (потому что 2^2 + 3^2=4+9=13).
print(calculate_special_sum([4, 6, 8])) # 0 (нет простых чисел).
print(calculate_special_sum([11, 13, 17])) # 579 (11^2 + 13^2+17^2=121+169+289=579).
    
    