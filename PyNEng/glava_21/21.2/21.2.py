"""
Сделать шаблон TextFSM для обработки вывода sh ip dhcp snooping binding
и записать его в файл templates/sh_ip_dhcp_snooping.template

Вывод команды находится в файле output/sh_ip_dhcp_snooping.txt.

Шаблон должен обрабатывать и возвращать значения таких столбцов:
    * mac - такого вида 00:04:A3:3E:5B:69
    * ip - такого вида 10.1.10.6
    * vlan - 10
    * intf - FastEthernet0/10

Проверить работу шаблона с помощью функции parse_command_output из задания 21.1.
"""

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
    
    with open('21.2/sh_ip_dhcp_snooping.txt', 'r') as file:
        output = file.read() # Читаем весь файл как одну строку
       
    result = parse_command_output("21.2/templates/sh_ip_dhcp_snooping.template", output)
    
    for row in result:
        print(row)