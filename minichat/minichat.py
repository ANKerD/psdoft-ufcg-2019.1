# -*- coding: utf-8 -*-
# Anderson Kleber Dantas - 117110537
# anderson.dantas@ccc.ufcg.edu.br
import sys 
import socket
import time
from threading import Thread

port = int(sys.argv[1] if len(sys.argv) > 1 else 8998)
host = sys.argv[2] if len(sys.argv) > 2 else socket.gethostbyname(socket.gethostname())

allClients = {}

def publish(sender, msg):
    for userId, client in allClients.items():
        if sender != userId:
            client.sendall(msg.encode())

def leave(userId):
    msg = '%s saiu' % userId
    publish(userId, msg)

    allClients[userId].close()
    allClients.pop(userId)

def clientHandler(userId, client):
    welcome = 'Voce é o usuário número %d\n' % userId
    client.sendall(welcome.encode())

    msg = '%s entrou\n' % userId
    publish(userId, msg)

    while True:
        msg = client.recv(4096).decode()

        if not msg or ':bye' in msg: 
            leave(userId)
            break

        msg = '%d diz %s' % (userId, msg)
        publish(userId, msg)

def joinClinet(id, client):
    handler = Thread(target=clientHandler, args=(id, client))
    allClients[id] = client
    handler.start()

def runServer():
    nextId = 1
    with socket.socket() as server:

        server.bind((host, port))
        server.listen()
        print('Conexão estabelecida em %s:%s' % (host, port))
        while True:
            client, addr = server.accept()
            if client:
                joinClinet(nextId, client)
                nextId += 1

Thread(target=runServer).start()