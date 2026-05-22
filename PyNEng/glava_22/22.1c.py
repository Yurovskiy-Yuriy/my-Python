
"""
Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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

    
    def show_topology(self):
        pprint(self.topology_dict)
    

top = Topology(topology_example)
top.delete_node('SW1')
# top.delete_node('R1')

top.show_topology()
    

