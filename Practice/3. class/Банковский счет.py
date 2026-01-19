'''Банковский счет
Создай класс BankAccount для моделирования банковского счета.

Требования:
1) __init__ принимает:
	-account_holder (владелец, строка)
	-initial_balance (начальный баланс, по умолчанию 0)

2) Метод deposit(amount):
	-Принимает сумму (положительное число)
	-Если сумма > 0: добавляет к балансу, выводит "Пополнено на {amount}. 	Баланс: {balance}"
	-Если сумма ≤ 0: "Сумма пополнения должна быть положительной!"

3) Метод withdraw(amount):
	-Если сумма > баланса: "Недостаточно средств!"
	-Если сумма ≤ 0: "Сумма снятия должна быть положительной!"
	-Иначе: вычитает сумму, выводит "Снято {amount}. Баланс: {balance}"

4) Метод get_balance():
	-Возвращает только число (не печатает!)

5) Метод show_info():
	Владелец: Иван Иванов
	Баланс: 5000.00 руб.

# Создай класс и протестируй:
account = BankAccount("Иван Иванов", 1000)
account.show_info()

account.deposit(500)
account.withdraw(200)
print(f"Баланс: {account.get_balance()}")  # Только число!

account.withdraw(2000)  # Недостаточно средств
account.deposit(-100)   # Отрицательная сумма


Ожидаемый вывод:
text
Владелец: Иван Иванов
Баланс: 1000.00 руб.

Пополнено на 500. Баланс: 1500.0
Снято 200. Баланс: 1300.0
Баланс: 1300.0
Недостаточно средств!
Сумма пополнения должна быть положительной!'''

class BankAccount:

    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
    
    def deposit(self, amount): # amount- сумма для пополнения
        if amount > 0:
            self.balance += amount
            print(f'Пополнено на {amount}. Баланс: {self.balance:.2f}')
        else:
            print('Сумма пополнения должна быть положительной!')

    def withdraw(self, amount): # amount- сумма для снятия
        if amount > self.balance:
            print('Недостаточно средств!')
        elif amount <= 0:
            print('Сумма снятия должна быть положительной!')
        else:
            self.balance -= amount
            print(f'Снято {amount}. Баланс: {self.balance:.2f}')
        
    def get_balance(self):
        return self.balance

    def show_info(self):
        print(f'Владелец: {self.account_holder}')
        print(f'Баланс: {self.balance:.2f}')


account = BankAccount("Иван Иванов", 1000)
account.show_info()
print('')
account.deposit(500)
account.withdraw(200)
print('')
print(f"Баланс: {account.get_balance()}")  # Только число!
print('')
account.withdraw(2000)  # Недостаточно средств
account.deposit(-100)   # Отрицательная сумма