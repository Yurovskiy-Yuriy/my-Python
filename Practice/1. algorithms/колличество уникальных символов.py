'''Выведите колличество уникальных символов в строке, игнорируя регистр букв и пррбелы'''

input_string = 'Python is funy, t!'
string = set(input_string.lower().replace(' ', ''))
#print(string)
simbol = list(filter(lambda x: input_string.count(x) > 1, string))
print(len(simbol))