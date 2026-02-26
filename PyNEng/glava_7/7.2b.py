'''Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода, скрипт
должен записать полученные строки в файл
Имена файлов нужно передавать как аргументы скрипту:
• имя исходного файла конфигурации
• имя итогового файла конфигурации
При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore и строки,
которые начинаются на „!“.
Ограничение: Все задания надо выполнять используя только пройденные темы.
ignore = ["duplex", "alias", "configuration"]'''

ignore = ["duplex", "alias", "configuration"]
config_sw2 = []
with open('config_sw1.txt') as f:
    for line in f:
        for x in ignore:
            if '!' not in line and x not in line:
                config_sw2.append(line)
                # config_sw2.append(line.rstrip())
            break
print(config_sw2)

with open(r'D:\new_config.txt', 'w') as file_out:  
          for line in config_sw2:
                 file_out.write(line)

print(f'Обработанный файл сохранён в new_config.txt !')

                 

       
