from app import app, db
from models import Camera
import os

# Configuration spécifique pour Render
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

with app.app_context():
    # Supprime toutes les tables existantes
    db.drop_all()
    # Crée toutes les tables
    db.create_all()
    # Ajoute les caméras réelles
    cameras = [
        Camera(
            name="CAM-001",
            ip_address="192.168.1.101",
            code="A1",
            room_number="Salle A1"
        ),
        Camera(
            name="CAM-002",
            ip_address="192.168.1.102",
            code="A2",
            room_number="Salle A2"
        ),
        Camera(
            name="CAM-003",
            ip_address="192.168.1.103",
            code="A3",
            room_number="Salle A3"
        ),
        Camera(
            name="CAM-004",
            ip_address="192.168.1.201",
            code="B1",
            room_number="Salle B1"
        )
    ]
    db.session.add_all(cameras)
    db.session.commit()
    print("Base de données initialisée avec succès!")
