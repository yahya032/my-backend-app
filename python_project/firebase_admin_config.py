import os
import json
import firebase_admin
from firebase_admin import credentials
def init_firebase():
    if firebase_admin._apps:
        return
    firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")
    if not firebase_key_json:
        raise ValueError("FIREBASE_KEY_JSON non défini")
    cred_dict = json.loads(firebase_key_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
# Initialisation automatique au démarrage
init_firebase()
