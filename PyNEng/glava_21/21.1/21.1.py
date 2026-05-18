"""
Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды sh ip int br с оборудования
и шаблоне templates/sh_ip_int_br.template.

"""
# from netmiko import ConnectHandler
import textfsm


def parse_command_output(template, command_output):

    # 1. Загружаем шаблон
    with open(template) as f:
        re_table = textfsm.TextFSM(f)

    # 2. Парсим текст с помощью шаблона
    structured_data = re_table.ParseText(command_output)
    print(re_table.header) # выводим заголовок
    
    return structured_data


if __name__ == "__main__":
    
    with open('21.1/output.txt', 'r') as file:
        output = file.read() # Читаем весь файл как одну строку
       
    result = parse_command_output("21.1/templates/sh_ip_int_br.template", output)
    
    for row in result:
        print(row)
        
# ['FastEthernet0/0', '192.168.2.77', 'up', 'up']
# ['FastEthernet1/0', '192.168.1.25', 'up', 'up']
# ['FastEthernet2/0', 'unassigned', 'administratively down', 'down']
# ['FastEthernet3/0', 'unassigned', 'administratively down', 'down']
