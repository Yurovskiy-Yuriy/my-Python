def rot13(message):
    result = ''
    for x in message:
        if ord(x) >= 110 and x.isalpha() == True:           # 'abcdefghijklm nopqrstuvwxyz'  от 97 до 122
            result += (str(chr(97 + ((ord(x) + 13) - 123))))
        elif 90 >= ord(x) >= 78:                            # 'ABCDEFGHIJKLM NOPQRSTUVWXYZ'  от 65 до 90
            result += (str(chr(65 + ((ord(x) + 13) - 91))))
        elif x.isalpha() == True:
            result += (str((chr(ord(x) + 13))))
        else:
            result += x
    return result