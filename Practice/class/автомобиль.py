'''Задание: Система управления автомобилем
Создай класс Car, который моделирует автомобиль.

Требования:
Инициализатор __init__ принимает:

- brand (марка, строка)
- model (модель, строка)
- year (год выпуска, число)
- fuel (топливо, изначально 100 литров)
- is_running (работает ли двигатель, изначально False)

Метод start():
- Запускает двигатель (self.is_running = True)
- Выводит: "Двигатель {brand} {model} запущен"

Метод stop():
- Останавливает двигатель (self.is_running = False)
- Выводит: "Двигатель остановлен"

Метод drive(km):
- Принимает расстояние в км
- Только если двигатель запущен:
	-Списывает 0.1 л/км (self.fuel -= km * 0.2)
	- Выводит: "Проехали {km} км. Осталось топлива: {fuel:.1f} л"
- Если двигатель выключен: "Запустите двигатель!"
- Если топлива нет: "Недостаточно топлива!"

Метод show_info():
- Выводит всю информацию об автомобиле:

Toyota Camry 2023
Двигатель: запущен/остановлен
Топливо: 45.5 л


Тестовый код (проверь на нем):
# Создай класс и протестируй:
my_car = Car("Toyota", "Camry", 2023)
my_car.show_info()

my_car.start()
my_car.drive(50)
my_car.show_info()

my_car.drive(600)  # Недостаточно топлива
my_car.stop()'''

class Car:
    def __init__(self, brand, model, year, fuel = 100, is_running = False):
        self.brand = brand
        self.model = model
        self.year = year 
        self.fuel = fuel 
        self.is_running = is_running
    
    def start(self):
        self.is_running = True
        print('Двигатель запущен')
    
    def stop(self):
        self.is_running = False
        print('Двигатель остановлен')
    
    def drive(self, distance):
        if self.is_running == False:
            print('Запустите двигатель!')
            return
        
        needed_fuel = distance * 0.2
        if self.fuel < needed_fuel:
            print('Недостаточно топлива!')
            return
        
        self.fuel -= needed_fuel 
        print(f'Проехали {distance} км. Осталось топлива: {self.fuel:.1f} л')
    
    def show_info(self):
        print(f'Марка: {self.brand}, модель: {self.model}, год выпуска: {self.year}')
    
# Создай класс и протестируй:
my_car = Car("Toyota", "Camry", 2023)
my_car.show_info()

print('')
my_car.start()
my_car.drive(50)

print('')
my_car.drive(600)  # Недостаточно топлива

print('')
my_car.stop()

print('')
my_car.drive(50)

