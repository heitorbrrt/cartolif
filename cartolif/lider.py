from functools import wraps
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Jogador, Delegacao
from . import db

bp = Blueprint('lider', __name__, url_prefix='/lider')

# Decorator para verificar se o usuário é LIDER
def lider_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.cargo != 'LIDER':
            abort(403)
        if not current_user.delegacao:
            flash('Você não é líder de nenhuma delegação.', 'error')
            return redirect(url_for('routes.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@lider_required
def index():
    # O decorator já garante que current_user.delegacao existe
    delegacao = current_user.delegacao
    return render_template('lider/index.html', delegacao=delegacao)

@bp.route('/add_jogador', methods=['POST'])
@lider_required
def add_jogador():
    nome = request.form.get('nome')
    delegacao = current_user.delegacao

    if nome:
        novo_jogador = Jogador(nome=nome, delegacao=delegacao)
        db.session.add(novo_jogador)
        db.session.commit()
        flash(f'Jogador "{nome}" adicionado com sucesso!', 'success')
    else:
        flash('O nome do jogador não pode ser vazio.', 'error')
        
    return redirect(url_for('lider.index'))
