"""
Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm


def parse_output_to_dict(template, command_output):

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
    
    with open('21.1a/sh_ip_int_br.txt', 'r') as file:
        output = file.read() # Читаем весь файл как одну строку
       
    result = parse_output_to_dict("21.1a/templates/sh_ip_int_br.template", output)
    
    for row in result:
        print(row)


# {'intf': 'FastEthernet0/0', 'address': '15.0.15.1', 'status': 'up', 'protocol': 'up'}
# {'intf': 'FastEthernet0/1', 'address': '10.0.12.1', 'status': 'up', 'protocol': 'up'}
# {'intf': 'FastEthernet0/2', 'address': '10.0.13.1', 'status': 'up', 'protocol': 'up'}
# {'intf': 'FastEthernet0/3', 'address': 'unassigned', 'status': 'up', 'protocol': 'up'}
# {'intf': 'Loopback0', 'address': '10.1.1.1', 'status': 'up', 'protocol': 'up'}
# {'intf': 'Loopback100', 'address': '100.0.0.1', 'status': 'up', 'protocol': 'up'}