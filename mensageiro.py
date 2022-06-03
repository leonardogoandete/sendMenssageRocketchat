import requests
import json

# Define o servidor do rocket
servidor_rocket = 'http://21.21.21.5:3000'
canais = ['canal1','canal2']
#mensagem='Boa tarde Pesso @all, Estamos fazendo um teste!'

#define o cabeçalho da requisição
headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

json_data = {
    'username': 'jubileu',
    'password': 'jubileu',
}

#envia a requisição
response = requests.post(
           servidor_rocket+'/api/v1/login', 
           headers=headers, 
           json=json_data
           );
# converte a resposta de bytes para um dicionário do Python
user = json.loads(response.content);

#guardo userId e token
userId = user['data']['userId'];
token =  user['data']['authToken'];

# enviar mensagem
# https://developer.rocket.chat/reference/api/rest-api/endpoints/team-collaboration-endpoints/chat-endpoints/postmessage#important

userHeaders = {
    'X-Auth-Token': token,
    'X-User-Id' : userId,
    'Content-Type' : 'application/json; charset=utf-8',
}

status = requests.post(
    url=servidor_rocket+'/api/v1/chat.postMessage',
    json= {'channel': canais, 'text': mensagem,},
    headers= userHeaders,
    timeout=1.5,
);
