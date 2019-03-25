from threading import Thread
import time

def contador(nome, segundos, intervalo):
    while segundos:
        print("%s: %s" % (nome, segundos))
        time.sleep(intervalo / 1000.0)
        segundos -= 1

t1 = ('Iniciando contador 1 ("5 Segundos")', \
    Thread(target=contador, args=("5 Segundos", 5, 1000)))
t2 = ('Iniciando contador 2 ("A")', \
    Thread(target=contador, args=("A", 15, 300)))

threads = [t2,t1]

for msg, thread in threads:
    print(msg)
    thread.start()
