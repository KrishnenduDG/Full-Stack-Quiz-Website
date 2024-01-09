from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path,makedirs
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jingalala hu hu '
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Profile Pic Upload Folder
    app.config['UPLOAD_FOLDER'] = "./website/static/profile_pic"
    makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    
    db.init_app(app)

    from .auth import auth
    from .quiz import quiz

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(quiz, url_prefix='/quiz')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Redirecting the Home Page to login page
    @app.route("/",methods = ["GET"])
    def get_home_page():
        return app.redirect("/login",code=302)
    
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME + '.sqlite'):
        db.create_all(app=app)
        print('Created Database!')