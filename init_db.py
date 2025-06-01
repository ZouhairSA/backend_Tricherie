from app import app, db
from models import Camera

def init_db():
    with app.app_context():
        # Supprime toutes les tables existantes
        db.drop_all()
        # Crée toutes les tables
        db.create_all()
        # Ajoute quelques caméras de test
        test_cameras = [
            Camera(name="Camera 1", ip_address="192.168.1.1", code="CAM001", room_number="S101"),
            Camera(name="Camera 2", ip_address="192.168.1.2", code="CAM002", room_number="S102")
        ]
        db.session.add_all(test_cameras)
        db.session.commit()
        print("Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_db()
