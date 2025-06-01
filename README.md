# Backend Exam Eye - Anti-Cheating Detection

Ce backend Flask gère la détection de tricherie via des caméras IP et un modèle YOLOv8.

## Structure du Projet

```
backend/
├── app.py          # Application Flask principale
├── models.py       # Modèles SQLAlchemy
├── requirements.txt # Dépendances Python
└── static/         # Dossier pour les images
```

## Installation

1. Créer un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

L'application sera accessible sur http://localhost:5000

## Déploiement sur Render

1. Créer un nouveau Web Service sur Render
2. Lier le dépôt GitHub contenant ce projet
3. Configurer les variables d'environnement si nécessaire
4. Déployer

## Endpoints API

- `GET /api/cameras` - Lister les caméras
- `POST /api/cameras` - Ajouter une caméra
- `DELETE /api/cameras/<id>` - Supprimer une caméra
- `GET /api/alerts` - Lister les alertes
- `POST /api/alerts` - Déclencher une détection (avec image et camera_id)

## Base de données

La base de données SQLite (`database.db`) est créée automatiquement lors du premier lancement.

## Sécurité

- Les images sont sauvegardées dans le dossier `static/` avec des noms uniques basés sur le timestamp
- Les chemins d'images sont stockés dans la base de données
- Les appels à l'API YOLO sont gérés de manière sécurisée via requests
