import yaml
import paramiko

def send_command_to_device(device, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=device['host'],
            username=device['username'],
            password=device['password'],
            timeout=device.get('timeout', 10)
        )
        stdin, stdout, stderr = client.exec_command(command)
        
        output = stdout.read().decode()
        error_output = stderr.read().decode()
        
        # Если есть ошибки в stderr (например, неверная команда), возвращаем их
        if error_output:
            return f"Ошибка команды '{command}':\n{error_output}"
        
        return output
    except TimeoutError:
        print(f'Превышено время ожидания соединения {device["host"]}')
    except paramiko.ssh_exception.AuthenticationException:
        print(f'Ошибка аутентификации для {device["host"]} (неверный логин/пароль)')
    except Exception as e:
        print(f'Не удалось подключиться к {device["host"]}: {e}')
    finally:
        if client.get_transport() and client.get_transport().is_active():
            client.close()
    return None

if __name__ == "__main__":
    try:
        with open("devices_2.yaml") as f:
            devices = yaml.safe_load(f)
    except FileNotFoundError:
        print("Файл devices_2.yaml не найден.")
        exit(1)
    
    command = ['show', 'show version']
    
    for device in devices:
        results = []
        print(f"Подлючение к {device['host']}... ")
        
        for cmd in command: # перебираем команды
            result = send_command_to_device(device, cmd)
            if result is not None:
                results.append(f"=== Команда: {cmd} ===")
                results.append(result)
                results.append('')
        
        # Заголовок добавляем один раз, если есть хоть какой-то результат
        if results:
            results.insert(0, f"--- Конфигурация устройства {device['host']} ---")
            
        #сохранение каждого устройства в отдельный файл
        filename = f"test_{device['host']}.txt"
        print(f'Сохранение конфигурации в файл "{filename}"...')
        try:    
            with open(filename, 'w', encoding='utf-8') as file_out:  
                file_out.write('\n'.join(results)) 
        except OSError as e: # Если запись в файл не удалась (например, нет прав), выводим в консоль
            print(f'Не удалось сохранить конфигурацию {device["host"]}: {e}')
