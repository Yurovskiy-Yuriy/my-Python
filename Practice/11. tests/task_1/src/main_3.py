'''Магазин «Шестёрочка» проводит конкурс, где победителем станет
 каждый третий покупатель. Выведите номера чеков победителей из 
 списка чеков receipts и посчитайте их количество.

receipts = [123, 145, 346, 246, 235, 166, 112, 351, 436]'''

def solve(receipts: list):
    i = 1
    result = []
    count = 0
    for number in receipts:
        if i % 3 == 0:
           result.append(number)
           count += 1
        i += 1
    
    return result, len(result) 

receipts = [123, 145, 346, 246, 235, 166, 112, 351, 436]
print(solve(receipts))

