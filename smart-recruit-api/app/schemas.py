from app import ma
from app.models import OffreEmploi, Candidat, Candidature
from marshmallow import fields, validate

# Schéma pour OffreEmploi
class OffreEmploiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OffreEmploi
        load_instance = True  # Crée directement un objet OffreEmploi

    titre = fields.String(
        required=True,
        validate=validate.Length(min=3, max=150)
    )
    description = fields.String(required=True)
    competences = fields.List(fields.String(), required=True)
    salaire = fields.Float(required=True, validate=validate.Range(min=0))


# Schéma pour Candidat
class CandidatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidat
        load_instance = True

    nom = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    email = fields.Email(required=True)  # Vérifie automatiquement le format email
    bio = fields.String(required=True)
    diplome = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100)
    )


# Schéma pour Candidature
class CandidatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidature
        load_instance = True

    candidat_id = fields.Integer(required=True)
    offre_id = fields.Integer(required=True)

    # Affiche les détails du candidat et de l'offre dans la réponse
    candidat = fields.Nested(CandidatSchema, dump_only=True)
    offre = fields.Nested(OffreEmploiSchema, dump_only=True)


# Instances des schémas (on les utilisera dans les routes)
offre_schema = OffreEmploiSchema()
offres_schema = OffreEmploiSchema(many=True)  # Pour une liste d'offres

candidat_schema = CandidatSchema()
candidats_schema = CandidatSchema(many=True)  # Pour une liste de candidats

candidature_schema = CandidatureSchema()
candidatures_schema = CandidatureSchema(many=True)