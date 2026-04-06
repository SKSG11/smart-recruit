from app import db
from app.models import OffreEmploi, Candidat, Candidature
from app.schemas import (
    offre_schema, offres_schema,
    candidat_schema, candidats_schema,
    candidature_schema
)
from marshmallow import ValidationError
from flask import jsonify
from app.ai_service import analyser_compatibilite
from app.models import OffreEmploi, Candidat

# ---- CANDIDATS ----

def creer_candidat(data):
    # Validation des données
    try:
        candidat = candidat_schema.load(data)
    except ValidationError as err:
        return jsonify({"erreurs": err.messages}), 422

    # Vérification unicité de l'email
    existing = Candidat.query.filter_by(email=data.get("email")).first()
    if existing:
        return jsonify({"erreur": "Un candidat avec cet email existe déjà"}), 409

    db.session.add(candidat)
    db.session.commit()
    return jsonify(candidat_schema.dump(candidat)), 201


# ---- OFFRES ----

def creer_offre(data):
    try:
        offre = offre_schema.load(data)
    except ValidationError as err:
        return jsonify({"erreurs": err.messages}), 422

    db.session.add(offre)
    db.session.commit()
    return jsonify(offre_schema.dump(offre)), 201


# ---- CANDIDATURES ----

def soumettre_candidature(data):
    # Vérifier que le candidat existe
    candidat = Candidat.query.get(data.get("candidat_id"))
    if not candidat:
        return jsonify({"erreur": "Candidat introuvable"}), 404

    # Vérifier que l'offre existe
    offre = OffreEmploi.query.get(data.get("offre_id"))
    if not offre:
        return jsonify({"erreur": "Offre introuvable"}), 404

    # Vérifier que le candidat n'a pas déjà postulé
    existing = Candidature.query.filter_by(
        candidat_id=data.get("candidat_id"),
        offre_id=data.get("offre_id")
    ).first()
    if existing:
        return jsonify({"erreur": "Ce candidat a déjà postulé à cette offre"}), 409

    try:
        candidature = candidature_schema.load(data)
    except ValidationError as err:
        return jsonify({"erreurs": err.messages}), 422

    db.session.add(candidature)
    db.session.commit()
    return jsonify(candidature_schema.dump(candidature)), 201


# ---- LISTE CANDIDATS PAR OFFRE ----

def get_candidats_par_offre(offre_id):
    offre = OffreEmploi.query.get(offre_id)
    if not offre:
        return jsonify({"erreur": "Offre introuvable"}), 404

    candidatures = Candidature.query.filter_by(offre_id=offre_id).all()
    candidats = [c.candidat for c in candidatures]
    return jsonify(candidats_schema.dump(candidats)), 200


# ---- ANALYSE IA ----

def analyser_match(offre_id, data):
    # Récupérer l'offre
    offre = OffreEmploi.query.get(offre_id)
    if not offre:
        return jsonify({"erreur": "Offre introuvable"}), 404

    # Récupérer le candidat via son ID
    candidat_id = data.get("candidat_id")
    candidat = Candidat.query.get(candidat_id)
    if not candidat:
        return jsonify({"erreur": "Candidat introuvable"}), 404

    # Appel au service IA
    resultat, erreur = analyser_compatibilite(offre.description, candidat.bio)

    if erreur:
        return jsonify({"erreur": erreur}), 503

    return jsonify({
        "offre": offre.titre,
        "candidat": candidat.nom,
        "analyse": resultat
    }), 200