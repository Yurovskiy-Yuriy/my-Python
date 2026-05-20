import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def send_command_to_device(device, command):
    # Создаем словарь для подключения, совместимый с Netmiko
    netmiko_device = {
        'device_type': 'linux',  # Dionis NX — Linux-based устройство
        'host': device['host'],
        'username': device['username'],
        'password': device['password'],
        'timeout': device.get('timeout', 10),
    }

    try:
        # Устанавливаем соединение с устройством
        with ConnectHandler(**netmiko_device) as ssh:
            # Отправляем команду и получаем вывод
            output = ssh.send_command(command)
            return output
    except NetMikoTimeoutException:
        print(f'Превышено время ожидания соединения {device["host"]}')
    except NetMikoAuthenticationException:
        print(f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)')
    except Exception as e:
        print(f'Не удалось подключиться к {device["host"]}: {e}')
    return None

if __name__ == "__main__":
    try:
        with open("21.4/log/devices_cisco.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_cisco.yaml не найден.")
        exit(1)
    
    commands = ['show configuration']  # Список команд для выполнения

    for device in devices:
        results = []
        print(f"Подключение к {device['host']}... ")
        
        for cmd in commands:  # Перебираем команды
            result = send_command_to_device(device, cmd)
            if result is not None:
                results.append(f"=== Команда: {cmd} ===")
                results.append(result)
                results.append('')
        
        # Заголовок добавляем один раз, если есть хоть какой-то результат
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
            
        # Сохранение каждого устройства в отдельный файл
        filename = f"21.4/log/test_{device['host']}.txt"
        print(f'Сохранение конфигурации в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e:  # Если запись в файл не удалась (например, нет прав), выводим в консоль
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')