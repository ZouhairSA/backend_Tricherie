from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Camera, Alert
import os
import requests
from datetime import datetime
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/exam_eye_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

# Test database connection directly
try:
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    connection = engine.connect()
    result = connection.execute('SELECT 1').fetchone()
    logger.info(f"Database connection test successful: {result}")
    connection.close()
except Exception as e:
    logger.error(f"Database connection test failed: {str(e)}")

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# Initialize database
with app.app_context():
    try:
        db.create_all()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        result = connection.execute('SELECT 1').fetchone()
        logger.info(f"Health check successful: {result}")
        connection.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500

YOLO_API_URL = "https://api-tricherie-hestim.onrender.com/predict"

@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    cameras = Camera.query.all()
    return jsonify([{
        'id': camera.id,
        'name': camera.name,
        'ip_address': camera.ip_address,
        'code': camera.code,
        'room_number': camera.room_number
    } for camera in cameras])

@app.route('/api/cameras', methods=['POST'])
def add_camera():
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'ip_address', 'code', 'room_number']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    camera = Camera(
        name=data['name'],
        ip_address=data['ip_address'],
        code=data['code'],
        room_number=data['room_number']
    )
    db.session.add(camera)
    db.session.commit()
    
    return jsonify({
        'id': camera.id,
        'name': camera.name,
        'ip_address': camera.ip_address,
        'code': camera.code,
        'room_number': camera.room_number
    }), 201

@app.route('/api/cameras/<int:camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    camera = Camera.query.get_or_404(camera_id)
    db.session.delete(camera)
    db.session.commit()
    return '', 204

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = Alert.query.all()
    return jsonify([{
        'id': alert.id,
        'camera_id': alert.camera_id,
        'timestamp': alert.timestamp.isoformat(),
        'image_path': alert.image_path,
        'detected_object': alert.detected_object
    } for alert in alerts])

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    if 'image' not in request.files or 'camera_id' not in request.form:
        return jsonify({'error': 'Missing image or camera_id'}), 400
    
    image = request.files['image']
    camera_id = request.form['camera_id']
    
    # Save image with unique name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'image_{timestamp}.jpg')
    image.save(image_path)
    
    # Call YOLO API
    try:
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            response = requests.post(YOLO_API_URL, files=files)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('detected_object') == 'phone':
                    alert = Alert(
                        camera_id=camera_id,
                        image_path=image_path,
                        detected_object='phone'
                    )
                    db.session.add(alert)
                    db.session.commit()
                    
                    return jsonify({
                        'message': 'Alert created successfully',
                        'alert': {
                            'id': alert.id,
                            'camera_id': alert.camera_id,
                            'timestamp': alert.timestamp.isoformat(),
                            'image_path': alert.image_path,
                            'detected_object': alert.detected_object
                        }
                    }), 201
                else:
                    return jsonify({'message': 'No phone detected'}), 200
            
            return jsonify({'error': 'YOLO API error'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
