from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import UserModel
from db import mongo  # Import the MongoDB instance
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint setup
user_bp = Blueprint("user", __name__)
user_model = UserModel(mongo.db)

@user_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not all([name, email, phone, password]):
        return jsonify({"error": "All fields are required!"}), 400

    if user_model.find_by_email(email):
        return jsonify({"error": "User already exists!"}), 409

    user_id = user_model.create_user(name, email, phone, password)
    return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201

@user_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required!"}), 400

    user = user_model.find_by_email(email)
    if not user or not user_model.verify_password(user["password"], password):
        return jsonify({"error": "Invalid credentials!"}), 401

    access_token = create_access_token(identity={"email": email, "role": user["role"]})
    return jsonify({"message": "Login successful!", "access_token": access_token, "role": user["role"] }), 200

@user_bp.route("/promote-to-admin", methods=["POST"])
@jwt_required()
def promote_to_admin():
    """Promote a user to admin role."""
    current_user = get_jwt_identity()
    
    # Ensure only existing admins can promote other users
    if current_user.get("role") != "admin":
        return jsonify({"error": "Access denied. Admins only."}), 403

    data = request.json
    email = data.get("email")

    # Check if the user exists
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found!"}), 404

    # Update the user's role to admin
    mongo.db.users.update_one({"email": email}, {"$set": {"role": "admin"}})
    return jsonify({"message": f"User {email} promoted to admin successfully!"}), 200

