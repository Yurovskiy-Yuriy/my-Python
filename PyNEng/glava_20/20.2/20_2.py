"""
Создать шаблон templates/cisco_router_base.txt.

В шаблон templates/cisco_router_base.txt должно быть включено содержимое шаблонов:
    * templates/cisco_base.txt
    * templates/alias.txt
    * templates/eem_int_desc.txt

При этом, нельзя копировать текст шаблонов.

Проверьте шаблон templates/cisco_router_base.txt, с помощью
функции generate_config из задания 20.1. Не копируйте код функции generate_config.

В качестве данных, используйте информацию из файла data_files/router_info.yml

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
    
    data_file = "20.2/data_files/router_info.yml"
    template_file = "20.2/templates/cisco_router_base.txt"
    
  
    with open(data_file) as f:
        data = yaml.safe_load(f)    
        
    print(generate_config(template_file, data))
    
    
# service timestamps debug datetime msec localtime show-timezone
# service timestamps log datetime msec localtime show-timezone
# service tcp-keepalives-in
# service tcp-keepalives-out
# service password-encryption
# hostname R1
# no ip domain lookup
# no ip http server
# no ip http secure-server
# line con 0
#  logging synchronous
#  history size 100
# line vty 0 4
#  logging synchronous
#  history size 100


# alias exec c conf t
# alias configure sh do sh
# alias exec top sh proc cpu sorted | excl 0.00%__0.00%__0.00%
# alias exec diff sh archive config differences nvram:startup-config system:running-config
# alias exec bri show ip int bri | exc unass
# alias exec id show int desc
# alias exec desc sh int desc | ex down
# alias exec ospf sh run | s ^router ospf


# event manager applet update-int-desc
#  event neighbor-discovery interface regexp .*Ethernet.* cdp add
#  action 1.0 cli command "enable"
#  action 2.0 cli command "config t"
#  action 3.0 cli command "interface $_nd_local_intf_name"
#  action 4.0 cli command "description To $_nd_cdp_entry_name $_nd_port_id"
#  action 5.0 syslog msg "Description for $_nd_local_intf_name changed to $_nd_cdp_entry_name $_nd_port_id"
#  action 6.0 cli command "end"
#  action 7.0 cli command "exit"
    