from flask import Flask
from flask import jsonify
from flask import request
import const 
import requests

app = Flask(__name__)

print("Servidor do Chat está pronto para uso...")

pontosEquipeAzul = 0
pontosEquipeVermelha = 0 

@app.route('/placarAtual',methods=['GET'])
def createEmp():
    global pontosEquipeAzul
    global pontosEquipeVermelha
    dados = {
    'nameUser': request.json['nameUser'],
    'pointsRed':pontosEquipeVermelha,
    'pointsBlue': pontosEquipeAzul,
    }
    ip = const.registry[request.json['nameUser']][0]
    port = const.registry[request.json['nameUser']][1]
    print("Devolvendo o Placar: Equipe Azul "+str(pontosEquipeAzul)+" X "+str(pontosEquipeVermelha)+" Equipe Vermelha")
    resposta = requests.get(ip+":"+str(port)+'/placarAtual', json = dados)
    return "ACK"


@app.route('/AtualizaPlacar',methods=['POST'])
def func():
    global pontosEquipeAzul
    global pontosEquipeVermelha
    dados = {
    'nameUser': request.json['nameUser'],
    'teamName': request.json['teamName'],
    'pointsRed':pontosEquipeVermelha,
    'pointsBlue': pontosEquipeAzul,
    'points': request.json['points'],
    }

    ip = const.registry[request.json['nameUser']][0]
    port = const.registry[request.json['nameUser']][1]
    print(ip+":"+str(port))
    if(request.json['teamName'] == 'Equipe Azul'):
        pontosEquipeAzul = request.json['points']
    elif(request.json['teamName'] == 'Equipe Vermelha'):
        pontosEquipeVermelha = request.json['points']
    else:
        print('Equipe Não Encontrada, favor verificar se a equipe está correta!!!')
    print("Atualização do Placar Feita com Sucesso para: Equipe Azul "+str(pontosEquipeAzul)+ " X "+str(pontosEquipeVermelha)+" Equipe Vermelha")
    resposta = requests.get(ip+":"+str(port)+'/placarAtual', json = dados)
    return "ACK"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)