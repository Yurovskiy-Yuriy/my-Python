import colorama
colorama.init()
from tabulate import tabulate

#проверка правильности ввода данных
while True:
    

    # Функция для проверки IP-адреса
    def is_valid_ip(ip_address):
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True

    # Функция для проверки длины маски
    def is_valid_mask(mask):
        if not mask.isdigit():
            return False
        num = int(mask)
        return 0 <= num <= 32

    # Основной цикл
    while True:
        network = input("Введите IP-адрес (например, 10.10.10.0/24) или префикс (например, 24): ").strip()

        # Проверка, введён ли только номер маски
        if network.isdigit():
            mask_length = int(network)
            if not is_valid_mask(str(mask_length)):
                print("\033[91mНеверная маска\033[0m\n")
                continue
            
            # Генерируем бинарную маску
            mask_binary = "1" * mask_length + "0" * (32 - mask_length)
            mask = [
                int(mask_binary[0:8], 2),
                int(mask_binary[8:16], 2),
                int(mask_binary[16:24], 2),
                int(mask_binary[24:32], 2)
            ]
            
            data = {
                "Параметр": ["Маска"],
                "Значение": [f"{mask[0]}.{mask[1]}.{mask[2]}.{mask[3]}"]
            }
            table = tabulate(data, headers='keys', tablefmt='grid')
            print(table)
            continue

        # Стандартная проверка формата IP/маска
        if '/' not in network:
            print("\033[91mНеверный формат. Используйте IP/маску.\033[0m\n")
            continue

        ip_str, mask_str = network.split('/')
        if not is_valid_ip(ip_str):
            print("\033[91mНеверный IP-адрес\033[0m\n")
            continue
        elif not is_valid_mask(mask_str):
            print("\033[91mНеверная маска\033[0m\n")
            continue

        # Конвертируем строку в числа
        ip_address = list(map(int, ip_str.split('.')))
        mask_length = int(mask_str)

        # Генерация бинарной маски
        mask_binary = "1" * mask_length + "0" * (32 - mask_length)

        # Перевод IP в двоичный вид
        ip_address_binary = ''.join([f"{octet:08b}" for octet in ip_address])

        # Вычисляем адрес сети и широковещательного адреса
        network_bin = ip_address_binary[:mask_length].ljust(32, '0')
        broadcast_bin = ip_address_binary[:mask_length].ljust(32, '1')

        # Преобразование в десятичные значения
        network_addr = [
            int(network_bin[0:8], 2),
            int(network_bin[8:16], 2),
            int(network_bin[16:24], 2),
            int(network_bin[24:32], 2)
        ]

        broadcast_addr = [
            int(broadcast_bin[0:8], 2),
            int(broadcast_bin[8:16], 2),
            int(broadcast_bin[16:24], 2),
            int(broadcast_bin[24:32], 2)
        ]

        # Минимальный и максимальный хосты
        first_host = None
        last_host = None
        if mask_length == 31:
            first_host = '.'.join(map(str, network_addr))
            last_host = '.'.join(map(str, broadcast_addr))
        elif mask_length == 32:
            first_host = '.'.join(map(str, network_addr))
            last_host = '.'.join(map(str, network_addr))
        else:
            first_host_octets = network_addr[:-1]
            first_host_octets.append(network_addr[-1]+1)
            first_host = '.'.join(map(str, first_host_octets))

            last_host_octets = broadcast_addr[:-1]
            last_host_octets.append(broadcast_addr[-1]-1)
            last_host = '.'.join(map(str, last_host_octets))

        # Количество хостов
        host_count = (2**(32-mask_length))-2 if mask_length < 31 else 2 if mask_length==31 else 1

        # Формируем данные для таблицы
        data = {
            "Параметры": ["Адрес сети", "Широковещательный адрес", "Первый хост", "Последний хост", "Маска", "Количество хостов"],
            "Значения": [
                ".".join(map(str, network_addr)),
                ".".join(map(str, broadcast_addr)),
                first_host,
                last_host,
                ".".join(map(str, map(lambda x: int(x, 2), [mask_binary[i:i+8] for i in range(0, 32, 8)]))),
                str(host_count)
            ]
        }

        # Таблица
        table = tabulate(data, headers='keys', tablefmt='grid')
        print(table)