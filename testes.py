from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

# Suas credenciais de autenticação Twilio
account_sid = 'AC9aced17f811b471542706483e565c061'
auth_token = 'b70707aed364d9f04b152fb640064ba2'
client = Client(account_sid, auth_token)

@app.route("/whatsapp", methods=['GET', 'POST'])
def incoming_whatsapp():
    # Aqui você pode adicionar sua lógica para processar a mensagem recebida e decidir qual a próxima pergunta
    # Por enquanto, estou apenas respondendo com a mesma mensagem recebida
    incoming_msg = request.values.get('Body', '').lower()

    questions = {
        '1': 'Qual o seu nome?',
        '2': 'Qual a sua idade?',
        '3': {
            'text': 'Qual é a sua cidade preferida?',
            'options': ['São Paulo', 'Rio de Janeiro', 'Salvador'],
        },
    }

    resposta = MessagingResponse()
    msg = resposta.message()

    current_question = questions.get(str(incoming_msg), None)

    if current_question is not None:
        if isinstance(current_question, dict):
            # Se a pergunta é um dicionário, ela tem opções de botão
            # Cria os botões no Twilio Content Service
            url = 'https://content.twilio.com/v1/Content'
            data = {
                "friendly_name": "question_options",
                "language": "en",
                "variables": {},
                "types": {
                    "twilio/quick-reply": {
                        "body": current_question['text'],
                        "actions": [{"title": option, "id": option} for option in current_question['options']],
                    },
                    "twilio/text": {
                        "body": current_question['text'],
                    }
                }
            }
            headers = {'Content-Type': 'application/json'}
            requests.post(url, headers=headers, auth=(account_sid, auth_token), data=json.dumps(data))

            # Envie uma mensagem com o conteúdo criado
            msg.body(current_question['text'])
        else:
            # Se não, é apenas um texto normal
            msg.body(current_question)
    else:
        msg.body('Você digitou: ' + incoming_msg)

    return str(resposta)

if __name__ == "__main__":
    app.run(debug=True)
