'''В этом примере вам нужно проверить, является ли введенная
 пользователем строка буквенно-цифровой. 
 Данная строка не является таковой nil/null/NULL/None,
   поэтому проверять это не нужно.

Строка должна быть буквенно-цифровой при следующих условиях:

- Не менее одного символа ( ""недопустимо)
- Допустимые символы: заглавные/строчные латинские буквы 
    и цифры от 0до9
- Без пробелов / подчеркивания'''


def alphanumeric(password: str) -> bool:
    result = password.isalnum() # проверяет только буквы и цифры (a-z, A-Z, 0-9), исключая все спецсимволы автоматически 
    result_2 = len(password) > 0
    return result and result_2

print(alphanumeric("hello world_")) # False
print(alphanumeric("PassW0rd")) # True
print(alphanumeric("     ")) # False
print(alphanumeric("")) # False
