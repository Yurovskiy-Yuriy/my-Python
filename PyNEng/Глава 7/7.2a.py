'''
Сделать копию скрипта задания 7.2.
Дополнить скрипт: Скрипт не должен выводить команды, в которых содержатся слова, кото-
рые указаны в списке ignore.
При этом скрипт также не должен выводить строки, которые начинаются на !.
Проверить работу скрипта на конфигурационном файле config_sw1.txt. Имя файла передает-
ся как аргумент скрипту.
Ограничение: Все задания надо выполнять используя только пройденные темы.

ignore = ["duplex", "alias", "configuration"]
...
'''
# ПЕРВЫЙ ВАРИАНТ:
'''
with open('config_sw1.txt') as f:
    for line in f:
        if line.startswith('!'):
            continue
        if 'duplex' in line or 'alias' in line or 'configuration' in line:
            continue
        print(line.rstrip())
'''       

# ВТОРОЙ ВАРИАНТ:    

ignore = ["duplex", "alias", "configuration"]
       
with open('config_sw1.txt', 'r') as f:   
    for line in f:
        if line.startswith('!'):
            continue
        
        # перебираем слова из ignore
        ignored = False   
        for word in ignore:
            if word in line:
                ignored = True
                break
        
        if not ignored:
            print(line.rstrip())
        

