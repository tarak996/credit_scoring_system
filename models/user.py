from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self, db):
        self.users = db.users

    def create_user(self, name, email, phone, password, role="user"):
        """Creates a new user."""
        hashed_password = generate_password_hash(password)
        user_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": hashed_password,
            "role": role
        }
        result = self.users.insert_one(user_data)
        return str(result.inserted_id)

    def find_by_email(self, email):
        """Finds a user by email."""
        return self.users.find_one({"email": email})

    def verify_password(self, stored_password, provided_password):
        """Verifies a password."""
        return check_password_hash(stored_password, provided_password)
