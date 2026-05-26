from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Inicializa as extensões, mas sem vincular a uma app ainda
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)

    # Configurações da aplicação
    app.config.from_mapping(
        SECRET_KEY='uma-chave-secreta-muito-segura',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'cartolif.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Garante que a pasta 'instance' exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configura a view de login para o Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'

    # Importa e registra o comando CLI
    from . import commands
    app.cli.add_command(commands.create_admin_command)

    with app.app_context():
        # Importa as partes da aplicação
        from . import models
        from . import routes
        from . import auth
        from . import admin
        from . import lider # Importa o novo módulo lider

        # Define o user_loader para o Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(int(user_id))

        # Registra os blueprints
        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(lider.bp) # Registra o blueprint de lider

        # Cria as tabelas do banco de dados, se não existirem
        db.create_all()

    return app
