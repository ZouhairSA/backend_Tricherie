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

from sqlalchemy import inspect

with app.app_context():
    # Vérifie si les tables existent déjà
    inspector = inspect(db.engine)
    if not inspector.has_table('cameras'):
        print("INFO:app:Initializing database for the first time...")
        # Supprime toutes les tables existantes
        db.drop_all()
        # Crée toutes les tables
        db.create_all()
        
        # Insertion des données initiales
        cameras = [
            Camera(
                name="Camera 1",
                ip_address="192.168.1.1",
                code="CAM001",
                room_number="Salle A"
            ),
            Camera(
                name="Camera 2",
                ip_address="192.168.1.2",
                code="CAM002",
                room_number="Salle B"
            ),
            Camera(
                name="Camera 3",
                ip_address="192.168.1.3",
                code="CAM003",
                room_number="Salle C"
            )
        ]
        db.session.add_all(cameras)
        db.session.commit()
        print("INFO:app:Database initialized successfully")
        print("Base de données initialisée avec succès!")
    else:
        print("INFO:app:Database already initialized, skipping initialization")
