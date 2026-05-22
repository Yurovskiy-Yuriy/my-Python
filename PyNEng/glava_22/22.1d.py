"""
Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


"""

from pprint import pprint


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

class Topology:
    def __init__(self, topology_dict):
        # сразу вызывается метод _normalize, который обрабатывает переданный словарь и сохраняет результат в self.topology
        self.topology_dict = topology_dict
        
    def delete_link(self, x, y):
        
        # Собираем ключи для удаления
        to_delete = []
        for key, value in self.topology_dict.items():  #  ("R1", "Eth0/0")    ("SW1", "Eth0/1")
            if (key == x and value == y) or (key == y and value == x):
                to_delete.append(key)  # вот тут нельзя удалить ключ, т.к. сейчас он в работе
            
           
        # Удаляем найденные ключи
        for key in to_delete:
            del self.topology_dict[key]
        
        if len(to_delete) == 0:
            print('Такого соединения нет')
        return None    
    
    def delete_node(self, x):
        
        # Собираем ключи для удаления
        to_delete = []
        for key, value in self.topology_dict.items():  #  ("R1", "Eth0/0")    ("SW1", "Eth0/1")
            if key[0] == x  or value[0] == x:
                to_delete.append(key)  # вот тут нельзя удалить ключ, т.к. сейчас он в работе
           
        # Удаляем найденные ключи
        for key in to_delete:
            del self.topology_dict[key]
            
        if len(to_delete) == 0:
            print('Такого соединения нет')
            
        return None
  
   
    def add_link(self, x, y):
        
        # Собираем ключи для удаления
        key_and_value = False
        key_or_value = False
        for key, value in self.topology_dict.items():  #  ("R1", "Eth0/0")    ("SW1", "Eth0/1")
            if (key == x and value == y) or (key == y and value == x):
                key_and_value = True
            elif (key == x and value != y) or (key != y and value == x) or (key != x and value == y) or (key == y and value != x):
                key_or_value = True
            
        if key_and_value == True:
            print('Такое соединение существует')  
        elif key_or_value == True:
            print('Соединение с одним из портов существует')
        elif key_and_value == False and  key_or_value == False:
            self.topology_dict[x] = y
            print('Новое соединение добавлено')

   
    def show_topology(self):
        pprint(self.topology_dict)
    

top = Topology(topology_example)

top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))  # Новое соединение добавлено
top.add_link(('R1', 'Eth0/0'), ('SW1', 'Eth0/1')) # Такое соединение существует
top.add_link(('SW1', 'Eth0/1'), ('R1', 'Eth0/0')) # Такое соединение существует
top.add_link(('SW8', 'Eth0/1'), ('R1', 'Eth0/0')) # Соединение с одним из портов существует

top.show_topology()
    

