print("🔥 mensagens.py carregado")
from flask import request
from flask_restx import reqparse, abort, Resource, fields
from src.server.instance import server
from src.server.raw import collection
from bson import ObjectId
from datetime import datetime
from src.app.config import get_embedding_function
from src.app.models.rag_model import RAGModel


DOC_DIR = "documents"
DB_DIR = "db"



# Acessar namespace e api criados no instance.py
ns = server.ns_mensagens
api = server.api



# MODELOS DO SWAGGER

# modelos de entrada
ask_input = ns.model("AskInput", {
    "user": fields.String(required=True),
    "msg": fields.String(required=True)
})

# Modelo padrão para mensagens
mensagem_model = ns.model('Mensagem', {
    'user': fields.String(required=True, description='Nome do usuário que envia a mensagem'),
    'msg': fields.String(required=True, description='Conteúdo da mensagem (pergunta ou resposta)'),
    'to': fields.String(required=True, description='Destinatário (pode ser o bot)'),
    'id': fields.String(description='ID da mensagem no banco'),
    'createdAt': fields.String(description='Data de criação da mensagem')
})



# Modelo para erros no Swagger
error_model = ns.model('Error', {
    'status': fields.String(description='Status (error)'),
    'message': fields.String(description='Descrição do erro')
})

# Função auxiliar para padronizar respostas de erro
def error_response(code, message):
    return {"status": "error", "message": message}, code

# Cria embeddings a partir do config centralizado
embedding_function = get_embedding_function()

# Instancia o modelo RAG
rag_model = RAGModel(db_path=DB_DIR, embedding_function=embedding_function)

# ROTAS PRINCIPAIS

@ns.route('/allMessages')
class Mensagens(Resource):

    # -------------------- GET --------------------
    @ns.marshal_list_with(mensagem_model)
    @ns.response(200, "Lista retornada com sucesso")
    @ns.response(500, "Erro interno", error_model)
    def get(self):
        """Listar todas as mensagens"""
        try:
            mensagens = list(collection.find({}).sort('createdAt', -1))  # Ordenar do mais recente para o mais antigo

            for m in mensagens:
                m["id"] = str(m.pop("_id"))

            return mensagens

        except Exception as e:
            return error_response(500, f"Erro ao buscar mensagens: {str(e)}")

    # -------------------- POST --------------------
    @ns.expect(mensagem_model)
    @ns.marshal_with(mensagem_model)
    @ns.response(201, "Mensagem criada")
    @ns.response(400, "Dados inválidos", error_model)
    @ns.response(500, "Erro interno", error_model)
    def post(self):
        """Adicionar uma nova mensagem"""
        try:
            nova = api.payload

            # Validar campos obrigatórios
            if not nova.get("user") or not nova.get("msg") or not nova.get("to"):
                return error_response(400, "Campos obrigatórios faltando: user, msg, to")

            # ADICIONA DATA PARA ORDENAR
            nova["createdAt"] = datetime.utcnow().isoformat()

            # Inserir no MongoDB
            resultado = collection.insert_one(nova)
            nova["id"] = str(resultado.inserted_id)

            return nova, 201

        except Exception as e:
            return error_response(500, f"Erro ao criar mensagem: {str(e)}")


# ROTAS COM ID — PUT e DELETE (caso queira editar ou excluir mensagens)

@ns.route('/<string:id>')
class Mensagem(Resource):

    # -------------------- PUT --------------------
    @ns.expect(mensagem_model)
    @ns.marshal_with(mensagem_model)
    def put(self, id):
        if not ObjectId.is_valid(id):
            return error_response(400, "ID inválido.")

        dados = api.payload

        try:
            resultado = collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": dados}
            )

            if resultado.matched_count == 0:
                return error_response(404, "Mensagem não encontrada.")

            dados["id"] = id
            return dados

        except Exception as e:
            return error_response(500, f"Erro ao atualizar: {str(e)}")

    # -------------------- DELETE --------------------
    @ns.response(200, "Mensagem deletada com sucesso")
    @ns.response(400, "ID inválido", error_model)
    @ns.response(404, "Mensagem não encontrada", error_model)
    @ns.response(500, "Erro interno", error_model)
    def delete(self, id):
        """Deletar uma mensagem"""
        if not ObjectId.is_valid(id):
            return error_response(400, "ID inválido.")

        try:
            resultado = collection.delete_one({"_id": ObjectId(id)})

            if resultado.deleted_count == 0:
                return error_response(404, "Mensagem não encontrada.")

            return {"status": "success", "id": id}

        except Exception as e:
            return error_response(500, f"Erro ao deletar mensagem: {str(e)}")


# -------------------- PERGUNTAS --------------------

@ns.route('/ask')
class RAGAsk(Resource):
    @api.expect(ask_input)
    @api.response(201, "Resposta do bot")
    def post(self):
        data = request.json
        user = data.get('user')
        msg = data.get('msg')

        if not user or not msg:
            return error_response(400, "Campos 'user' e 'msg' são obrigatórios.")

        try:
            # 1 Gera resposta com RAG
            resposta_bot = rag_model.get_rag_response(msg)

            # 2 Mensagem do usuário
            mensagem_usuario = {
                "user": user,
                "msg": msg,
                "to": "atendente",
                "createdAt": datetime.utcnow().isoformat()
            }

            result_user = collection.insert_one(mensagem_usuario)
            mensagem_usuario["id"] = str(result_user.inserted_id)

            # 3 Mensagem do bot
            mensagem_bot = {
                "user": "atendente",
                "msg": resposta_bot,
                "to": user,
                "createdAt": datetime.utcnow().isoformat()
            }

            result_bot = collection.insert_one(mensagem_bot)
            mensagem_bot["id"] = str(result_bot.inserted_id)

            # 4 Retorna as DUAS mensagens
            return {
                "userMessage": mensagem_usuario,
                "botMessage": mensagem_bot
            }, 201

        except Exception as e:
            return error_response(500, f"Erro ao processar pergunta: {str(e)}")