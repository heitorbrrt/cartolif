from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import TimeFantasia, Jogador, Evento, Partida
from . import db

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """ Rota para a página inicial. """
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """ Rota para o painel do usuário, onde ele gerencia seu time. """
    time_fantasia = current_user.time_fantasia
    if not time_fantasia:
        return redirect(url_for('routes.create_team'))
    
    goleiros = Jogador.query.filter_by(posicao='Goleiro').order_by(Jogador.nome).all()
    jogadores_linha = Jogador.query.filter_by(posicao='Linha').order_by(Jogador.nome).all()
    escalacao_atual = time_fantasia.jogadores_escalados

    return render_template('dashboard.html', goleiros=goleiros, jogadores_linha=jogadores_linha, escalacao_atual=escalacao_atual)

@bp.route('/create-team', methods=['GET', 'POST'])
@login_required
def create_team():
    """ Rota para a página de criação do time de fantasia. """
    if current_user.time_fantasia:
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        nome_time = request.form.get('team_name')
        if nome_time:
            novo_time = TimeFantasia(nome=nome_time, usuario=current_user)
            db.session.add(novo_time)
            db.session.commit()
            flash(f'Time "{nome_time}" criado com sucesso! Agora escale seus jogadores.', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('O nome do time não pode ser vazio.', 'error')
    return render_template('create_team.html')

@bp.route('/update-escalacao', methods=['POST'])
@login_required
def update_escalacao():
    """ Rota para processar a atualização da escalação. """
    time_fantasia = current_user.time_fantasia
    if not time_fantasia:
        return redirect(url_for('routes.create_team'))

    id_goleiro = request.form.get('goleiro')
    ids_jogadores_linha = request.form.getlist('jogadores_linha')

    if not id_goleiro or len(ids_jogadores_linha) != 4:
        flash('Você deve selecionar 1 goleiro e 4 jogadores de linha.', 'error')
        return redirect(url_for('routes.dashboard'))
    
    ids_selecionados = [id_goleiro] + ids_jogadores_linha
    if len(set(ids_selecionados)) != 5:
        flash('Você não pode escalar o mesmo jogador duas vezes.', 'error')
        return redirect(url_for('routes.dashboard'))

    jogadores = Jogador.query.filter(Jogador.id.in_(ids_selecionados)).all()
    if len(jogadores) != 5:
        flash('Um ou mais jogadores selecionados são inválidos.', 'error')
        return redirect(url_for('routes.dashboard'))

    time_fantasia.jogadores_escalados = jogadores
    db.session.commit()
    flash('Sua escalação foi atualizada com sucesso!', 'success')
    return redirect(url_for('routes.dashboard'))

@bp.route('/ranking')
def ranking():
    """ Rota para a página de ranking geral. """
    times_fantasia = TimeFantasia.query.all()
    ranking_data = []

    PONTOS_GOL, PONTOS_MVP, PONTOS_GOLEIRO_SEM_GOL = 8, 5, 5

    for time in times_fantasia:
        pontuacao_total = 0
        for jogador in time.jogadores_escalados:
            for evento in jogador.eventos:
                if evento.partida.finalizada:
                    if evento.tipo_evento == 'GOL': pontuacao_total += PONTOS_GOL
                    elif evento.tipo_evento == 'MELHOR_DA_PARTIDA': pontuacao_total += PONTOS_MVP
            
            if jogador.posicao == 'Goleiro':
                partidas_como_goleiro = Partida.query.filter(Partida.finalizada == True).filter(
                    (Partida.delegacao_a_id == jogador.delegacao_id) | (Partida.delegacao_b_id == jogador.delegacao_id)
                ).all()
                for partida in partidas_como_goleiro:
                    if (partida.delegacao_a_id == jogador.delegacao_id and partida.placar_b == 0) or \
                       (partida.delegacao_b_id == jogador.delegacao_id and partida.placar_a == 0):
                        pontuacao_total += PONTOS_GOLEIRO_SEM_GOL
        ranking_data.append({'time': time, 'pontuacao': pontuacao_total})

    ranking_data_sorted = sorted(ranking_data, key=lambda item: item['pontuacao'], reverse=True)
    return render_template('ranking.html', ranking=ranking_data_sorted)

@bp.route('/jogadores')
def lista_jogadores():
    """ Rota para a lista de todos os jogadores. """
    jogadores = Jogador.query.order_by(Jogador.nome).all()
    return render_template('lista_jogadores.html', jogadores=jogadores)

@bp.route('/jogador/<int:id>')
def perfil_jogador(id):
    """ Rota para a página de perfil de um jogador específico. """
    jogador = Jogador.query.get_or_404(id)
    stats = {
        'gols': Evento.query.filter_by(jogador_id=id, tipo_evento='GOL').count(),
        'mvps': Evento.query.filter_by(jogador_id=id, tipo_evento='MELHOR_DA_PARTIDA').count()
    }
    return render_template('perfil_jogador.html', jogador=jogador, stats=stats)
