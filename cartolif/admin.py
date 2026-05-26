from functools import wraps
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Delegacao, User, Partida, Evento, Jogador
from . import db
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.cargo != 'ADMIN':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@admin_required
def index():
    delegacoes = Delegacao.query.order_by(Delegacao.nome).all()
    partidas = Partida.query.order_by(Partida.data.desc()).all()
    return render_template('admin/index.html', delegacoes=delegacoes, partidas=partidas)

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
    if delegacao.lider and delegacao.lider != novo_lider:
        delegacao.lider.cargo = 'USER'
    delegacao.lider = novo_lider
    novo_lider.cargo = 'LIDER'
    db.session.commit()
    flash(f'{novo_lider.nome} foi definido como líder da delegação {delegacao.nome}.', 'success')
    return redirect(url_for('admin.manage_delegacao', id=id))

@bp.route('/partida', methods=['POST'])
@admin_required
def add_partida():
    delegacao_a_id = request.form.get('delegacao_a_id')
    delegacao_b_id = request.form.get('delegacao_b_id')
    data_str = request.form.get('data')
    if not all([delegacao_a_id, delegacao_b_id, data_str]):
        flash('Todos os campos são obrigatórios.', 'error')
        return redirect(url_for('admin.index'))
    if delegacao_a_id == delegacao_b_id:
        flash('As delegações devem ser diferentes.', 'error')
        return redirect(url_for('admin.index'))
    data = datetime.fromisoformat(data_str)
    nova_partida = Partida(delegacao_a_id=delegacao_a_id, delegacao_b_id=delegacao_b_id, data=data)
    db.session.add(nova_partida)
    db.session.commit()
    flash('Partida agendada com sucesso!', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/partida/<int:id>')
@admin_required
def manage_partida(id):
    partida = Partida.query.get_or_404(id)
    jogadores_a = partida.delegacao_a.jogadores
    jogadores_b = partida.delegacao_b.jogadores
    todos_jogadores_partida = sorted(jogadores_a + jogadores_b, key=lambda j: j.nome)
    return render_template('admin/manage_partida.html', partida=partida, todos_jogadores_partida=todos_jogadores_partida)

@bp.route('/partida/<int:id>/placar', methods=['POST'])
@admin_required
def update_placar(id):
    partida = Partida.query.get_or_404(id)
    partida.placar_a = request.form.get('placar_a', type=int)
    partida.placar_b = request.form.get('placar_b', type=int)
    partida.finalizada = 'finalizada' in request.form
    db.session.commit()
    flash('Placar e status da partida atualizados.', 'success')
    return redirect(url_for('admin.manage_partida', id=id))

@bp.route('/partida/<int:id>/evento', methods=['POST'])
@admin_required
def add_evento(id):
    partida = Partida.query.get_or_404(id)
    jogador_id = request.form.get('jogador_id')
    tipo_evento = request.form.get('tipo_evento')
    if not all([jogador_id, tipo_evento]):
        flash('Dados do evento incompletos.', 'error')
        return redirect(url_for('admin.manage_partida', id=id))
    if tipo_evento == 'MELHOR_DA_PARTIDA':
        evento_existente = Evento.query.filter_by(partida_id=id, tipo_evento='MELHOR_DA_PARTIDA').first()
        if evento_existente:
            flash('O prêmio Melhor da Partida já foi registrado para este jogo.', 'error')
            return redirect(url_for('admin.manage_partida', id=id))
    novo_evento = Evento(partida_id=id, jogador_id=jogador_id, tipo_evento=tipo_evento)
    db.session.add(novo_evento)
    db.session.commit()
    flash(f'Evento "{tipo_evento}" registrado com sucesso!', 'success')
    return redirect(url_for('admin.manage_partida', id=id))
