# firebaseConfig.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin SDK only if not already initialized
if not firebase_admin._apps:
    # Path to your service account key
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "accountKey.json")
    
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized.")
else:
    print("Firebase Admin SDK already initialized.")

# Initialize Firestore
db = firestore.client()
