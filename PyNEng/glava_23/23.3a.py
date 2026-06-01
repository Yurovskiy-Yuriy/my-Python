"""
В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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
        self.topology = self._normalize(topology_dict)
        self.index = 0 # индекс колличества списков в словаре
        self._items = list(self.topology.items()) # преобразуем в словарь


    
    def __iter__(self):
        return self    
    
    def __next__(self):
        
        if self.index < len(self._items):
            x = self._items[self.index] 
            self.index += 1
            return x
        else:
            raise StopIteration
            
        
        
    
    def _normalize(self, topology_dict):
        normalized_topology  = {}
        
        for key, value in topology_dict.items():  #  ("R1", "Eth0/0")    ("SW1", "Eth0/1")
   
                if value not in normalized_topology or normalized_topology[value] != key:
                    normalized_topology[key] = value
           
        return normalized_topology
    
    def show_topology(self):
        pprint(self.topology)
        
        
top = Topology(topology_example)
for link in top:
   print(link)
