'''Реализуйте функцию unique_in_order, 
которая принимает в качестве аргумента последовательность 
и возвращает список элементов, в котором отсутствуют элементы 
с одинаковым значением, расположенные рядом, и при этом 
сохраняется исходный порядок элементов.

Например:
unique_in_order('AAAABBBCCDAABBB') == ['A', 'B', 'C', 'D', 'A', 'B']
unique_in_order('ABBCcAD')         == ['A', 'B', 'C', 'c', 'A', 'D']
unique_in_order([1, 2, 2, 3, 3])   == [1, 2, 3]
unique_in_order((1, 2, 2, 3, 3))   == [1, 2, 3]
'''
def unique_in_order(sequence):
    result = []
    control = []
    for simbol in sequence:
        if simbol != control:
            result.append(simbol)
        control = simbol
    return result

print(unique_in_order('AAAABBBCCDAABBB'))
print(unique_in_order('ABBCcAD'))       
print(unique_in_order([1, 2, 2, 3, 3]))  
print(unique_in_order((1, 2, 2, 3, 3)))