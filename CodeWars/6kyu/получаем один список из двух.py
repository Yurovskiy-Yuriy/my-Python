'''Внедрить функцию, которая вычисляет разницу между двумя списками. 
Функция должна удалять все проявления элементов из первого списка (a),
которые присутствуют во втором списке (b) Порядок элементов в первом 
списке должен быть сохранен в результате.
Примеры

Если a = [1, 2] и b = [1], результат должен быть [2].

Если a = [1, 2, 2, 2, 3] и b = [2], результат должен быть [1, 3].
'''
def array_diff(a, b):
    result = []
    for x in a:
        if x not in b:
            result.append(x)
    return result


print(array_diff([1,2], [1]))        #[2])        #"a was [1,2], b was [1], expected [2]")
print(array_diff([1,2,2], [1]))      # [2,2]) # "a was [1,2,2], b was [1], expected [2,2]")
print(array_diff([1,2,2], [2]))      # [1]) #"a was [1,2,2], b was [2], expected [1]")
print(array_diff([1,2,2], []))       # [1,2,2]) #"a was [1,2,2], b was [], expected [1,2,2]")
print(array_diff([], [1,2]))         # []) # "a was [], b was [1,2], expected []")
print(array_diff([1,2,3], [1, 2]))   #[3]) # "a was [1,2,3], b was [1, 2], expected [3]")