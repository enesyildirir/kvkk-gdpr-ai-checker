from flask import Flask
from app.config import Config
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Veritabanı tablolarını oluştur
    with app.app_context():
        init_db()

    # Route'ları kaydet
    from app.routes import main
    app.register_blueprint(main)

    return app
