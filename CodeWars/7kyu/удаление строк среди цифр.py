'''В этом задании вы создадите функцию, 
которая принимает список неотрицательных 
целых чисел и строк и возвращает новый список, 
из которого будут удалены только строки.

Пример
filter_list([1,2,'a','b']) == [1,2]
filter_list([1,'a','b',0,15]) == [1,0,15]
filter_list([1,2,'aasf','1','123',123]) == [1,2,123]
'''

def filter_list(general_list):
    return list(filter(lambda x: isinstance(x, int), general_list))
    

print(filter_list([1,2,'a','b']))
print(filter_list([1,'a','b',0,15]))
print(filter_list([1,2,'aasf','1','123',123]))

