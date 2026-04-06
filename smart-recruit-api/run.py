from app import create_app, db
from app.models import OffreEmploi, Candidat, Candidature

app = create_app()

with app.app_context():
    db.create_all() #Crée les tables si elles n'exitent pas
    print("Tables crées!")

if __name__ == "__main__":
    app.run(debug=True)