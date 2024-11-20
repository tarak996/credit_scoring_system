from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.loan import LoanModel
from db import mongo
from functools import wraps
from bson.objectid import ObjectId

# Blueprint setup
admin_bp = Blueprint("admin", __name__)
loan_model = LoanModel(mongo.db)

def admin_required(func):
    """Decorator to ensure the user is an admin."""
    @wraps(func)  # Preserve the original function name
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        if user.get("role") != "admin":
            return jsonify({"error": "Access denied. Admins only."}), 403
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route("/all-loans", methods=["GET"])
@jwt_required()
def all_loans():
    """Get a list of all loan applications."""
    current_user = get_jwt_identity()

    # Ensure the user is an admin
    if current_user.get("role") != "admin":
        return jsonify({"error": "Access denied. Admins only."}), 403

    loans = mongo.db.loans.find()
    result = [
        {
            "loan_id": str(loan["_id"]),
            "user_email": loan["user_email"],
            "loan_amount": loan["loan_amount"],
            "tenure": loan["tenure"],
            "purpose": loan["purpose"],
            "credit_score": loan["credit_score"],
            "status": loan["status"]
        }
        for loan in loans
    ]
    return jsonify(result), 200


@admin_bp.route("/review-loan/<loan_id>", methods=["POST"])
@jwt_required()
def review_loan(loan_id):
    """Approve or reject a loan application."""
    try:
        current_user = get_jwt_identity()
        data = request.json
        new_status = data.get("status")

        # Ensure the user is an admin
        if current_user.get("role") != "admin":
            return jsonify({"error": "Access denied. Admins only."}), 403

        data = request.json
        new_status = data.get("status")

        if new_status not in ["Approved", "Rejected"]:
            return jsonify({"error": "Invalid status. Use 'Approved' or 'Rejected'."}), 400

        loan = mongo.db.loans.find_one({"_id": ObjectId(loan_id)})
        if not loan:
            return jsonify({"error": "Loan not found!"}), 404

        # Update loan status
        mongo.db.loans.update_one({"_id": ObjectId(loan_id)}, {"$set": {"status": new_status}})
        return jsonify({"message": f"Loan application {new_status} successfully!"}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error in review_loan: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
