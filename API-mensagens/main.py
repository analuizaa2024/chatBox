import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.server.instance import server  # tras o instance para o main
import src.server.mensagens

if __name__ == '__main__':
    server.run()  #“Se este arquivo está sendo executado diretamente, então inicie o servidor da API.”