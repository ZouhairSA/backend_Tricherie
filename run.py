from app import app, db
from models import Camera
import os
import sys

# Configuration spécifique pour Render
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("DATABASE_URL environment variable is not set")
    sys.exit(1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

with app.app_context():
    # Vérifie si les tables existent déjà
    if not db.engine.dialect.has_table(db.engine, 'camera'):
        print("INFO:app:Initializing database for the first time...")
        # Supprime toutes les tables existantes
        db.drop_all()
        # Crée toutes les tables
        db.create_all()
        
        # Insertion des données initiales
        cameras = [
            Camera(name="Camera 1", location="Salle A"),
            Camera(name="Camera 2", location="Salle B"),
            Camera(name="Camera 3", location="Salle C")
        ]
        db.session.add_all(cameras)
        db.session.commit()
        print("INFO:app:Database initialized successfully")
        print("Base de données initialisée avec succès!")
    else:
        print("INFO:app:Database already initialized, skipping initialization")
