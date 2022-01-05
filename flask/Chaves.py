from sqlalchemy.orm import backref
from database import db

class Chave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    emprestimos = db.relationship('Emprestimo',backref='chave',lazy=True)
