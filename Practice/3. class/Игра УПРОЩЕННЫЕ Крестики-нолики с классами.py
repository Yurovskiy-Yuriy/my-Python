'''УПРОЩЕННЫЕ Крестики-нолики с классами
Точно такая же структура как Орел-решка!

Структура:
1) Класс Board (игровое поле):

	cells = ["1","2","3","4","5","6","7","8","9"]  # номера клеток
	current_player = "X"  # чей ход

2)Класс TicTacToe (игра):

	board
	play_round()
	show_stats()

Требования (5 шагов по 5 минут):
ШАГ 1: Класс Board

	__init__(): self.cells = ["1","2","3","4","5","6","7","8","9"]
	make_move(position, symbol): заменить cells[position-1] на "X"/"O"
	is_full(): все клетки заполнены?
	print_board(): 
	 1 | 2 | 3
	---------
	 4 | 5 | 6
	---------
	 7 | 8 | 9

ШАГ 2: Простая проверка победы

	check_winner(): 8 комбинаций (3 горизонтали, 3 вертикали, 2 диагонали)
	return "X" / "O" / None

ШАГ 3: TicTacToe

	__init__(): self.board = Board()
	play_round():
		1. Показать поле
		2. Спросить позицию (1-9)
		3. Поставить X
		4. Компьютер: random.choice(пустых клеток)
		5. Показать поле

Тест Шага 3:
game = TicTacToe()
game.play_round()

Ожидаемый вывод:
text
 1 | 2 | 3
---------
 4 | 5 | 6
---------
 7 | 8 | 9
Твой ход (1-9): 5
X поставил в 5

 1 | 2 | 3
---------
 4 | X | 6
---------
 7 | 8 | 9
O поставил в 3

 1 | 2 | O
---------
 4 | X | 6
---------
 7 | 8 | 9

План:
ШАГ 1: Board с print_board() + make_move()
ШАГ 2: check_winner()  
ШАГ 3: play_round() без проверки победы
ШАГ 4: Добавить check_winner() в play_round()
ШАГ 5: Цикл до победы/ничьей'''
import random

class Board:
    def __init__(self):
        self.cells = ['1','2','3','4','5','6','7','8','9']
        #self.full = ['0','1','2','3','4','5','6','7','8'] # пустые клетки
        self.full = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def is_full(self, position): # учет пустых клеток
        self.full.remove(position)
    
    def make_move(self, position, symbol): # меняем цифры на доске с учетом ходов
        self.cells[position - 1] = symbol
    
    def print_board(self):
        print(f' {self.cells[0]} | {self.cells[1]} | {self.cells[2]}')
        print('----------')
        print(f' {self.cells[3]} | {self.cells[4]} | {self.cells[5]}')
        print('----------')
        print(f' {self.cells[6]} | {self.cells[7]} | {self.cells[8]}')
        
class TicTacToe:
    def __init__(self):
        self.board = Board()

    def play_round(self):
        self.board.print_board()
        player_move =  input('Твой ход:')    # запрос хода у человека 
        while (player_move - 1) in self.board.full:
            player_move = input('Клетка занята, повтори ход: ')
        #computer_move = random.choice(self.board.full)  # ход компьютера
       

game = TicTacToe()
game.play_round()


a = ['1', '2', '3', '4', '5']
b = ['1', '2', '5']
if set(b).issubset(set(a)):
    print("Все элементы b есть в a")  # Truм