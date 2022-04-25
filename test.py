from threading import Thread

def func(p):
    t = 0
    while True:
        p += 1
        t += 1
        if t > 5000000:
            print(p)
            t = 0

a = Thread(target=func, args=(5, ))
a.start()
while True:
    x = input()
    print("!!", x)