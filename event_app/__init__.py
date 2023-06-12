from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "event_management.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/event_management'
    register_blueprint(app)
    db.init_app(app)

    from .bp_user.model_user import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def register_blueprint(app):
    from .bp_home.views_general import bp_home
    from .bp_events.views_event import bp_events
    from .bp_user.auth import auth
    from .bp_meetings.views_meeting import bp_meetings
    from .bp_stakeholders.controller_stakeholder import bp_stakeholders
    from .bp_calendar.views_calendar import bp_calendar
    from .bp_tasks.views_task import bp_tasks
    
    app.register_blueprint(bp_home, url_prefix='/')
    app.register_blueprint(bp_events, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(bp_meetings, url_prefix='/')
    app.register_blueprint(bp_stakeholders, url_prefix='/')
    app.register_blueprint(bp_calendar, url_prefix='/')
    app.register_blueprint(bp_tasks, url_prefix='/')


def create_database(app):
    if not path.exists('event_app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')



