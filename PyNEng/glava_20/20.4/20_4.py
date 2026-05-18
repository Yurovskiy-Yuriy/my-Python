"""
Создайте шаблон templates/add_vlan_to_switch.txt, который будет использоваться
при необходимости добавить VLAN на коммутатор.

В шаблоне должны поддерживаться возможности:
* добавления VLAN и имени VLAN
* добавления VLAN как access, на указанном интерфейсе
* добавления VLAN в список разрешенных, на указанные транки

Шаблон надо создавать вручную.

Если VLAN необходимо добавить как access, надо настроить и режим интерфейса
и добавить его в VLAN:
interface Gi0/1
 switchport mode access
 switchport access vlan 5

Для транков, необходимо только добавить VLAN в список разрешенных:
interface Gi0/10
 switchport trunk allowed vlan add 5

Имена переменных надо выбрать на основании примера данных,
в файле data_files/add_vlan_to_switch.yaml.


Проверьте шаблон templates/add_vlan_to_switch.txt на данных
в файле data_files/add_vlan_to_switch.yaml, с помощью функции generate_config
из задания 20.1.
Не копируйте код функции generate_config.

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
    
    data_file = "20.4/data_files/add_vlan_to_switch.yaml"
    template_file = "20.4/templates/add_vlan_to_switch.txt"
    
  
    with open(data_file) as f:
        data = yaml.safe_load(f)    
        
    print(generate_config(template_file, data))
    

# vlan 10
#  name Marketing


# interface Fa0/1
#  switchport mode access
#  switchport access vlan 10


# interface Fa0/23
#  switchport trunk allowed vlan add  10
# interface Fa0/24
#  switchport trunk allowed vlan add  10
