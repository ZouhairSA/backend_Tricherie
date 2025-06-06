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
    # Get required environment variables
    required_vars = {
        'DATABASE_URL': 'Database connection string',
        'FLASK_APP': 'Flask application file',
        'FLASK_ENV': 'Flask environment',
        'API_URL': 'YOLO API endpoint'
    }
    
    # Validate all required variables
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Required environment variable {var_name} is not set")
        
        # Validate specific values
        if var_name == 'DATABASE_URL' and not value.startswith('postgresql://'):
            raise ValueError(f"Invalid DATABASE_URL format: {value}")
        elif var_name == 'FLASK_APP' and not os.path.exists(value):
            raise ValueError(f"FLASK_APP file not found: {value}")
        elif var_name == 'FLASK_ENV' and value not in ['production', 'development']:
            raise ValueError(f"Invalid FLASK_ENV value: {value}")
        
        logger.info(f"Using {description}: {value}")
    
    # Set database URL
    DATABASE_URL = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    
    # Set other required configurations
    app.config['FLASK_APP'] = os.getenv('FLASK_APP', 'app.py')
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')
    
    # Set YOLO API URL
    global YOLO_API_URL
    YOLO_API_URL = os.getenv('API_URL', 'https://api-tricherie-hestim.onrender.com/predict')
    
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
