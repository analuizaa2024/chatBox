from flask import Flask
from flask_restx import Api, Namespace
from flask_cors import CORS   

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        # CORS GLOBAL (UMA ÚNICA VEZ)
        CORS(self.app)

        self.api = Api(
            self.app,
            version='1.0',
            title='API de mensagens',
            description='Uma API de estudo, chat de mensagens',
            doc='/docs'
        )

        self.ns_mensagens = Namespace(
            'mensagens',
            description='Operações relacionais às mensagens'
        )
        
        self.api.add_namespace(self.ns_mensagens)
    
    def run(self):
     self.app.run(host="0.0.0.0", port=5000, debug=True)

server = Server()