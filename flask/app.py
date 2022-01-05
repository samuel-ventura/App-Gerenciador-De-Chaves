from Emprestimo import Emprestimo
from Chaves import Chave
from Usuarios import Usuario
from database import db
from flask import Flask
from waitress import serve
from flask import render_template
from flask import request, url_for, redirect, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.sql import func
from flask_session import Session
from flask import session
import logging
import os
import hashlib
from datetime import datetime
import pytz
from formChave import ChaveForm
from formUsuario import UsuarioForm
from formEmprestimo import EmprestimoForm
from formLogin import LoginForm
from flask import make_response
import json
from flask_json import FlaskJSON, json_response

app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap(app)
CSRFProtect(app)
CSV_DIR = '/flask/'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_SSL_STRICT'] = False
Session(app)

FlaskJSON(app)

logging.basicConfig(filename=CSV_DIR + 'app.log', filemode='w',format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + CSV_DIR + 'bd.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def inicializar_bd():
    # db.drop_all()
    db.create_all()


@app.route('/')
def home():
    return(render_template('ladingpage.html'))

@app.route('/home')
def root():
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    return (render_template('index.html'))


@app.route('/usuario/login',methods=['POST','GET'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       #PROCESSAMENTO DOS DADOS RECEBIDOS
       usuario = request.form['usuario']
       senha = request.form['senha']
       senhahash = hashlib.sha1(senha.encode('utf8')).hexdigest()
       #Verificar se existe alguma linha na tabela usuários com o login e senha recebidos
       linha = Usuario.query.filter(Usuario.username==usuario,Usuario.senha==senhahash  ).all()
       if (len(linha)>0): #"Anota" na sessão que o usuário está autenticado
           session['autenticado'] = True
           session['usuario'] = linha[0].id
           flash(u'Usuário autenticado com sucesso!')
           return(redirect(url_for('root')))
   return (render_template('form.html',form=form,action=url_for('login')))
   

@app.route('/usuario/logout',methods=['POST','GET'])
def logout():
    session.clear()
    return(redirect(url_for('home')))


@app.route('/chave/cadastrar', methods=['POST', 'GET'])
def cadastrar_chave():
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    form = ChaveForm()
    if form.validate_on_submit():
        # PROCESSAMENTO DOS DADOS RECEBIDOS
        novaChave = Chave(nome=request.form['nome'])
        db.session.add(novaChave)
        db.session.commit()
        return(redirect(url_for('listar_chaves')))
    return (render_template('form.html', form=form, action=url_for('cadastrar_chave')))


@app.route('/chave/listar')
def listar_chaves():
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    chaves = Chave.query.order_by(Chave.id).all()
    return(render_template('chaves.html', chaves=chaves))


@app.route('/chave/remover/<id_chave>')
def remover_chave(id_chave):
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    id_chave = int(id_chave)
    chave = Chave.query.get(id_chave)
    db.session.delete(chave)
    db.session.commit()
    return (redirect(url_for('listar_chaves')))


@app.route('/usuario/listar')
def listar_usuarios():
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return(render_template('usuarios.html', usuarios=usuarios))


@app.route('/usuario/cadastrar', methods=['POST', 'GET'])
def cadastrar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        # PROCESSAMENTO DOS DADOS RECEBIDOS
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        senhahash = hashlib.sha1(senha.encode('utf8')).hexdigest()
        novoUsuario = Usuario(nome=nome, username=username,email=email, telefone=telefone, senha=senhahash)
        db.session.add(novoUsuario)
        db.session.commit()
        return(redirect(url_for('listar_usuarios')))
    return (render_template('form.html', form=form, action=url_for('cadastrar_usuario')))


@app.route('/usuario/remover/<id_usuario>')
def remover_usuario(id_usuario):
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    id_usuario = int(id_usuario)
    usuario = Usuario.query.get(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return (redirect(url_for('listar_usuarios')))


@app.route('/chave/emprestar', methods=['POST', 'GET'])
def emprestar_chave():
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    form = EmprestimoForm()
    chaves = Chave.query.filter(Chave.disponivel==True).order_by(Chave.nome).all()
    form.chave.choices = [(c.id, c.nome) for c in chaves]
    if form.validate_on_submit():
        # IMPLEMENTAÇÃO DO CADASTRO DO EMPRÉSTIMO
        nome = request.form['nome']
        chave = int(request.form['chave'])
        tz_BR = pytz.timezone('America/Sao_Paulo')
        datetime_BR = datetime.now(tz_BR)
        data_emprestimo = datetime_BR
        novoEmprestimo = Emprestimo(id_usuario=session['usuario'], id_chave=chave, nome_pessoa=nome, data_emprestimo=data_emprestimo)
        chaveAlterada = Chave.query.get(chave)
        chaveAlterada.disponivel = False
        db.session.add(novoEmprestimo)
        db.session.commit()
        return(redirect(url_for('listar_emprestimos')))
    form.chave.choices = [(c.id, c.nome) for c in chaves]
    return(render_template('form.html', form=form, action=url_for('emprestar_chave')))


@app.route('/chave/listar_emprestimos')
def listar_emprestimos():
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    emprestimos = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).all()
    return(render_template('emprestimos.html', emprestimos=emprestimos))


@app.route('/emprestimo/remover/<id_emprestimo>', methods=['GET', 'POST'])
def remover_emprestimo(id_emprestimo):
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    id_emprestimo = int(id_emprestimo)
    emprestimo = Emprestimo.query.get(id_emprestimo)
    id_chave = emprestimo.id_chave
    chave = Chave.query.get(id_chave)
    chave.disponivel = True
    db.session.delete(emprestimo)
    db.session.commit()
    return(redirect(url_for('listar_emprestimos')))


@app.route('/chave/devolver/<id_emprestimo>', methods=['GET','POST'])
def devolver_chave(id_emprestimo):
    if session.get('autenticado',False)==False:
       return (redirect(url_for('login')))
    id_emprestimo = int(id_emprestimo)
    emprestimo = Emprestimo.query.get(id_emprestimo)
    tz_BR = pytz.timezone('America/Sao_Paulo')
    datetime_BR = datetime.now(tz_BR)
    emprestimo.data_devolucao = datetime_BR
    chave = Chave.query.get(emprestimo.id_chave)
    chave.disponivel = True
    db.session.commit()
    return (redirect(url_for('listar_emprestimos')))

@app.route('/chave/ultimo_emprestimo/<nome>')
def ultimo_emprestimo_json(nome):
   chave = Chave.query.filter(Chave.nome==nome).first()
   if chave is not None:
       emprestimo = Emprestimo.query.filter(Emprestimo.id_chave==chave.id).order_by(Emprestimo.id.desc()).first()
       if emprestimo is not None:
           resultado = json_response(nome=emprestimo.nome_pessoa, data_emprestimo=emprestimo.data_emprestimo, data_devolucao=emprestimo.data_devolucao)
       else:
           resultado = json_response(situacao='Emprestimo Indisponivel') 
   
   else:
       resultado = json_response(situacao='Chave Indisponivel')      

   return(resultado)


@app.route('/chave/situacao/<nome>')
def chave_situacao(nome):
   chave = Chave.query.filter(Chave.nome==nome).first()
   if chave is not None:
       if chave.disponivel:
           resultado = json_response(situacao="DISPONIVEL")
       else:
           #Procurar pra quem está emprestada
           emprestimo = Emprestimo.query.filter(Emprestimo.id_chave==chave.id).order_by(Emprestimo.id.desc()).first()
           resultado = json_response(situacao="EMPRESTADA",nome=emprestimo.nome_pessoa)
   else:
       resultado = json_response(situacao=-1)

   return(resultado)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80, url_prefix='/app')
