from sqlalchemy.orm import backref
from database import db
from sqlalchemy.sql import func

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    nome_pessoa = db.Column(db.String(100),unique=False,nullable=True)
    id_chave = db.Column(db.Integer,db.ForeignKey('chave.id'))
    data_emprestimo = db.Column(db.DateTime,unique=False,nullable=False,default=func.now())
    data_devolucao = db.Column(db.DateTime,unique=False,nullable=True)