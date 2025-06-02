from app import app, db
from models import Camera

def seed_data():
    with app.app_context():
        # Clear existing data
        Camera.query.delete()
        
        # Add sample cameras
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
        
        # Add cameras to database
        db.session.add_all(cameras)
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
