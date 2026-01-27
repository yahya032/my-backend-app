import os
import json
import firebase_admin
from firebase_admin import credentials

# Charger la clé depuis la variable d'environnement FIREBASE_KEY_JSON
firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")

if not firebase_key_json:
    raise ValueError("FIREBASE_KEY_JSON n'est pas défini")

# Convertir la chaîne JSON en dict Python
cred_dict = json.loads(firebase_key_json)

# Initialiser Firebase avec le dict
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
