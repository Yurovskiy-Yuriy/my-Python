"""
Скопировать класс Topology из задания 22.1 и изменить его.

Перенести функциональность удаления "дублей" в метод _normalize.
При этом метод __init__ должен выглядеть таким образом:

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
        
    def _normalize(self, topology_dict):
        normalized_topology  = {}
        
        for key, value in topology_dict.items():  #  ("R1", "Eth0/0")    ("SW1", "Eth0/1")
   
                if value not in normalized_topology or normalized_topology[value] != key:
                    normalized_topology[key] = value
           
        return normalized_topology
    
    def show_topology(self):
        pprint(self.topology)
    

top = Topology(topology_example)
top.show_topology()
    

