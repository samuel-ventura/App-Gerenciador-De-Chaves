from flask import Flask
from waitress import serve
from flask import render_template
from flask import request,url_for,redirect,flash,session
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import logging
import os

from formChave import ChaveForm
from formUsuario import UsuarioForm
from formEmprestimo import EmprestimoForm

app = Flask(__name__)
bootstrap = Bootstrap(app)
CSRFProtect(app)
CSV_DIR = '/flask/'

logging.basicConfig(filename=CSV_DIR + 'app.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + CSV_DIR + 'bd.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from database import db
db.init_app(app)


from Usuarios import Usuario
from Chaves import Chave
from Emprestimo import Emprestimo

@app.before_first_request
def inicializar_bd():
    #db.drop_all()
    db.create_all()

@app.route('/')
def root():
    return (render_template('index.html'))

@app.route('/chave/cadastrar',methods=['POST','GET'])
def cadastrar_chave():
    form = ChaveForm()
    if form.validate_on_submit():
        #PROCESSAMENTO DOS DADOS RECEBIDOS
        novaChave = Chave(nome=request.form['nome'])
        db.session.add(novaChave)
        db.session.commit()
        return(redirect(url_for('root')))
    return (render_template('form.html',form=form,action=url_for('cadastrar_chave')))

@app.route('/chave/listar')
def listar_chaves():
    chaves = Chave.query.order_by(Chave.nome).all()
    return(render_template('chaves.html',chaves=chaves))

@app.route('/usuario/listar')
def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return(render_template('usuarios.html',usuarios=usuarios))

@app.route('/usuario/cadastrar',methods=['POST','GET'])
def cadastrar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        #PROCESSAMENTO DOS DADOS RECEBIDOS
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        novoUsuario = Usuario(nome=nome,username=username,email=email,telefone=telefone,senha=senha)
        db.session.add(novoUsuario)
        db.session.commit()
        return(redirect(url_for('root')))
    return (render_template('form.html',form=form,action=url_for('cadastrar_usuario')))

@app.route('/chave/emprestar',methods=['POST','GET'])
def emprestar_chave():
    form = EmprestimoForm()
    chaves = Chave.query.order_by(Chave.nome).all()
    form.chave.choices = [(c.id,c.nome) for c in chaves]
    if form.validate_on_submit():
        #IMPLEMENTAÇÃO DO CADASTRO DO EMPRÉSTIMO
        nome = request.form['nome']
        chave = int(request.form['chave'])
        novoEmprestimo = Emprestimo(id_usuario=1,id_chave=chave,nome_pessoa=nome)
        db.session.add(novoEmprestimo)
        db.session.commit()
        return(redirect(url_for('root')))
    form.chave.choices = [(c.id,c.nome) for c in chaves]
    return(render_template('form.html',form=form,action=url_for('emprestar_chave')))

@app.route('/chave/listar_emprestimos')
def listar_emprestimos():
    emprestimos = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).all()
    return(render_template('emprestimos.html',emprestimos=emprestimos))

@app.route('/chave/devolver')
def devolver_chave():
    return ("Nao implementado")

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80, url_prefix='/app')
