from flask import Flask
from waitress import serve
from flask import render_template
from flask import request,url_for,send_from_directory,redirect,flash,session
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import logging

app = Flask(__name__)
bootstrap = Bootstrap(app)
CSRFProtect(app)
CSV_DIR = '/flask/'

logging.basicConfig(filename=CSV_DIR + 'app.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

@app.route('/')
def root():
    return (render_template('index.html'))

@app.route('/chave/cadastrar')
def cadastrar_chave():
    return ("Nao implementado")

@app.route('/chave/listar')
def listar_chaves():
    return ("Nao implementado")

@app.route('/usuario/listar')
def listar_usuarios():
    return ("Nao implementado")

@app.route('/usuario/cadastrar')
def cadastrar_usuario():
    return ("Nao implementado")

@app.route('/chave/emprestar')
def emprestar_chave():
    return ("Nao implementado")

@app.route('/chave/listar_emprestimos')
def listar_emprestimos():
    return ("Nao implementado")

@app.route('/chave/devolver')
def devolver_chave():
    return ("Nao implementado")


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80, url_prefix='/app')
