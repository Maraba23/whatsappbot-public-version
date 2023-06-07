# Whats app bot - Sprint 3

---

## Instalação

Para executar o bot siga o seguinte tutorial

1. Instale o `python` no seu computador

1. abra o terminal e digite `pip install -r requirements.txt`

1. Execute `python bot.py` no terminal

---

## Como usar



1. Crie uma conta na Twilio

1. Mude as credenciais no codigo em:
```python
# Suas credenciais de autenticação Twilio
account_sid = 'Sua chave aqui'
auth_token = 'Sua chave aqui'
```
- Troque para as suas credencias que iram aparecer após você conectar à sandbox

1. Apos criar a conta scaneie o qrcode para conectar seu celular ao sandbox

1. Crie uma conta em ngrok e execute o ngrok.exe (Isso vai servir para emular um deploy, mais duvidas sobre como realizar esse processo, siga esse [video](https://youtu.be/EeUdel2AJ5g))

1. Use o link presente no ngrok da sua aplicação na `sandbox settings -> When a message comes in` e coloque o metodo como `POST`

1. Apos isso, basta apenas mandar uma mensagem para o bot e ele estara pronto para rodar

