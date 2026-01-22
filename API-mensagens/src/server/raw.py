from pymongo import MongoClient
from bson.objectid import ObjectId


connection_string = "mongodb+srv://AnaLuiza:AnaLuiza@cluster0.elo3l5s.mongodb.net/"
client = MongoClient(connection_string)
db_connection = client["ChatBot"]

print(db_connection)
print()
collection = db_connection.get_collection("mensagens")

print(collection)
print()

def listar_documentos():
 for documento in collection.find():
    print(documento)

def atualizar_por_id(id, novos_dados):
    resultado = collection.update_one({"_id": ObjectId(id)}, {"$set": novos_dados})
    if resultado.matched_count:
        print("Documento atualizado com sucesso.")
    else:
        print("Documento não encontrado.")


def remover_por_id(id):
    resultado = collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count:
        print("Documento removido com sucesso.")
    else:
        print("Documento não encontrado.")  


