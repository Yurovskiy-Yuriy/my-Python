'''Создать функцию write_last_log_to_csv.

Аргументы функции:
    • source_log - имя файла в формате csv, из которого читаются данные 
        (пример mail_log.csv)
    • output - имя файла в формате csv, в который будет записан результат
    
Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом,
email пользователь менять не может,только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv
файл. В файле output первой строкой должны быть заголовки столбцов, такие
же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо 
записать только ее. Для некоторых пользователей есть несколько записей с
разными именами. Например пользователь с email c3po@gmail.com несколько
раз менял имя:
    C=3PO,c3po@gmail.com,16/12/2019 17:10
    C3PO,c3po@gmail.com,16/12/2019 17:15
    C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - 
самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime -
она конвертирует строку с датой в формате 11/10/2019 14:05 в объект 
datetime. Полученные объекты datetime можно сравнивать между собой. 
Вторая функция convert_datetime_to_str делает обратную операцию
- превращает объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать 
не обязательно.

    import datetime
    
    def convert_str_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

    
    def convert_datetime_to_str(datetime_obj):
    """
     Конвертирует объект datetime в строку с датой в формате 11/10/2019 14:05
    """
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")'''
    
import datetime
import csv

# Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
def convert_str_to_datetime(datetime_str):
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

# Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
def convert_datetime_to_str(datetime_obj):
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")

def write_last_log_to_csv(log, output=None):
    result = [] # Список для хранения финальных строк
  
    with open(log, encoding='utf-8') as f:
        reader = csv.reader(f) 
        headers = next(reader)  # Сохраняем шапку
        result.append(headers)   #  добавляем шапку в финальный список
        duble = False
        
        for row in reader:  # читаем построчно лог
            index_line = 1 #  контролируем номер строки с которй работаем в result

            for lines in result[1:]:   # пеербираем построчно итоговый список (начиная со строки)

                if lines[1] == row[1]:  #если нашли пвтор строки
                    duble = True
                    lines_duble = index_line # запоминаем номер строки в result, где был повтор
                    break
                else:
                    duble = False
      
                index_line += 1
                
            if duble == False:
                result.append(row)
                print('строка добвлена')
            else:
                # # Сравниваем даты, чтобы найти самую свежую запись
                if convert_str_to_datetime(row[2]) > convert_str_to_datetime(result[lines_duble][2]):
                    del(result[lines_duble]) # удаляем дублирующую строку с наименьшим временем
                    result.append(row) # добавляем в список новую строку с наибольшим временем
    
    # Запись в файл
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(result)

write_last_log_to_csv('mail_log.csv', 'result_17.4.csv')


# result_17.4.csv:

# Name,Email,Last Changed
# BB-8,bb8@gmail.com,16/12/2019 17:20
# Chewie,chewbacca@gmail.com,10/02/2019 22:45
# Ben Solo,supreme_leader@gmail.com,21/12/2019 12:25
# C-3PO,c3po@gmail.com,16/12/2019 17:24
# R2D2,r2d2@gmail.com,23/10/2018 05:10
# Cara Dune,shocktrooper@gmail.com,11/10/2019 14:05
# D-O,do@gmail.com,15/12/2019 22:45
# Kuiil,i_have_spoken@gmail.com,20/04/2015 21:56
# Mandalorian,mandalorian176@gmail.com,10/11/2019 12:11