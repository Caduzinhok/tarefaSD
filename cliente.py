import sys
from flask import Flask
from flask import request
import const 
import requests
import threading

app = Flask(__name__)

consultaRealizada = False
pontosVermelho = 0
pontosAzul = 0

@app.route('/placarAtual',methods=['GET'])
def createEmp():
    global pontosAzul, pontosVermelho
    if(request.json['nameUser'] != ''):
        print(str("O jogo está com o Placar de: Equipe Azul " +  str(request.json['pointsBlue']) + " X "+ str(request.json['pointsRed'])+" Equipe Vermelha"))
        pontosVermelho = request.json['pointsRed']
        pontosAzul = request.json['pointsBlue']
    else:
        print("Mensagem de requisição para o saber o Placar falhou")
    return "ACK"

equipeModificada = ""
@app.route('/AtualizaPlacar',methods=['POST'])
def func():
    if(request.json['nameUser'] != ''):
        print(str("O Placar foi atualizado para: Equipe Azul " +  str(request.json['pointsBlue']) + " X "+ str(request.json['pointsRed'])+" Equipe Vermelha"))
    else:
        print("Mensagem da atualização do Placar falhou")
    return "Não Necessário","ACK"
me = str(sys.argv[1]) 

def sending():
    global consultaRealizada, pontosAzul, pontosVermelho
    while True:
        tipoReq = input("Digite 1 para consultar o placar e 2 para atualizar o placar\n")
        if(str(tipoReq) == '1'):
            data = {
            'nameUser':me,
            'ip':const.registry[me][0],
            }
            resposta = requests.get(const.CHAT_SERVER_HOST+":"+str(const.CHAT_SERVER_PORT)+'/placarAtual', json = data)
            if resposta.text != "ACK":
                print("Error: O servidor não aceitou a solicitação!!!")
            else:
                consultaRealizada = True
        elif(str(tipoReq) == '2'):
            if(consultaRealizada):
                team = input("Qual o nome da Equipe Deseja Atualizar o Placar? ('Equipe Azul' ou 'Equipe Vermelha'): \n")
                valorPlacar = input("Qual o novo placar da equipe?\n")
                boolAtualizar = True
                if(team == 'Equipe Azul'):
                    if(int(valorPlacar) < int(pontosAzul)):
                        print("O Valor do Placar não pode ser menor que o atual!!!")
                        boolAtualizar = False
                if(team == 'Equipe Vermelha'):
                    if(int(valorPlacar) < int(pontosVermelho)):
                        print("O Valor do Placar não pode ser menor que o atual!!!")
                        boolAtualizar = False

                data = {
                'teamName':team,
                'nameUser':me,
                'points': valorPlacar,
                'ip':const.registry[me][0],
                }
                if(boolAtualizar):
                    resposta = requests.post(const.CHAT_SERVER_HOST+":"+str(const.CHAT_SERVER_PORT)+'/AtualizaPlacar', json = data)
                    if resposta.text != "ACK":
                        print("Error: O servidor não aceitou a solicitação!!!")
            else:
                print("Primeiro é necessário consultar o placar!!!")
            consultaRealizada = False
        else:
            print("Operação não encontrada")
        

def receiving():
    app.run(host="0.0.0.0",port=const.registry[me][1])

if __name__ == '__main__':
    send = threading.Thread(target=sending)
    send.start()
    
    receive = threading.Thread(target=receiving)
    receive.start()
