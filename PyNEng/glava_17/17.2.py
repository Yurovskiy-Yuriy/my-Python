'''В этом задании нужно:
    • взять содержимое нескольких файлов с выводом команды sh version
    • распарсить вывод команды с помощью регулярных выражений и получить информацию
        об устройстве
    • записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
    • ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
    • обрабатывает вывод, с помощью регулярных выражений
    • возвращает кортеж из трёх элементов:
        – ios - в формате «12.4(5)T»
        – image - в формате «flash:c2800-advipservicesk9-mz.124-5.T.bin»
        – uptime - в формате «5 days, 3 hours, 3 minutes»

У функции write_inventory_to_csv должно быть два параметра:
    • data_filenames - ожидает как аргумент список имен файлов с выводом sh version
    • csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в ко-
        торый будет записана информация в формате CSV

Функция write_inventory_to_csv записывает содержимое в файл, в формате CSV и ничего не
возвращает

Функция write_inventory_to_csv должна делать следующее:
    • обработать информацию из каждого файла с выводом sh version:
        – sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
    • с помощью функции parse_sh_version, из каждого вывода должна быть получена инфор-
        мация ios, image, uptime
    • из имени файла нужно получить имя хоста
    • после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы: hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое
списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.

import glob
sh_version_files = glob.glob("sh_vers*")
#print(sh_version_files)
headers = ["hostname", "ios", "image", "uptime"]
'''

# 1. Функция parse_sh_version

# Эта функция принимает одну строку — вывод команды sh version. С помощью регулярных выражений нужно извлечь:

#     версию IOS (например, 12.4(5)T),
#     имя файла образа (например, flash:c2800-advipservicesk9-mz.124-5.T.bin),
#     время работы устройства (например, 5 days, 3 hours, 3 minutes).

# 2. Функция write_inventory_to_csv

# Эта функция:

#     получает список имён файлов (data_filenames) и имя итогового CSV (csv_filename);
#     для каждого файла:
#         читает его содержимое;
#         вызывает parse_sh_version для получения ios, image, uptime;
#         извлекает имя хоста из имени файла (например, из sh_version_r1.txt — r1);
#         записывает строку в CSV.

import re
import os
import csv
import glob


def parse_sh_version(output):
    match = re.search(r"Cisco IOS Software, .*, Version (\S+),", output)
    ios = match.group(1) if match else None

    match = re.search(r"System image file is \"(.+?)\"", output)
    image = match.group(1) if match else None

    match = re.search(r"uptime is (.+)", output)
    uptime = match.group(1) if match else None

    return ios, image, uptime

def write_inventory_to_csv(data_filenames, csv_filename):
    data = ['hostname', 'ios', 'image', 'uptime']
    
    with open(csv_filename, 'w', newline='') as f:  # открываем файл для записи шапки
        writer = csv.writer(f)
        writer.writerow(data)
        
        for filename in data_filenames:  # перебираем файлы
            
            with open(filename) as f:
                output = f.read()

            ios, image, uptime = parse_sh_version(output)
            
            # Извлекаем hostname из имени файла
            hostname = os.path.splitext(os.path.basename(filename))[0].split('_')[-1]
            
            writer.writerow([hostname, ios, image, uptime]) # записываем в файл
        

sh_version_files = glob.glob("sh_vers*")
write_inventory_to_csv(sh_version_files, "routers_inventory.csv")