'''Ваша задача — написать функцию maskify, 
которая заменяет все символы, кроме последних четырех, на '#'.

Примеры (вход --> выход):
"4556364607935616" --> "############5616"
     "64607935616" -->      "#######5616"
               "1" -->                "1"
                "" -->                 ""

// "What was the name of your first pet?"
"Skippy" --> "##ippy"
"Nananananananananananananananana Batman!" --> "####################################man!"
'''

def maskify(cc):
    result = ""
    len_list = len(cc) - 4 # длина строки
    
    for x in cc:
        if len_list > 0:
            result += x.replace(x, '#')
            len_list = len_list - 1
        else:
            result += x               
    return result

print(maskify("4556364607935616"))
print(maskify("64607935616"))
print(maskify("1"))
print(maskify(""))
print(maskify("Skippy"))
print(maskify("Nananananana Batman!"))

    