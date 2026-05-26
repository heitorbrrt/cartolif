from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime

# Tabela de associação para a escalação (Muitos-para-Muitos)
escalacao = db.Table('escalacao',
    db.Column('time_fantasia_id', db.Integer, db.ForeignKey('times_fantasia.id'), primary_key=True),
    db.Column('jogador_id', db.Integer, db.ForeignKey('jogadores.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    cargo = db.Column(db.String(20), nullable=False, default='USER')
    delegacao = db.relationship('Delegacao', back_populates='lider', uselist=False)
    time_fantasia = db.relationship('TimeFantasia', back_populates='usuario', uselist=False, cascade="all, delete-orphan")
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    def __repr__(self): return f'<User {self.nome}>'

class Delegacao(db.Model):
    __tablename__ = 'delegacoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    lider_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    lider = db.relationship('User', back_populates='delegacao')
    jogadores = db.relationship('Jogador', back_populates='delegacao', cascade="all, delete-orphan")
    partidas_a = db.relationship('Partida', foreign_keys='Partida.delegacao_a_id', back_populates='delegacao_a', lazy='dynamic')
    partidas_b = db.relationship('Partida', foreign_keys='Partida.delegacao_b_id', back_populates='delegacao_b', lazy='dynamic')
    def __repr__(self): return f'<Delegação {self.nome}>'

class Jogador(db.Model):
    __tablename__ = 'jogadores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(20), nullable=False, default='Linha')
    delegacao_id = db.Column(db.Integer, db.ForeignKey('delegacoes.id'), nullable=False)
    delegacao = db.relationship('Delegacao', back_populates='jogadores')
    eventos = db.relationship('Evento', back_populates='jogador', cascade="all, delete-orphan")
    def __repr__(self): return f'<Jogador {self.nome} ({self.posicao})>'

class TimeFantasia(db.Model):
    __tablename__ = 'times_fantasia'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    usuario = db.relationship('User', back_populates='time_fantasia')
    jogadores_escalados = db.relationship('Jogador', secondary=escalacao, lazy='subquery', backref=db.backref('times_que_escalaram', lazy=True))
    def __repr__(self): return f'<TimeFantasia {self.nome}>'

class Partida(db.Model):
    __tablename__ = 'partidas'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delegacao_a_id = db.Column(db.Integer, db.ForeignKey('delegacoes.id'), nullable=False)
    delegacao_b_id = db.Column(db.Integer, db.ForeignKey('delegacoes.id'), nullable=False)
    placar_a = db.Column(db.Integer, default=0)
    placar_b = db.Column(db.Integer, default=0)
    finalizada = db.Column(db.Boolean, default=False)
    delegacao_a = db.relationship('Delegacao', foreign_keys=[delegacao_a_id], back_populates='partidas_a')
    delegacao_b = db.relationship('Delegacao', foreign_keys=[delegacao_b_id], back_populates='partidas_b')
    eventos = db.relationship('Evento', back_populates='partida', cascade="all, delete-orphan")
    def __repr__(self): return f'<Partida {self.delegacao_a.nome} vs {self.delegacao_b.nome}>'

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    partida_id = db.Column(db.Integer, db.ForeignKey('partidas.id'), nullable=False)
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=False)
    tipo_evento = db.Column(db.String(50), nullable=False) # 'GOL', 'MELHOR_DA_PARTIDA'
    partida = db.relationship('Partida', back_populates='eventos')
    jogador = db.relationship('Jogador', back_populates='eventos')
    def __repr__(self): return f'<Evento {self.tipo_evento} - {self.jogador.nome}>'
