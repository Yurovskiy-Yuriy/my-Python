'''Ваша задача - сортировать данную строку. Каждое слово в строке будет содержать одно число. 
Это число - позиция, которую слово должно иметь в результате.

Примечание: числа могут быть от 1 до 9. Таким образом, первое слово будет первым (а не 0).

Если строка ввода пуста, верните пустую строку. Слова в строке ввода будут содержать только 
действительные последовательные числа.
Примеры

"is2 Thi1s T4est 3a"  -->  "Thi1s is2 3a T4est"
"4of Fo1r pe6ople g3ood th5e the2"  -->  "Fo1r the2 g3ood 4of th5e pe6ople"
""  -->  ""
'''

def order(sentence):
    word = sentence.split(' ')
    len_ = len(word)
    n = 1
    result = ""
    while n <= int(len_):
        #result += list(filter(lambda x: str(n) in x), word)
        for x in word:            
            if str(n) in x:
                result += x + ' '
                break  
        n += 1          
    result = result[:-1]   
    return result      




print(order("is2 Thi1s T4est 3a")) # "Thi1s is2 3a T4est")
print(order("4of Fo1r pe6ople g3ood th5e the2")) # "Fo1r the2 g3ood 4of th5e pe6ople")
print(order("")) #"")