'''реализовать игру "Камень-Ножницы-Бумага"'''

def random_number():
    # Получаем текущую временную метку
    from time import time
    current_time = int(time())
    
    # Преобразуем её в диапазоне от 1 до 3
    return ((current_time  % 3) + 1)

choices = ['камень', 'ножницы', 'бумага']
player_choice = int(input('Ваш ход: '))
print(f'Компьютер выбрал {choices[random_number() - 1]}')
print(f'У вас {choices[player_choice - 1]}')

# не доделал