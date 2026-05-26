from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    cargo = db.Column(db.String(20), nullable=False, default='USER') # Valores: 'USER', 'LIDER', 'ADMIN'

    # Relação: Um usuário pode ser líder de uma delegação
    delegacao = db.relationship('Delegação', back_populates='lider', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.nome}>'

class Delegacao(db.Model):
    __tablename__ = 'delegacoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    lider_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    lider = db.relationship('User', back_populates='delegacao')

    # Relação: Uma delegação tem muitos jogadores
    jogadores = db.relationship('Jogador', back_populates='delegacao', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Delegação {self.nome}>'

class Jogador(db.Model):
    __tablename__ = 'jogadores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    delegacao_id = db.Column(db.Integer, db.ForeignKey('delegacoes.id'), nullable=False)
    delegacao = db.relationship('Delegacao', back_populates='jogadores')

    def __repr__(self):
        return f'<Jogador {self.nome}>'
