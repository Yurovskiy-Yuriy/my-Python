"""
Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* parse_command_dynamic - словарь атрибутов, в котором находятся такие
пары ключ-значение:
    * 'Command': команда
    * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""

# нужно создать функцию parse_command_dynamic, которая будет динамически выбирать
# шаблон для парсинга вывода команды, в зависимости от:

#     самой команды,
#     вендора оборудования.

# Для этого используется файл-индекс (по умолчанию index), где прописано, 
# какой шаблон (файл) использовать для какой команды и вендора. Шаблоны хранятся 
# в каталоге templates.

import textfsm


def parse_command_dynamic(template, command_output):

    # 1. Загружаем шаблон
    with open(template) as f:
        re_table = textfsm.TextFSM(f)

    # 2. Парсим текст с помощью шаблона
    structured_data = re_table.ParseText(command_output)
    
    # 3. Формируем список словарей
    result = []

    for item in structured_data:
        row = dict(zip(re_table.header, item)) # Создаём словарь

        result.append(row)
    
    return result
    

if __name__ == "__main__":
    
    # получаем необходимую команду
    print('1. show cdp neighbors detail\n2. show clock\n3. show ip interface brief\n4. show ip route ospf\n5. show version')
    dic_command = {1:'show cdp neighbors detail', 2:'show clock', 3:'show ip interface brief', 4:'show ip route ospf', 5:'show version',}
    print()
    number_command = int(input('Введите номер команды: '))
    
    while  number_command > 5 or number_command <= 0 :
        number_command = int(input('Неправильная команда, повотрите: '))
    command = dic_command[number_command]
    
    
    # получаем нужный шаблон .template в зависимости от команды
    with open('21.3/templates/index', 'r') as file:
        output = file.readlines()
        for out in output:
            out_split = out.split(',')
            if command in out_split[3]:
                file_templates = out_split[0]     # sh_cdp_n_det.template


    file_output = file_templates.replace('template', 'txt')  # sh_cdp_n_det.txt

    
    with open(f'21.3/output/{file_output}', 'r') as file:
        output = file.read() # Читаем весь файл как одну строку
       
    result = parse_command_dynamic(f'21.3/templates/{file_templates}', output)
    
    print()
    print('Результат: ')
    for row in result:
        print(row)
        
# 1. show cdp neighbors detail
# 2. show clock
# 3. show ip interface brief
# 4. show ip route ospf
# 5. show version

# Введите номер команды: 4

# Результат: 
# {'network': '10.0.0.0', 'mask': '8', 'distance': '110', 'metric': '20', 'nexthop': ['192.168.1.2']}
# {'network': '192.168.3.0', 'mask': '16', 'distance': '110', 'metric': '30', 'nexthop': ['192.168.1.3']}

