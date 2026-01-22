'''Камень-Ножницы-Бумага с классами
Создай игру против компьютера используя классы. Введет ООП в action!

Структура:
1) Класс Player:
	name, wins=0, losses=0, draws=0
	choose_move() → "rock", "paper", "scissors"
2) Класс Game:
	player, computer
	play_round(player_move)
	show_stats()

Требования:
Player:
	-__init__(name) — wins, losses, draws = 0

	- choose_move() — ВОЗВРАЩАЕТ ход игрока (input())

	- update_stats(result) — win/loss/draw


	"win" → wins += 1
	"loss" → losses += 1  
	"draw" → draws += 1

Game:
	-__init__(player_name) — создает Player + Computer

`	-get_winner(move1, move2) → ВОЗВРАЩАЕТ "win", "loss", "draw"

	- play_round():

	1.Игрок выбирает ход

	2.Компьютер случайно: random.choice(["rock", "paper", "scissors"])

	3.Определяет победителя

	4.Обновляет статистику ОБОИХ

	5.Выводит результат раунда

	- show_stats() — статистика игроков

Тест (5 раундов):

game = Game("Иван")
for _ in range(5):
    game.play_round()
    print()
game.show_stats()

Ожидаемый вывод раунда:
text
Твой ход (rock/paper/scissors): rock
Компьютер: scissors
Ты победил!

ИЛИ
Ничья!
ИЛИ  
Компьютер победил!

Ожидаемая статистика:
text
📊 Статистика:
Иван: Побед: 2 | Поражений: 2 | Ничьи: 1
Компьютер: Побед: 2 | Поражений: 2 | Ничьи: 1
Импорты:

import random'''

import random

class Player:
    def __init__(self, name): # храним имя игрока и его результаты
        self.name = name
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def choose_move(self):  # запрашиваем ход у игрока
        return input('Твой ход (rock/paper/scissors):')
    
    def update_stats(self, result): # обновляем статистику по результату игры
        if result == 'win':
            self.wins += 1
        elif result == 'loss':
            self.losses += 1
        elif result == 'draw':
            self.draws += 1

class Game:
    def __init__(self, name):
        self.player = Player(name) 

    def get_winner(self, player_move, computer_move):  # Метод определения победителя
        if (player_move == 'rock' and computer_move == 'paper') or (player_move == 'paper' and computer_move == 'scissors') or (player_move == 'scissors' and computer_move == 'rock'):
            return 'win'
        elif player_move == computer_move:
            return 'draw'
        else:
            return 'loss'

    def play_pound(self):
        player_move = self.player.choose_move()  # запрос хода у человека
        computer_move = random.choice(["rock", "paper", "scissors"])  # ход компьютера
        result = self.get_winner(player_move, computer_move) # определяем победителя
        self.player.update_stats(result) # Обновляет статистику 
        print(f'Компьютер: {computer_move}')
        if self.get_winner(player_move, computer_move) == 'win':
            print('🎉 Ты победил!')
        elif self.get_winner(player_move, computer_move) == 'loss':
            print("💻 Компьютер победил!")  
        elif self.get_winner(player_move, computer_move) == 'draw':
            print("🤝 Ничья!") 

    def show_stats(self):
       print("📊 Статистика:")
       print(f'{self.player.name}: Побед: {self.player.wins} | Ничьих: {self.player.draws}  | Поражений: {self.player.losses}')


game = Game('Иван')
for n in range(5):
    game.play_pound()
    print('')
game.show_stats()