# docker run --name rocketchat -p 3000:3000 --link db --env ROOT_URL=http://localhost --env MONGO_OPLOG_URL=mongodb://db:27017/local -d rocket.chat
import os
import sys
import requests
import json

ROCKET_SERVER = "21.21.21.3:3000"
if os.getenv('CANAIS_ROCKET') is not None:
  CANAIS = os.getenv('CANAIS_ROCKET')
else:
  CANAIS="canal-a,canal-b,canal-c"

def login():
    #envia a requisição
    response = requests.post(
            ROCKET_SERVER+'/api/v1/login', 
            headers= {'Content-Type': 'application/json; charset=utf-8'}, 
            json={'username': 'jubileu','password': 'jubileu'},
            );
    # converte a resposta de bytes para um dicionário do Python
    user = json.loads(response.content);
    #guardo userId e token
    userId = user['data']['userId'];
    token =  user['data']['authToken'];
    return userId,token

def enviaMensagem(canal,mensagem,usuario):
  if mensagem != None:
    resp = requests.post(
      url= ROCKET_SERVER+'/api/v1/chat.postMessage',
      json= {'channel': canal, 'text': mensagem},
      headers= {'X-Auth-Token': usuario[1], 'X-User-Id' : usuario[0], 'Content-Type' : 'application/json; charset=utf-8'}, timeout=1.5,
      );
    if resp.status_code == 200:  
      print("Enviando mensagem no canal: " + canal)

if __name__ == "__main__":
  try:
      usuario = login()
      if len(sys.argv) != 3 and len(sys.argv) != 2:
        sys.exit('Usage:  %s MENSAGEM\n\t%s CANAIS MENSAGEM\n\n\
          example: %s "Mensagem de teste!"\n\
              \t   %s "canal-a,canal-b" "Mensagem de teste"\n' % (sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0]))
      elif len(sys.argv) == 3:
        canais=sys.argv[1]
        mensagem=sys.argv[2]
        for canal in canais.split(","):
          enviaMensagem(canal,mensagem,usuario)
      
      elif len(sys.argv) == 2:
        mensagem=sys.argv[1]
        for canal in CANAIS.split(","):
          enviaMensagem(canal,mensagem,usuario)
      print("Mensagem: " + mensagem)
      
  except Exception as exc:
    print (exc)
