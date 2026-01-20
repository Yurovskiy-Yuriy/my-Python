''' Игровой инвентарь
Создай класс Inventory для хранения предметов персонажа в игре.
 Идеально для закрепления списков из словарей!

Требования:
1) __init__:
	-self.items = [] (пустой список предметов)

2) Каждый предмет — словарь:
	{"name": "Меч", "damage": 25, "weight": 3, "equipped": False}

3) add_item(name, damage, weight):
 	-Добавляет предмет если его нет
	-"Предмет {name} уже в инвентаре!"
4)equip_item(name):
	-Снимает с других предметов equipped=True
	-Одевает найденный предмет
	-"Одет {name}" или "Предмета нет"

5)unequip_item(name):
	-Снимает equipped=False
	-"Снят {name}" или "Предмет не надет"

6) show_inventory():

	🎒 Инвентарь:
	1. Меч (урон:25, вес:3) [⚔️ ОДЕТ]
	2. Щит (урон:0, вес:2) [ ]
	3. Зелье (урон:0, вес:0.5) [ ]
	Всего предметов: 3 (1 надет)

7) total_weight() → возвращает общий вес


Объяснение: "equipped": False — это флаг "надет/не надет".
                -True = предмет надет (оружие в руках, броня на персонаже)
                -False = предмет в инвентаре (лежит в рюкзаке)
Тест:
inv = Inventory()
inv.add_item("Меч", 25, 3)
inv.add_item("Щит", 0, 2)
inv.add_item("Меч", 30, 4)  # Уже есть!

inv.show_inventory()

inv.equip_item("Меч")
inv.equip_item("Щит")  # Снимает меч, одевает щит
inv.show_inventory()

print(f"Вес инвентаря: {inv.total_weight()}")

Ожидаемый вывод:
Предмет Меч уже в инвентаре!

🎒 Инвентарь:
1. Меч (урон:25, вес:3) [ ]
2. Щит (урон:0, вес:2) [ ]
Всего предметов: 2 (0 надет)

Одет Щит
🎒 Инвентарь:
1. Меч (урон:25, вес:3) [ ]
2. Щит (урон:0, вес:2) [⚔️ ОДЕТ]
Всего предметов: 2 (1 надет)

Вес инвентаря: 5.0'''

class Inventory:
    def __init__(self):
        self.items = [] # пустой список предметов
    
    def add_item(self, name, damage, weight): 
        for x in self.items:
            if name.lower() in x['name'].lower():
                print(f'Предмет {name} уже в инвентаре!')
                return
        #new_items = {"name": name, "damage": damage, "weight": weight, "equipped": False}
        #self.items.append(new_items)
        self.items.append({"name": name, "damage": damage, "weight": weight, "equipped": False})
    
    def equip_item(self, name): # одеваем пердмет, всегда оставляет ТОЛЬКО 1 предмет надетым. 🗡️или🛡️
        for x in self.items:
            if name.lower() in x['name'].lower() and x['equipped'] == True:
                print(f'Предмет {name} уже был одет!')
                return
            elif name.lower() in x['name'].lower():
                x['equipped'] = True
                print(f'Предмет {name} успешно одет!')


        for x in self.items:
            if name.lower() not in x['name'].lower() and x['equipped'] == True:
                x['equipped'] = False
                print(f'Предмет {x['name']} снят!')

        
    
    def unequip_item(self, name): # снимаем данный инвентарь
         for x in self.items:
            if name in x['name']:
                if x['equipped'] == False:
                    print(f'Предмет {name} уже был снят!')
                    return
                x['equipped'] = False 
                print(f'Предмет {name} успешно снят!')
    
    def total_weight(self):
        return sum(x['weight'] for x in self.items)
    
    def show_inventory(self):
        y = 0
        z = 0
        print('🎒 Инвентарь:')
        for x in self.items:
            y += 1
            if x['equipped'] == True:
                eq = 'ОДЕТ'
                z +=1
            else:
                eq = ' '
            print(f'{y}. {x['name']} (урон:{x['damage']}, вес: {x['weight']}) [{eq}]')
        print(f'Всего предметов: {y} ({z} надет)')

inv = Inventory()
inv.add_item("Меч", 25, 3)
inv.add_item("Щит", 0, 2)
inv.add_item("Меч", 30, 4)  # Уже есть!
inv.add_item("Копье", 15, 1)
print('')
inv.show_inventory()
print('')
inv.equip_item("Меч")
print('')
inv.equip_item("Меч")
print('')
inv.equip_item("Щит")  # Снимает меч, одевает щит
print('')
inv.equip_item("Меч")
print('')
inv.equip_item("Меч")
print('')
inv.show_inventory()
print('')
inv.unequip_item("Меч") # Снимаем
inv.unequip_item("Меч") # Снимаем
inv.show_inventory()
print('')
inv.equip_item("Меч")
inv.show_inventory()
print(f"Вес инвентаря: {inv.total_weight()}")

 