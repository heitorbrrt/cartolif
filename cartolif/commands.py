import click
from flask.cli import with_appcontext
from . import db
from .models import User

@click.command('create-admin')
@with_appcontext
@click.argument('nome')
@click.argument('email')
@click.argument('password')
def create_admin_command(nome, email, password):
    """Cria um novo usuário com o cargo de ADMIN."""
    
    # Verifica se o email já existe
    if User.query.filter_by(email=email).first():
        click.echo(f"Erro: O e-mail '{email}' já está cadastrado.")
        return

    admin_user = User(nome=nome, email=email, cargo='ADMIN')
    admin_user.set_password(password)
    
    db.session.add(admin_user)
    db.session.commit()
    
    click.echo(f"Administrador '{nome}' criado com sucesso.")
