from functools import wraps
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Delegacao, User
from . import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator para verificar se o usuário é ADMIN
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.cargo != 'ADMIN':
            abort(403) # Erro de acesso proibido
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@admin_required
def index():
    delegacoes = Delegacao.query.order_by(Delegacao.nome).all()
    return render_template('admin/index.html', delegacoes=delegacoes)

@bp.route('/delegacao', methods=['POST'])
@admin_required
def add_delegacao():
    nome = request.form.get('nome')
    if nome:
        if Delegacao.query.filter_by(nome=nome).first():
            flash(f'A delegação "{nome}" já existe.', 'error')
        else:
            nova_delegacao = Delegacao(nome=nome)
            db.session.add(nova_delegacao)
            db.session.commit()
            flash(f'Delegação "{nome}" adicionada com sucesso!', 'success')
    else:
        flash('O nome da delegação não pode ser vazio.', 'error')
    return redirect(url_for('admin.index'))

@bp.route('/delegacao/<int:id>')
@admin_required
def manage_delegacao(id):
    delegacao = Delegacao.query.get_or_404(id)
    # Busca todos os usuários que não são admins para serem possíveis líderes
    usuarios = User.query.filter(User.cargo != 'ADMIN').order_by(User.nome).all()
    return render_template('admin/manage_delegacao.html', delegacao=delegacao, usuarios=usuarios)

@bp.route('/delegacao/<int:id>/assign_lider', methods=['POST'])
@admin_required
def assign_lider(id):
    delegacao = Delegacao.query.get_or_404(id)
    user_id = request.form.get('user_id')

    if not user_id:
        flash('Nenhum usuário selecionado.', 'error')
        return redirect(url_for('admin.manage_delegacao', id=id))

    novo_lider = User.query.get(user_id)
    if not novo_lider:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('admin.manage_delegacao', id=id))

    # Remove o cargo de LIDER do líder antigo, se houver
    if delegacao.lider and delegacao.lider != novo_lider:
        delegacao.lider.cargo = 'USER'

    # Atribui a delegação ao novo líder e atualiza seu cargo
    delegacao.lider = novo_lider
    novo_lider.cargo = 'LIDER'

    db.session.commit()
    flash(f'{novo_lider.nome} foi definido como líder da delegação {delegacao.nome}.', 'success')
    return redirect(url_for('admin.manage_delegacao', id=id))
