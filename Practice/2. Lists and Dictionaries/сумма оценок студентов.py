''' обюъедените два список в один, суммируя оценки студентов'''
list1 = [{'name': 'Alice', 'math': 85}]
list2 = [{'name': 'Alice', 'math': 90, 'physics': 88}]


# Создаем пустой словарь для хранения итоговых результатов
result_dict = {}

# Добавляем элементы первого списка
for student in list1:
    name = student['name']
    result_dict[name] = {subject: score for subject, score in student.items() if subject != 'name'}
    

# Обрабатываем второй список
for student in list2:
    name = student['name']
    # Проверяем, существует ли студент в результате
    if name in result_dict:
        # Суммируем оценки по предметам
        for subject, score in student.items():
            if subject != 'name':
                if subject in result_dict[name]:
                    result_dict[name][subject] += score
                else:
                    result_dict[name][subject] = score
    else:
        # Если студента нет, добавляем его сразу
        result_dict[name] = {subject: score for subject, score in student.items() if subject != 'name'}

# Преобразуем обратно в список словарей
final_list = []
for name, subjects in result_dict.items():
    final_list.append({'name': name, **subjects})

print(final_list)





#list1 = [{'name': 'Alice', 'math': 175, 'physics': 88}]