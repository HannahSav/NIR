# Created by Hannah at 13.06.2024 14:49

with open("text1.txt") as f:
    a = f.readlines()

with open('text2.txt', 'w') as f2:
    for c in a:
        c = c[2:]
        if len(c) > 0 and c[0] in '0123456789':
            c = c[1:]
        f2.write(c)