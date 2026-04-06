from app import db
from datetime import datetime

#Table OffreEmploi
class OffreEmploi(db.Model):
    __tablename__ = "offres_emploi"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    competences = db.Column(db.JSON, nullable=False)
    salaire = db.Column(db.Float, nullable=False)

    #Relation : une offre peut avoir plusieurs candidatures
    candidatures = db.relationship("Candidature", back_populates="offre")

    def __repr__(self):
        return f"<OffreEmploi {self.titre}>"


# Table Candidat
class Candidat(db.Model):
    __tablename__ = "candidats"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    diplome = db.Column(db.String(100), nullable=False)

    # Relation : un candidat peut avoir plusieurs candidatures
    candidatures = db.relationship("Candidature", back_populates="candidat")

    def __repr__(self):
        return f"<Candidat {self.nom}>"


# Table Candidature (relation entre Candidat et OffreEmploi)
class Candidature(db.Model):
    __tablename__ = "candidatures"

    id = db.Column(db.Integer, primary_key=True)
    date_depot = db.Column(db.DateTime, default=datetime.utcnow)

    #Clés étrangères
    candidat_id = db.Column(db.Integer, db.ForeignKey("candidats.id"), nullable=False)
    offre_id = db.Column(db.Integer, db.ForeignKey("offres_emploi.id"), nullable=False)

    #Relations
    candidat = db.relationship("Candidat", back_populates="candidatures")
    offre = db.relationship("OffreEmploi", back_populates="candidatures")

    def __repr__(self):
        return f"<Candidature candidat={self.candidat_id} offre={self.offre_id}>"