# init_db.py

from app import app, db
from models import User

with app.app_context():
    db.create_all()
    # Create an admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin_user.set_password('secure_admin_password')  # Use a strong password
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

