"""
Создать шаблоны templates/gre_ipsec_vpn_1.txt и templates/gre_ipsec_vpn_2.txt,
которые генерируют конфигурацию IPsec over GRE между двумя маршрутизаторами.

Шаблон templates/gre_ipsec_vpn_1.txt создает конфигурацию для одной стороны туннеля,
а templates/gre_ipsec_vpn_2.txt - для второй.

Примеры итоговой конфигурации, которая должна создаваться на основе шаблонов в файлах:
cisco_vpn_1.txt и cisco_vpn_2.txt.

Шаблоны надо создавать вручную, скопировав части конфига в соответствующие шаблоны.

Создать функцию create_vpn_config, которая использует эти шаблоны
для генерации конфигурации VPN на основе данных в словаре data.

Параметры функции:
* template1 - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* template2 - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна возвращать кортеж с двумя конфигурациями (строки),
которые получены на основе шаблонов.

Примеры конфигураций VPN, которые должна возвращать функция create_vpn_config в файлах
cisco_vpn_1.txt и cisco_vpn_2.txt.
"""


from jinja2 import Environment, FileSystemLoader
import yaml
from pprint import pprint

def create_vpn_config(template1, template2, data):
    
    # Указываем, что шаблоны лежат в папке '.'
    env = Environment(loader=FileSystemLoader("."))
    
    # Загружаем шаблон из файла template внутри папки '.'
    templ_1 = env.get_template(template1)  
    templ_2 = env.get_template(template2) 
    
    return templ_1.render(data), templ_2.render(data)
    

if __name__ == "__main__":
    
    data = {
    "tun_num": 10,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252"
    }
    
    template_file_1 = "20.5/templates/gre_ipsec_vpn_1.txt"
    template_file_2 = "20.5/templates/gre_ipsec_vpn_2.txt"
    
    pprint(create_vpn_config(template_file_1, template_file_2, data))
    
    
#     ('crypto isakmp policy 10\n'
#  ' encr aes\n'
#  ' authentication pre-share\n'
#  ' group 5\n'
#  ' hash sha\n'
#  '\n'
#  'crypto isakmp key cisco address 192.168.100.2\n'
#  '\n'
#  'crypto ipsec transform-set AESSHA esp-aes esp-sha-hmac\n'
#  ' mode transport\n'
#  '\n'
#  'crypto ipsec profile GRE\n'
#  ' set transform-set AESSHA\n'
#  '\n'
#  'interface Tunnel 10\n'
#  ' ip address 10.0.1.1 255.255.255.252\n'
#  ' tunnel source 192.168.100.1\n'
#  ' tunnel destination 192.168.100.2\n'
#  ' tunnel protection ipsec profile GRE\n',
#  'crypto isakmp policy 10\n'
#  ' encr aes\n'
#  ' authentication pre-share\n'
#  ' group 5\n'
#  ' hash sha\n'
#  '\n'
#  'crypto isakmp key cisco address 192.168.100.1\n'
#  '\n'
#  'crypto ipsec transform-set AESSHA esp-aes esp-sha-hmac\n'
#  ' mode transport\n'
#  '\n'
#  'crypto ipsec profile GRE\n'
#  ' set transform-set AESSHA\n'
#  '\n'
#  'interface Tunnel 10\n'
#  ' ip address 10.0.1.2 255.255.255.252\n'
#  ' tunnel source 192.168.100.2\n'
#  ' tunnel destination 192.168.100.1\n'
#  ' tunnel protection ipsec profile GRE\n')