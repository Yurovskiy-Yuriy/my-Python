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
'''

import random

class Board:
    def __init__(self):
        self.cells = ['1','2','3','4','5','6','7','8','9'] # визуальное отображение поля
        self.full = ['1','2','3','4','5','6','7','8','9'] # пустые клетки
        self.go_player = [] # все хода игрока
        self.go_computer = [] # все хода компьютера
        self.winner_list = ({'1','2','3'}, {'4','5','6'}, {'7','8','9'}, {'1','4','7'}, {'2','5','8'}, {'3','6','9'}, {'1','5','9'}, {'3','5','7'})

    def is_full(self, position): # учет пустых клеток
        self.full.remove(position)
    
    def make_move(self, position, symbol): # меняем цифры на доске с учетом ходов
        self.cells[int(position) - 1] = symbol
    
    def print_board(self):
        print(f' {self.cells[0]} | {self.cells[1]} | {self.cells[2]}')
        print('----------')
        print(f' {self.cells[3]} | {self.cells[4]} | {self.cells[5]}')
        print('----------')
        print(f' {self.cells[6]} | {self.cells[7]} | {self.cells[8]}')
              
class TicTacToe:
    def __init__(self):
        self.board = Board()
        self.end = False
  
    def winner(self, list_):   # проверка на победу или ничью
        for x in self.board.winner_list:
            if x.issubset(set(list_)):
                if list_ == self.board.go_player:
                    print('')
                    print("Ты победил!!!")
                    self.end = True                       
                elif list_ == self.board.go_computer:
                    print('')
                    print("Поражение!!! Победил компьютер")
                    self.end = True 
                elif len(self.board.full) == 0:
                    print('')
                    print("Ничья!!!")
                    self.end = True 
         
    def play_round(self):
        self.board.print_board()
        
        while self.end == False:
            print('')
            player_move =  input('Твой ход:')    # запрос хода у человека 
            while player_move not in self.board.full: # проверка правильности хода
                player_move = input('Клетка занята, повтори ход: ')
            
            self.board.make_move(player_move, 'X')  # ставим на доске 'X'
            self.board.full.remove(player_move) # удаляем эллемент из возможных следующих ходов
            self.board.go_player.append(player_move) # добавляем в список ход человека
            self.winner(self.board.go_player) # проверка на победу
            
            if self.end == True:
                self.board.print_board()
                break 
            
            computer_move = random.choice(self.board.full)  # ход компьютера
            
            self.board.make_move(computer_move, 'O') # ставим на доске 'O'
            self.board.full.remove(computer_move) # удаляем эллемент из возможных следующих ходов
            self.board.go_computer.append(computer_move) # добавляем в список ход компьютера
            self.winner(self.board.go_computer) # проверка на победу
            self.board.print_board()
        
game = TicTacToe()
game.play_round()