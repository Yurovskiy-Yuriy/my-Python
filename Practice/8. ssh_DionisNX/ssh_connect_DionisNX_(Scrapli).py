import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliTimeout, ScrapliAuthenticationFailed

def send_command_to_device(device, command):
    conn = None # ИНИЦИАЛИЗАЦИЯ: создаем переменную до попытки подключения
    
    # Словарь параметров для подключения
    scrapli_device = {
        "host": device["host"],
        "auth_username": device["username"],
        "auth_password": device["password"],
        "auth_strict_key": False,  # Отключаем проверку SSH-ключа хоста
        "timeout_socket": device.get("timeout", 10),
        "timeout_transport": device.get("timeout", 10),
        # "platform": "linux",  # Dionis NX — Linux-based устройство
        "platform": "generic", # если "Scrapli Community platform 'linux` not found!""
        # "transport": "paramiko" # если "system transport is not supported on windows devices"
        
        # pip install ssh2-python
        "transport": "ssh2",      # если "Сделана попытка выполнить операцию на объекте, не являющемся сокетом (10038)"
    }

    try:
        # Создаем объект подключения
        conn = Scrapli(**scrapli_device)
        conn.open()

        # Отправляем команду
        response = conn.send_command(command)

        # Проверяем успешность выполнения команды
        if response.failed:
            return f"Ошибка команды '{command}':\n{response.result}"
        
        return response.result

    except ScrapliTimeout:
        print(f'Превышено время ожидания соединения {device["host"]}')
    except ScrapliAuthenticationFailed:
        print(f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)')
    except Exception as e:
        print(f'Не удалось подключиться к {device["host"]}: {e}')
    finally:
        # Закрываем соединение, если оно было открыто
        if conn and conn.transport.isalive():
            conn.close()
    return None

if __name__ == "__main__":
    try:
        with open("devices_2.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_2.yaml не найден.")
        exit(1)
    
    commands = ['show', 'show version']

    for device in devices:
        results = []
        print(f"Подключение к {device['host']}... ")
        
        for cmd in commands:
            result = send_command_to_device(device, cmd)
            if result is not None:
                results.append(f"=== Команда: {cmd} ===")
                results.append(result)
                results.append('')
        
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
            
        filename = f"test_{device['host']}.txt"
        print(f'Сохранение конфигурации в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e:
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')