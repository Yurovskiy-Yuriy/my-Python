'''
Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации на
устройстве.
При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение
исключения.
Для проверки измените пароль на устройстве или в файле devices.yaml.
'''

from pprint import pprint
import yaml
from netmiko import ConnectHandler

from paramiko.ssh_exception import AuthenticationException, SSHException
from netmiko import NetMikoTimeoutException

def send_config_commands(device_params, commands):
    result = {}
    try:
        with ConnectHandler(**device_params) as ssh:
            ssh.enable() 
            output = ssh.send_command(commands)
            result[commands] = output
            
        return result
    
    except AuthenticationException as e:
        return {commands: f'Ошибка аутентификации: {e}'}
    except NetMikoTimeoutException as e:
        return {commands: f'Таймаут подключения: {e}'}
    except SSHException as e:
        return {commands: f'Ошибка SSH: {e}'}
    
# Файл devices.yaml содержит список словарей с параметрами устройств
if __name__ == "__main__":
    command = "sh ip int br"
    
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        
    for dev in devices:
        output = send_config_commands(dev, command)
        pprint(output)

    
