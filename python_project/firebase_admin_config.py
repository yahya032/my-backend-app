import firebase_admin
from firebase_admin import credentials

# 🔹 Remplace ce chemin par le chemin exact de ton fichier JSON Firebase
cred = credentials.Certificate("serviceAccountKey.json")
# Initialise Firebase
firebase_admin.initialize_app(cred)
