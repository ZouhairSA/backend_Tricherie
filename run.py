from app import app, db
from models import Camera
import os
import sys
import logging
from sqlalchemy import inspect

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration spécifique pour Render
try:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    
    # Test de connexion à la base de données
    try:
        with app.app_context():
            db.engine.connect()
            logger.info("Database connection successful")
            
            # Test if tables exist
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            logger.info(f"Database tables: {tables}")
            
            # Check if we need to initialize the database
            if not tables:
                logger.info("Database needs initialization")
                db.create_all()
                logger.info("Database initialized successfully")
            else:
                logger.info("Database already initialized, skipping initialization")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        sys.exit(1)
        try:
            db.engine.connect()
            logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            sys.exit(1)

    with app.app_context():
        # Vérifie si les tables existent déjà
        inspector = inspect(db.engine)
        if not inspector.has_table('cameras'):
            logger.info("Initializing database for the first time...")
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
            
            for camera in cameras:
                db.session.add(camera)
            db.session.commit()
            logger.info("Initial data inserted successfully")
        else:
            logger.info("Database already initialized, skipping initialization")

except Exception as e:
    logger.error(f"Error during database initialization: {str(e)}")
    sys.exit(1)
