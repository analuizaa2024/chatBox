# importações importantes
from flask import Flask
from flask_restx import Api, Namespace

class Server:
    def __init__(self):
        self.app = Flask(__name__)

# Cria a instância da API RESTx e conecta ela à aplicação Flask.
        self.api = Api(self.app,
                    version='1.0',
                    title='API de mensagens',
                    description='Uma API de estudo, chat de mensagens',
                    doc='/docs')
        self.ns_mensagens = Namespace('mensagens', description='Operações relacionais ás mensagens')
        
        self.api.add_namespace(self.ns_mensagens)  # Adiciona o namespace mensagens à API principal.
    
    def run (self):
        self.app.run(debug=True)

    
server = Server()