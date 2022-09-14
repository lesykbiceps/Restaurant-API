from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import EmployeeModel, VoteModel, MenuModel, RestaurantModel, session

def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            from app.database.database import db, base
            base.metadata.create_all(db)


def setup_jwt(app):
    jwt = JWTManager(app)

    from app.models import RevokedTokenModel

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

def clear_data():
    from app.database.database import session
    session.query(MenuModel).delete()
    session.commit()
    session.query(VoteModel).delete()
    session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'Sokyrka12031990403'
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_data, trigger='interval', hours=24)
    scheduler.start()
    # database first, then blueprints!
    setup_database(app)
    setup_jwt(app)

    from .views import employees_bp, auth_bp, votes_bp, restaurants_bp, menus_bp
    app.register_blueprint(employees_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(votes_bp)
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(menus_bp)
    return app
