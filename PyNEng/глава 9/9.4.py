'''Создать функцию convert_config_to_dict, которая обрабатывает конфигурационный файл ком-
мутатора и возвращает словарь:
    • Все команды верхнего уровня (глобального режима конфигурации), будут ключами.
    • Если у команды верхнего уровня есть подкоманды, они должны быть в значении у соот-
        ветствующего ключа, в виде списка (пробелы в начале строки надо удалить).
    • Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком

У функции должен быть один параметр config_filename, который ожидает как аргумент имя
конфигурационного файла.

При обработке конфигурационного файла, надо игнорировать строки, которые начинаются
с «!», а также строки в которых содержатся слова из списка ignore. Для проверки надо ли
игнорировать строку, использовать функцию ignore_command.

Проверить работу функции на примере файла config_sw1.txt

Часть словаря, который должна возвращать функция (полный вывод можно посмотреть в
тесте test_task_9_4.py):
{
    "version 15.0": [],
    "service timestamps debug datetime msec": [],
    "service timestamps log datetime msec": [],
    "no service password-encryption": [],
    "hostname sw1": [],
    "interface FastEthernet0/0": [
        "switchport mode access",
        "switchport access vlan 10",
    ],
    "interface FastEthernet0/1": [
        "switchport trunk encapsulation dot1q",
        "switchport trunk allowed vlan 100,200",
        "switchport mode trunk",
    ],
    "interface FastEthernet0/2": [
        "switchport mode access",
        "switchport access vlan 20",
    ],
}
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ignore = ["duplex", "alias", "Current configuration"]


def ignore_command(command, ignore):
    # Функция проверяет содержится ли в команде слово из списка ignore.
    #     Возвращает:
    #         * True, если в команде содержится слово из списка ignore
    #         * False - если нет
    ignore_status = False
    for word in ignore:
        if word in command:
            ignore_status = True
    return ignore_status

def convert_config_to_dict(config_filename):   
    with open(config_filename, 'r') as file:
        lines = file.readlines()
      
    result = {}
    for key in lines:
        if ignore_command(key, ignore) == False and key[0] != '!':
            if key[0] != ' ':
                key = key.strip()
                result[key] = []
                command_key = key 
            else:
                key = key.strip()
                result[command_key].append(key)
    
    # for x, y in result.items():
    #     print(x, y)
    
    return result
        
print(convert_config_to_dict('d:/test/config_sw1.txt'))