"""
Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt
и данных из файла data_files/for.yml.

Важный нюанс: надо получить каталог из параметра template и использовать его, нельзя
указывать текущий каталог в FileSystemLoader - то есть НЕ надо делать так FileSystemLoader(".").
Указание текущего каталога, сломает работу других заданий/тестов.
"""

from jinja2 import Environment, FileSystemLoader
import yaml


def generate_config(template, data):
    
    # Указываем, что шаблоны лежат в папке '.'
    env = Environment(loader=FileSystemLoader("."))
    
    # Загружаем шаблон из файла template внутри папки '.'
    templ = env.get_template(template)  
    
    return templ.render(data)
    

if __name__ == "__main__":
    
    data_file = "20.1/data_files/for.yml"
    template_file = "20.1/templates/for.txt"
    
  
    with open(data_file) as f:
        data = yaml.safe_load(f)    
        
    print(generate_config(template_file, data))
    
    
# hostname R3

# interface Loopback0
#  ip address 10.0.0.3 255.255.255.255


# vlan 10
#  name Marketing

# vlan 20
#  name Voice

# vlan 30
#  name Management


# router ospf 1
#  router-id 10.0.0.3
#  auto-cost reference-bandwidth 10000

#  network 10.0.1.0 0.0.0.255 area 0

#  network 10.0.2.0 0.0.0.255 area 2

#  network 10.1.1.0 0.0.0.255 area 0