# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

# размещяем ФИО в соответствующие столбики
def placement_names(row): 
        # ищем пробел в первом столбике
        if ' ' in row[0]:
          name_parts = row[0].split(' ')
          
          # проверяем наличие путсых столбиков, и заполняем их, чтобы в дальнейшем у нас не сместилась вся строка
          if len(name_parts) == 2:  # их может быть 1 или 2, т.к мы начали с первого, а всего их 3
                 name_parts.append('')
          elif len(name_parts) == 1:
                 name_parts.extend(['', ''])

          new_row = name_parts + row[3:] # добавляем в список начиная с organization

        # ищем пробел во втором столбике
        elif ' ' in row[1]:
           name_parts = row[1].split(' ')

           # проверяем наличие путсых столбиков, и заполняем их, чтобы в дальнейшем у нас не сместилась вся строка
           if len(name_parts) == 1: # он может быть только 1, т.к мы начали со второга, а всего их 3
                 name_parts.append('')

           new_row = [row[0]] + name_parts + row[3:]

        else:
           new_row = row
        
        return new_row

# форматирование телефонного номера в +7(999)999-99-99
def formatting_number(line):
    # проверяем, есть ли добавочный номер
    match_with_dob = re.search(r"доб\.?\s*(\d{4})", line[5])

    if match_with_dob:
        phone_pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[-]?(\d{2})\s?\(?д?о?б?\.?\s?(\d{4})\)?"
        replacement_pattern = r"+7(\2)\3-\4-\5 доб.\6"  
    else:
        phone_pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[-]?(\d{2})"
        replacement_pattern = r"+7(\2)\3-\4-\5"    

    line[5] = re.sub(phone_pattern, replacement_pattern, line[5])

    return line

# поиск совпадение по ФИО
def match_indicator(x, y):   
    for a, b in zip(x, y):
        if a != '' and b != '' and a != b:
            return False  # совпадений нет
    return True  # все сопадаеи с учетом пустых записей

# объединение совпадающих строк в одну
def concatenation_strings(x, y): 
    new_string = []
    for a, b in zip(x, y):

        if a == '' or b == '' and a != b: 
            new_string.append(a + b)
        elif a == b:
            if a =='':
                new_string.append(b)
            else:
                new_string.append(a)
        elif a != b:
            new_string.append(f'{a}. {b}')
             
    return new_string
        


if __name__ == "__main__":

    # 1. Поместим Фамилию, Имя и Отчество в поля lastname, firstname и surname соответственно.
    new_phonebook = []

    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")

        for row in rows:
            new_row = placement_names(row)
            new_phonebook.append(new_row)

    # 2. Приведем все телефоны в формат +7(999)999-99-99 или +7(999)999-99-99 доб.9999
    next_phonebook = []

    for line in new_phonebook:
        new_line = formatting_number(line)
        next_phonebook.append(new_line)

    # 3. Объедим все дублирующиеся записи о человеке в одну
    result_phonebook = []
    result_phonebook.append(next_phonebook[0]) # добавлям шапку

    for lines_next_phonebook in next_phonebook[1:]: # перебираем телефонный список
        found = False  # индикатор: нашли ли совпадение во всем списке
        index_of_duplicate = -1  # для хранения индекса дублирующей строки

        for i, line_result_phonebook in enumerate(result_phonebook): # перебираем окончательный телефонный список
            #ищем совпадение по ФИО
            if match_indicator(line_result_phonebook[:3], lines_next_phonebook[:3]):
                found = True # нашли совпадение
                index_of_duplicate = i  # запоминаем индекс дублирующей строки
                break

        if not found: # совпадений нет   
            result_phonebook.append(lines_next_phonebook)
        else:
            # Заменяем старую строку на объединенную
            new_line = concatenation_strings(lines_next_phonebook, result_phonebook[index_of_duplicate])
            result_phonebook[index_of_duplicate] = new_line

    # сохраняем получившиеся данные в другой файл
    with open('phonebook.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(result_phonebook)
        print('Адресная книга успешно сохранена: phonebook.csv')
        
