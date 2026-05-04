'''
Условие задачи
Нужно реализовать функцию, принимающую список чисел.
Вывести число, которое встречается чаще всего. 
Максимальное число голосов всегда уникально.
'''

def vote(votes):
    a = set(votes) #{1, 2, 3}
    max_count = 0
    result = None

    for i in a:
        count = votes.count(i)
        if count > max_count:
            max_count = count
            result = i

    return result    

if __name__ == '__main__':
    print(vote([1,1,1,2,3]))
    print(vote([1,2,3,2,2]))
    print(vote([1,5,1,5,5]))