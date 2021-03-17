from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

# Instantiate Flask Extension Objects
db = SQLAlchemy()
db_migration = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Application Factory Function
def create_app():

    # Instantiate flask application instance
    app = Flask(__name__)

    # Configure the flask application instance
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    # Configure logging
    configure_logging(app)

    # Initialize extensions
    initialize_extensions(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    register_blueprints(app)

    return app

# Helper Functions
def configure_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    # Create a file handler object
    file_handler = RotatingFileHandler('instance/task-master.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

def initialize_extensions(app):
    db.init_app(app)
    db_migration.init_app(app,db)
    bootstrap.init_app(app)
    login_manager.init_app(app)

def register_error_handlers(app):
    from flask import render_template

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(403)
    def method_not_allowed(error):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(403)
    def server_error(error):
        return render_template('500.html'), 500

def register_blueprints(app):
    # Import auth blueprint responsible for user management 
    from project.auth import auth_blueprint

    # Import main blueprint responsible for task master functionality
    from project.main import main_blueprint

    # Register the blueprints with the flask application instance
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)



