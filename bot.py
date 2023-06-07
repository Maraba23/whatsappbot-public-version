from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS
import os
import json
import requests
import base64
import datetime
import imghdr
import io

app = Flask(__name__)
CORS(app)

# Suas credenciais de autenticação Twilio
account_sid = 'Sua chave aqui'
auth_token = 'Sua chave aqui'
client = Client(account_sid, auth_token)

# Armazenar o estado do questionário e as respostas para cada número de telefone
states = {}
responses = {}

questions = {
    '1': 'Olá, seja bem vindo(a) ao formulário de denúncia de enchentes.\n\nQual o seu nome?',
    '2': 'Qual a sua idade?',
    '3': {
        'text': 'Em qual parte de Heliópolis ocorreu a enchente? Por favor, digite apenas o número.',
        'options': ['Barbinos', 'Fruta de Santo Amaro', 'Maciel Parente', 'Florestal', 'Mina', 'Flor do Pinhal', 'Itamarati', 'Triangulo', 'Imperador', 'João Lanhoso', 'Anny', 'Delamare', 'Presidente Wilson', 'Comandante Taylor'],
    },
    '4': {
        'text': 'Quando ocorreu a enchente? Por favor, digite apenas o número.',
        'options': ['Hoje', 'Ontem', 'Anteontem'],
    },
    '5' : 'Caso deseje, conte-nos um pouco sobre como foi o seu dia durante a enchente.\n\nCaso não queira, digite "Não".',
    '6': 'Por favor, envie um vídeo ou uma foto da enchente. Envie apenas um arquivo por vez.\n\nCaso deseje enviar mais de um, preencha novamente o formulário.',
}

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"

@app.route("/whatsapp", methods=['GET', 'POST'])
def incoming_whatsapp():
    from_number = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').lower()

    num_media = int(request.values.get('NumMedia', 0))
    media_items = [request.values.get(f'MediaUrl{i}', '') for i in range(num_media)]

    if from_number not in states:
        states[from_number] = 1
        responses[from_number] = {}
        resposta = MessagingResponse()
        msg = resposta.message()
        msg.body(questions[str(states[from_number])])
        return str(resposta)

    resposta = MessagingResponse()
    msg = resposta.message()

    current_question = questions[str(states[from_number])]

    if str(states[from_number]) in questions:
        if isinstance(current_question, dict):
            try:
                selected_option = int(incoming_msg)
                if selected_option < 1 or selected_option > len(current_question['options']):
                    raise ValueError
            except ValueError:
                msg.body("Resposta inválida. Por favor, selecione uma das opções listadas. Digite apenas o número.\n\n")
                question_text = current_question['text'] + "\n\nSelecione uma opção:"
                for i, option in enumerate(current_question['options'], 1):
                    question_text += f"\n{i} - {option}"
                msg.body(question_text)
                return str(resposta)
            else:
                responses[from_number][str(states[from_number])] = current_question['options'][selected_option-1]

        elif num_media > 0:
            responses[from_number][str(states[from_number])] = media_items
        else:
            responses[from_number][str(states[from_number])] = incoming_msg

    states[from_number] += 1

    if str(states[from_number]) in questions:
        next_question = questions[str(states[from_number])]
        if isinstance(next_question, dict):
            question_text = next_question['text'] + "\n\nSelecione uma opção:"
            for i, option in enumerate(next_question['options'], 1):
                question_text += f"\n{i} - {option}"
            msg.body(question_text)
        else:
            msg.body(next_question)
    else:
        #msg.body('Obrigado por realizar sua denúncia!\n\nAs informações foram enviadas a nossos voluntários.')
        for question, response in responses[from_number].items():
            if isinstance(response, list):
                encoded_media = []
                for url in response:
                    media_data = requests.get(url).content
                    encoded_media.append(base64.b64encode(media_data).decode())
                responses[from_number][question] = encoded_media

        # print(responses[from_number])
        print(responses[from_number]['6'][0])
        msg.body('Obrigado por realizar sua denúncia!\n\nAs informações foram enviadas a nossos voluntários.')
        send_to_backend(responses[from_number])
        del states[from_number]
        del responses[from_number]

    return str(resposta)

def send_to_backend(json_data):
    '''
    Json format to send to backend:
    {
    "nome": "Celão",
    "idade": 69,
    "dataEnchente": "2023-05-18",
    "local": "Insper",
    "relato": "a empadinha de camarão"
    "midiaType" : "jpeg" ou "mp4"
     }
    '''
    url = 'http://3.23.96.142:8080/denuncia'
    headers = {'Content-Type': 'application/json'}

    dataEnchente = datetime.datetime.now().strftime("%Y-%m-%d") if json_data['4'] == 'Hoje' else (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") if json_data['4'] == 'Ontem' else (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    # get the media type
    checkmedia(json_data)

    data = {
        'nome': json_data['1'],
        'idade': json_data['2'],
        'local': json_data['3'],
        'dataEnchente': dataEnchente,
        'relato': json_data['5'],
        'media': json_data['6'][0],
        'mediaType': json_data['mediaType'],
    }

    print(data)
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(r.status_code)
    print(r.text)

def checkmedia(json_data):
    string_base64 = json_data['6'][0]
    #if the string starts with /9j/ it is a jpeg 
    if string_base64.startswith('/9j/'):
        json_data['mediaType'] = '.jpeg'
    elif string_base64.startswith('AAAA'):
        json_data['mediaType'] = '.mp4'
    else:
        json_data['mediaType'] = 'https://youtu.be/dQw4w9WgXcQ'


if __name__ == "__main__":
    app.run()
