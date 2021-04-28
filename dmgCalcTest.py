import math, random
import functions, classes

Alice = classes.Character('Alice', [28, 27, 9, 7, 11, 6, 8, 9])

Bill = classes.Character('Bill', [27, 20, 13, 6, 6, 6, 9, 8])

C = classes.Character('C', [28, 27, 9, 7, 11, 6, 8, 9])

chars = {'Alice':Alice,'Bill':Bill, 'C':C}

while True:
    if input("Stop?\n") == 'y':
        break
    if input("Edit?\n") == 'y':
        C.HP = int(input('HP?\n'))
        C.MP = int(input('MP?\n'))
        C.ATK = int(input('ATK?\n'))
        C.DEF = int(input('DEF?\n'))
        C.INT = int(input('INT?\n'))
        C.RES = int(input('RES?\n'))
        C.DEX = int(input('DEX?\n'))
        C.AGI = int(input('AGI?\n'))
    if input("Print?\n") == 'y':
        for i in chars.values():
            print(i.name)
            print(i.HP)
            print(i.MP)
            print(i.ATK)
            print(i.DEF)
            print(i.INT)
            print(i.RES)
            print(i.DEX)
            print(i.AGI)
    functions.dealBasicDamage(chars[input('Attacker?\n')],chars[input('Defender?\n')],[],input('Atk Type?\n'),0)
    for i in chars:
        print(chars[i].HP)
