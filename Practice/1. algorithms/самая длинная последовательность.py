''' определить самую длинную последовательность одинаковых
символов подряд в строке и вернуть ее длину'''

string_seq = 'abbbcddddddddeeeeeffd'

result = 0
simbol = set(string_seq)
#print(simbol)
for x in simbol:
    #print(f'{x} -проверка')
    z = 0
    for y in string_seq:
        #print(y)
        if x == y:
            z += 1
            #print(z)
        else:
            if z > 0 and x != y:
                break
        if z > result:
            result = z
            result_2 = y
print(result_2, result)     
