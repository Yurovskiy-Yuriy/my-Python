'''
Создайте функцию, которая принимает в качестве аргумента римскую цифру
 и возвращает её значение в виде десятичного целого числа. 
 Проверять формат римской цифры не требуется.

Современные римские цифры записываются путем отдельного обозначения
 каждой десятичной цифры кодируемого числа, начиная с самой левой цифры 
 и пропуская все нули. Так, 1990 обозначается как "MCMXC" 
 (1000 = M, 900 = CM, 90 = XC), а 2008 — как "MMVIII" (2000 = MM, 8 = VIII). 
 Римская цифра 1666, "MDCLXVI", использует буквы в порядке убывания.

Пример:
"MM"      -> 2000
"MDCLXVI" -> 1666
"M"       -> 1000
"CD"      ->  400
"XC"      ->   90
"XL"      ->   40
"I"       ->    1
Помощь:
Symbol    Value
I          1
V          5
X          10
L          50
C          100
D          500
M          1,000
'''
def solution(roman : str) -> int:
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    result = 0
    prev = 0
    for x in roman:
        curr = roman_numerals[x]
        if prev < curr:
            result -= prev  
        else:
            result += prev
        prev = curr
    result += prev  
    return result


print(solution('MMMCMXCIX')) #       3999
print(solution('MMMDCCCLXXXVIII'))# 3888
print(solution('MM'))#              2000
print(solution('MDCLXVI'))#         1666
print(solution('M')) #              1000
print(solution('CD'))#               400
print(solution('XC'))#                90
print(solution('XL'))#                40
print(solution('I')) #                1
