# assign_admin.py
import firebase_admin
from firebase_admin import credentials, auth
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

def set_admin_custom_claim(email):
    try:
        user = auth.get_user_by_email(email)
        auth.set_custom_user_claims(user.uid, {'admin': True})
        print(f"Admin role assigned to {email}")
    except Exception as e:
        print(f"Error assigning admin role: {e}")

if __name__ == "__main__":
    admin_email = input("Enter the admin user's email: ")
    set_admin_custom_claim(admin_email)
