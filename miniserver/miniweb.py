# -*- coding: utf-8 -*-
# Com a help de Flavio Roberto Farias
import socket
import sys

# interpreta a mensagem
def parse_request(mensagem):
    ret = {}
    try:
        req = mensagem.splitlines()
        
        verb, resource, protocol = req[0].split()
        ret = {
            'verb': verb,
            'resource': resource,
            'protocol': protocol
        }
        
        currentLine = 1
        
        headers = {}
        
        while req[currentLine].strip():
            line = req[currentLine]
            headerKey, headerValue = req[currentLine].split(':')
            headers[headerKey] = headerValue
            currentLine += 1
        ret['headers'] = headers

        bodySeparator = '\n'
        body = ''
        for i in range(currentLine, len(req)):
            body = body + bodySeparator + req[i]
        
        ret['body'] = body
        
        return ret
    except:
        return None

# converte os dicionários para http-like string
def mountResponse(res, req):
    firstLine = ' '.join([req['protocol'], res['status'], res['status-message']])
    
    ret = [firstLine]
    
    for key, value in res['headers'].items():
        ret.append(key + ':' + value)

    ret.append('\n'+res['body'])

    return '\n'.join(ret)

# Atende a requisição
def server(message):
    req = parse_request(message)
    res = {}
    if not req:
        req = {
            'protocol': 'HTTP/1.1'
        }
        res['headers'] = {
            'Host': socket.gethostbyname(socket.gethostname()),
            'Content-type': 'text/html; charset=utf-8',
        }
        statusCode = 400
        statusMessage = 'Bad-Request'
    else:
        okTxt = 'Este é o conteúdo do recurso "/" neste servidor.'

        res['headers'] = req['headers']
        res['headers']['Content-type'] = 'text/html; charset=utf-8'

        if req['verb'] == 'GET':
            if req['resource'] == '/':
                statusCode = 200
                statusMessage = 'OK'
                res['body'] = okTxt
            else:
                statusCode = 404
                statusMessage = 'Not-Found'
        else:
            statusCode = 405
            statusMessage = 'Method-Not-Allowed'
    if 'body' not in res:
        res['body'] = ''
    res['status'] = str(statusCode)
    res['status-message'] = statusMessage
    
    return mountResponse(res,req)

# porta default 9090 (ou o que vier na linha de comando)
porta = int(sys.argv[1] if len(sys.argv) > 1 else 9090)

# Leitura de dados
with socket.socket() as s:
    s.bind(('localhost', porta))
    s.listen()

    print('Aguardando conexões na porta %s...' % porta)
    while True:
        conexao, endereco = s.accept()
        with conexao:
            print('Conexão estabelecida de %s:%s' % endereco)
            cnt = 0
            req = ''
            while True:
                mensagem = conexao.recv(4096).decode('utf-8')
                cnt = cnt+1 if not len(mensagem.strip()) else 0
                if cnt == 3: break
                req = req + '\n' + mensagem
            
            conexao.sendall(server(req).encode('utf-8'))
