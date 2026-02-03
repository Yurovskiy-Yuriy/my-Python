'''найти сумму элементов диагонали матрицы (слева сверху вправо вниз)'''\

matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
result = 0

for index, number in enumerate(matrix):
    result += number[index]
print(result)