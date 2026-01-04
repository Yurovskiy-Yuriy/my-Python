'''Вы, вероятно, знаете «лайк» систему из Facebook и других страниц. 
Люди могут «лайкать» сообщения в блогах, фотографии или другие предметы.
Мы хотим создать текст, который должен быть отображен рядом с таким пунктом.

Реализуйте функцию, которая принимает массив, содержащий имена людей, 
которые любят элемент. Он должен вернуть текст отображения, как показано в примерах:

[]                                -->  "no one likes this"
["Peter"]                         -->  "Peter likes this"
["Jacob", "Alex"]                 -->  "Jacob and Alex like this"
["Max", "John", "Mark"]           -->  "Max, John and Mark like this"
["Alex", "Jacob", "Mark", "Max"]  -->  "Alex, Jacob and 2 others like this"
'''
def likes(names):
    if names == []:
        return 'no one likes this'
    else:
        
        n = len(names)
        ferst = 0
        result = ""
        if n == 1:
            result += names[0] + ' likes this'
        elif n <= 3:
            while n > 1:
                result += names[ferst] + ', '
                ferst += 1
                n = n - 1
            result = result[:-2]
            result += ' and ' + names[-1]
            result += ' like this'
        else:
            while ferst <= 1:
                result += names[ferst] + ', '
                ferst += 1
                n = n - 1
            result = result[:-2]
            result += ' and ' + str(n) 
            result += ' others like this'
        
        return result

       
print(likes([]))
print(likes(["Peter"] ))
print(likes(["Jacob", "Alex"] ))
print(likes(["Max", "John", "Mark"] ))
print(likes(["Alex", "Jacob", "Mark", "Max"]))
print(likes(['Sylia Stingray', 'Nene Romanova', 'Galatea', 'Quincy Rosenkreutz', 'Daley Wong', 'Brian J. Mason', 'Linna Yamazaki', 'Priscilla S. Asagiri', 'Largo', 'Leon McNichol']))
print(likes(['Nene Romanova', 'Anri', 'Linna Yamazaki', 'Quincy Rosenkreutz', 'Nigel', 'Daley Wong', 'Sylvie']))

'''ДРУГИЕ ВАРИАНТЫ:

def likes(names):
    n = len(names)
    return {
        0: 'no one likes this',
        1: '{} likes this', 
        2: '{} and {} like this', 
        3: '{}, {} and {} like this', 
        4: '{}, {} and {others} others like this'
    }[min(4, n)].format(*names[:3], others=n-2)
    
def likes(names):
    if len(names) == 0:
        return "no one likes this"
    elif len(names) == 1:
        return "%s likes this" % names[0]
    elif len(names) == 2:
        return "%s and %s like this" % (names[0], names[1])
    elif len(names) == 3:
        return "%s, %s and %s like this" % (names[0], names[1], names[2])
    else:
        return "%s, %s and %s others like this" % (names[0], names[1], len(names)-2)   
    


def likes(names):
    match names:
        case []: return 'no one likes this'
        case [a]: return f'{a} likes this'
        case [a, b]: return f'{a} and {b} like this'
        case [a, b, c]: return f'{a}, {b} and {c} like this'
        case [a, b, *rest]: return f'{a}, {b} and {len(rest)} others like this'
'''