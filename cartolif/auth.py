from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se o email já existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Este e-mail já está cadastrado. Tente fazer login.')
            return redirect(url_for('auth.login'))

        # Cria o novo usuário
        new_user = User(nome=nome, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça o login para continuar.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Verifica se o usuário existe e a senha está correta
        if not user or not user.check_password(password):
            flash('E-mail ou senha inválidos. Tente novamente.')
            return redirect(url_for('auth.login'))

        # Faz o login do usuário
        login_user(user)
        return redirect(url_for('routes.dashboard'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.')
    return redirect(url_for('routes.index'))
