'''Система студентов
Создай класс Student для управления успеваемостью. 
Закрепит классы + списки словарей + вычисления.

Требования:
1) __init__:
	-name (ФИО)
	-grades = [] (список оценок)

2) Каждая оценка — словарь:

	{"subject": "Математика", "grade": 4, "date": "2026-01-20"}
3) add_grade(subject, grade):
	-Добавляет оценку если предмет новый
	-"Оценка по {subject} уже есть!"

4)update_grade(subject, new_grade):
	-Обновляет оценку по предмету
	-"Предмета нет!"

5)average_grade() → возвращает средний балл

6)show_grades():
	📚 Оценки студента "Иван Иванов":
	1. Математика: 4.0
	2. Физика: 3.5  
	3. Русский: 5.0
	Средний балл: 4.2
Тест:

student = Student("Иван Иванов")
student.add_grade("Математика", 4)
student.add_grade("Физика", 3.5)
student.add_grade("Математика", 5)  # Уже есть!

student.update_grade("Физика", 4)
print(f"Средний балл: {student.average_grade():.1f}")

student.show_grades()

Ожидаемый вывод:

Оценка по Математике уже есть!
Средний балл: 4.2
📚 Оценки студента "Иван Иванов":
1. Математика: 4.0
2. Физика: 4.0
3. Русский: 5.0
Средний балл: 4.3'''

from datetime import date
today = date.today()

class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, subject, grade):
        for x in self.grades:
            if subject in x['subject']:
                print(f'Оценка по {subject} уже есть!')
                return
        self.grades.append({"subject": subject, "grade": grade, "date": today})

    def update_grade(self, subject, new_grade):
        subject_exists = False
        for x in self.grades:
            if subject in x['subject']:
                x['grade'] = new_grade
                print(f'Оценка по "{x['subject']}" обновлена')
                subject_exists = True
        if subject_exists == False: 
            print(f'Предмета {subject} нет!') 
           
    
    def average_grade(self):
        y = 0
        sum_ = 0
        for x in self.grades:
            sum_ += x['grade']
            y += 1
        return (sum_ / y)
    
    def show_grades(self):
        n = 1
        print(f'📚 Оценки студента "{self.name}":')
        for x in self.grades:
            print(f'{n}. {x['subject']}: {x['grade']}')
            n += 1

student = Student("Иван Иванов")
student.add_grade("Математика", 4)
student.add_grade("Физика", 3.5)
student.add_grade("Математика", 5)  # Уже есть!
student.add_grade("Руский язык", 3) 
print('')
student.show_grades()
print('')
student.update_grade("Физика", 4)
student.update_grade("Руский язык", 2)
print('')
student.show_grades()
print(f"Средний балл: {student.average_grade():.1f}")
