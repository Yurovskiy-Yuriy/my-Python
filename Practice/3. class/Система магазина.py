'''Создай класс Shop для онлайн-магазина.
Это задание закрепит классы + добавит работу со списками.

Требования:
1) __init__ принимает:
	-name (название магазина)
	-items (список товаров по умолчанию пустой [])

2) Метод add_item(name, price):
	-Добавляет товар в список только если его нет
	-Формат: {"name": "Хлеб", "price": 50}
	-Если товар уже есть: "Товар {name} уже в магазине!"

3) Метод remove_item(name):
	-Удаляет товар если есть
	-Если нет: "Товара {name} нет в магазине"

4) Метод show_items():
	Товары в магазине "Магазинчик":
	1. Хлеб - 50 руб.
	2. Молоко - 70 руб.
	Всего товаров: 2

5)Метод total_value():
	-Возвращает общую стоимость всех товаров (сумма цен)

Тестовый код:
shop = Shop("Магазинчик")
shop.add_item("Хлеб", 50)
shop.add_item("Молоко", 70)
shop.add_item("Хлеб", 60)  # Уже есть!

shop.show_items()
print(f"Общая стоимость товаров: {shop.total_value()} руб.")

shop.remove_item("Молоко")
shop.show_items()

print(f"Новый total: {shop.total_value()} руб.")

Ожидаемый вывод:
Товар {name} уже в магазине!

Товары в магазине "Магазинчик":
1. Хлеб - 50 руб.
2. Молоко - 70 руб.
Всего товаров: 2
Общая стоимость товаров: 120 руб.

Товары в магазине "Магазинчик":
1. Хлеб - 50 руб.
Всего товаров: 1
Новый total: 50 руб.

Подсказки:
self.items — список словарей [{"name": "...", "price": ...}, ...]
Для поиска товара: цикл for item in self.items
item["name"] == name для сравнения
Сумма: sum(item["price"] for item in self.items)'''

class Shop:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items or {}  #  Новый словарь для каждого объекта
    
    def add_item(self, name, price):
        if name in self.items:
            print(f'Товар {name} уже в магазине!')
        else:
            self.items[name] = price

    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
        else:
            print(f'Товара {name} нет в магазине')

    def show_items(self):
        n = len(self.items)
        y = 1
        print('Товары в магазине "Магазинчик":')
        for key in self.items:
              print(f'{y}. {key} - {self.items[key]} руб.') 
              y += 1     
        print(f'Всего товаров: {n}')

    def total_value(self): # cумма товаров
        return sum(self.items[key] for key in self.items)
        
    
shop = Shop("Магазинчик")
shop.add_item("Хлеб", 50)
shop.add_item("Молоко", 70)
shop.add_item("Хлеб", 60)  # Уже есть!
print('')
shop.show_items()
print(f"Общая стоимость товаров: {shop.total_value()} руб.")
print('')
shop.remove_item("Молоко")
shop.show_items()
print('')
print(f"Новый total: {shop.total_value()} руб.")

