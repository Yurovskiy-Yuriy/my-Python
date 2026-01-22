'''🎲 Задание: "Орел-решка" с классами
Простая игра "подбросить монетку"

Структура (аналог RPS):
1)Класс Player:
	name, correct_guesses=0, wrong_guesses=0
	guess() → "heads" или "tails" (input())

2)Класс CoinGame:

	player, computer (монетка)
	play_round()
	show_stats()

Требования:
Player:

	__init__(name) → correct_guesses=0, wrong_guesses=0
	guess() → input("Орел или решка? (heads/tails):")
	update_stats(result) → "correct" → correct_guesses += 1

CoinGame:

	__init__(player_name) → создает Player
	get_winner(player_guess, coin_result) → "correct" или "wrong"  
	play_round():
		1. Игрок: guess()
		2. Монетка: random.choice(["heads", "tails"])
		3. Результат
		4. Обновить статистику
show_stats() → красивая статистика

Тест (5 раундов):

game = CoinGame("Иван")
for _ in range(5):
    game.play_round()
    print()
game.show_stats()

Ожидаемый вывод:

Орел или решка? (heads/tails): heads
Монетка: heads
✅ Правильно!t

Орел или решка? (heads/tails): tails  
Монетка: heads
❌ Неправильно!

📊 Статистика:
Иван: Правильно: 3 | Неправильно: 2 '''

import random

class Player:
    def __init__(self, name):
        self.name = name
        self.correct_guesses = 0 
        self.wrong_guesses = 0

    def guess(self):
        return input('Орел или решка? (heads/tails):')
    
    def update_guesses(self, result):
        if result == 'correct':
            self.correct_guesses += 1
        elif result == 'wrong':
            self.wrong_guesses += 1
    
class CoinGame:

    def __init__(self, name):
        self.player = Player(name)

    def get_winner(self, player_move, coin):
        if player_move == coin:
            return 'correct'
        else:
            return 'wrong'

    def play_round(self):
        player_move = self.player.guess()
        coin = random.choice(["heads", "tails"])
        result = self.get_winner(player_move, coin)
        self.player.update_guesses(result)
        print(f'Монетка: {coin}')
        if result == 'correct':
            print('✅ Правильно!')
        elif result == 'wrong':
            print('❌ Неправильно!')
        
    def show_stats(self):
        print('📊 Статистика:')
        print(f'{self.player.name}: Правильно: {self.player.correct_guesses} | Неправильно: {self.player.wrong_guesses}')








game = CoinGame("Иван")
for _ in range(5):
    game.play_round()
    print()
game.show_stats()