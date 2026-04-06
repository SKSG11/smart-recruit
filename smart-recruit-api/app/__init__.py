from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

#Chargement des variables du fichier .env
load_dotenv()

#Initialisation des extensions
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    #Configuration de la base de données
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #Link des extensions à l'app
    db.init_app(app)
    ma.init_app(app)

    #Enregistrement du blueprint
    from app.blueprints.routes import main
    app.register_blueprint(main)

    # Gestion des erreurs globales
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erreur": "Ressource introuvable"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"erreur": "Erreur interne du serveur"}), 500
    
    return app