'''Создать функцию generate_topology_from_cdp, которая обрабатывает 
вывод команды show cdp neighbor из нескольких файлов и записывает 
итоговую топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
    • list_of_files - список файлов из которых надо считать вывод
        команды sh cdp neighbor
    • save_to_filename - имя файла в формате YAML, в который сохранится 
        топология.
        – значение по умолчанию - None. По умолчанию, топология 
        не сохраняется в файл
        – топология сохраняется только, если save_to_filename 
        как аргумент указано имя файла
        
Функция должна возвращать словарь, который описывает соединения между 
устройствами, независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
    {"R4": {"Fa 0/1": {"R5": "Fa 0/1"},
            "Fa 0/2": {"R6": "Fa 0/0"}},
    "R5": {"Fa 0/1": {"R4": "Fa 0/1"}},
    "R6": {"Fa 0/0": {"R4": "Fa 0/2"}}}
    
Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, 
а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
• sh_cdp_n_sw1.txt
• sh_cdp_n_r1.txt
• sh_cdp_n_r2.txt
• sh_cdp_n_r3.txt
• sh_cdp_n_r4.txt
• sh_cdp_n_r5.txt
• sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый 
словарь в файл topology.yaml.'''



import re
import os
import glob
import yaml

result = {} 

def generate_topology_from_cdp(list_of_files, save_to_filename):
    global result 
    for filename in list_of_files:  # перебираем файлы
        with open(filename) as f:
            
            # Извлекаем hostname из имени файла
            hostname = os.path.splitext(os.path.basename(filename))[0].split('_')[-1]

            #создаем пустой ключ, далее будем все в него добавлять
            result[hostname] = {}
            
            output = f.readlines()
            for line in output:
                match = re.match(r'(\w+)\s+(\S+\s\S+)\s+\d+\s+.+(\S+\s\S+)', line)
                if match:
                    device, sport, dport = match.groups()
                    dport_dict = {device : dport} # cоздаем словарь с именем соседа и его портом
                    sport_dict = {sport : dport_dict} # cоздаем словарь для нашего интерфейса
                    result[hostname].update(sport_dict)
    # print(result)
    with open(save_to_filename, 'w') as f:
        yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

                    

sh_version_files = glob.glob("sh_cdp*")
generate_topology_from_cdp(sh_version_files, "topology.yaml")

