'''Найти товары, цена которых превышает среднее значение всех цен'''

prices = {'яблоки': 80, 'груши': 120, 'виноград': 150}
max_many = 0

for index, many in enumerate(prices.values(), start=1):
    max_many += int(many)
first_many = max_many / index

result = []
for index, many in prices.items():
    if many > first_many:
        #result.append(f'{index}: {many}')
        result.append({index: many})
print(result)


