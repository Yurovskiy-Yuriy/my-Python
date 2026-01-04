'''Напишите функцию, которая включает строку из 
одного или нескольких слов и возвращает одну и ту 
же строку, но со всеми словами, которые имеют пять
или более букв обратно (так же, как имя этой ката). 
Пройденные струны будут состоять только из букв и пробелов. 
Пространства будут включены только тогда, когда присутствует 
более одного слова.

Примеры:

"Hey fellow warriors"  --> "Hey wollef sroirraw" 
"This is a test"        --> "This is a test" 
"This is another test" --> "This is rehtona test"
'''

def spin_words(sentence):
    result = ""
    sentence = sentence.split(' ')
    for x in sentence:
        if len(x) >= 5:
            x = x[::-1]
            result += x + ' '
        else:
            result += x + ' '
    result = result[:-1]
    return result
        
  

print(spin_words("Hey fellow warriors"))
print(spin_words("This is a test"))
print(spin_words("This is another test"))
