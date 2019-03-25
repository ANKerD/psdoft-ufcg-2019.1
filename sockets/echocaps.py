import sys 
import socket

port = int(sys.argv[1] if len(sys.argv) > 1 else 8998)

with socket.socket() as server:
    host = socket.gethostbyname(socket.gethostname())
    server.bind((host, port))
    server.listen()
    print('Conexão estabelecida em %s:%s' % (host, port))
    client, addr = server.accept()
    with client:
        while True:
            msg = client.recv(4096)
            if not msg: break
            print('Recebi um %s' % msg)
            client.sendall(msg.upper())