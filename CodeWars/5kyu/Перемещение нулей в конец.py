'''
Напишите алгоритм, который принимает массив и перемещает 
все нули в конец, сохраняя при этом порядок остальных 
элементов.

move_zeros([1, 0, 1, 2, 0, 1, 3]) # returns [1, 1, 2, 1, 3, 0, 0]
'''

def move_zeros(lst):
    result = list()
    zeros = list()
    for number in lst:
        if number == 0:
            zeros.append(number)
        else:
            result.append(number)
    result += zeros
    return result



print(move_zeros([1, 2, 0, 1, 0, 1, 0, 3, 0, 1])) #[1, 2, 1, 1, 3, 1, 0, 0, 0, 0])
print(move_zeros([9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]))
                #[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
print(move_zeros([0, 0]))   # [0, 0])
print(move_zeros([0]))     # [0])
print(move_zeros([]))     # [])