from flask import Blueprint, jsonify, request
from app.services import (
    creer_candidat,
    creer_offre,
    soumettre_candidature,
    get_candidats_par_offre
)
from app.services import analyser_match


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return {"message": "Bienvenue sur Smart-Recruit API!"}

@main.route("/candidates", methods=["POST"])
def register_candidate():
    return creer_candidat(request.get_json())

@main.route("/offers", methods=["POST"])
def create_offer():
    return creer_offre(request.get_json())

@main.route("/apply", methods=["POST"])
def apply():
    return soumettre_candidature(request.get_json())

@main.route("/offers/<int:offre_id>/candidates", methods=["GET"])
def get_candidates(offre_id):
    return get_candidats_par_offre(offre_id)

@main.route("/offers/<int:offre_id>/analyze-match", methods=["POST"])
def analyze_match(offre_id):
    return analyser_match(offre_id, request.get_json())