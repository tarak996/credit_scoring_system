from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.loan import LoanModel
from services.credit_score import calculate_credit_score
from db import mongo
from datetime import datetime

# Blueprint setup
loan_bp = Blueprint("loan", __name__)
loan_model = LoanModel(mongo.db)

class LoanModel:
    def __init__(self, db):
        self.db = db

    def create_loan(self, user_email, loan_amount, tenure, purpose, credit_score):
        loan_data = {
            "user_email": user_email,
            "loan_amount": loan_amount,
            "tenure": tenure,
            "purpose": purpose,
            "credit_score": credit_score,
            "status": "Pending",  # Default status for new loans
            "timestamp": datetime.utcnow()
        }
        loan_id = self.db.loans.insert_one(loan_data).inserted_id
        return str(loan_id)

loan_model = LoanModel(mongo.db)

# Log service
class LogService:
    @staticmethod
    def create_log(action, user_email, details=None):
        log_entry = {
            "action": action,
            "user_email": user_email,
            "details": details,
            "timestamp": datetime.utcnow()
        }
        mongo.db.logs.insert_one(log_entry)


@loan_bp.route("/apply", methods=["POST"])
@jwt_required()
def apply_loan():
    """Submit a loan application."""
    user = get_jwt_identity()
    data = request.json

    try:
        loan_amount = float(data.get("loan_amount"))
        tenure = int(data.get("tenure"))
        purpose = data.get("purpose")
        income = int(data.get("income"))  # Convert to integer
        existing_loans = int(data.get("existing_loans"))  # Convert to integer

        # Validate required fields
        if not all([loan_amount, tenure, purpose, income, existing_loans]):
            return jsonify({"error": "All fields are required!"}), 400

        # Calculate credit score
        credit_score = calculate_credit_score(income, existing_loans)

        # Create loan application
        loan_id = loan_model.create_loan(
            user_email=user["email"],
            loan_amount=loan_amount,
            tenure=tenure,
            purpose=purpose,
            credit_score=credit_score
        )

        # Log the loan application action
        LogService.create_log(
            action="Loan Application Submitted",
            user_email=user["email"],
            details={"loan_id": loan_id, "amount": loan_amount, "purpose": purpose}
        )

        return jsonify({
            "message": "Loan application submitted successfully!",
            "loan_id": loan_id,
            "credit_score": credit_score
        }), 201

    except ValueError as e:
        return jsonify({"error": "Invalid input type: " + str(e)}), 400


@loan_bp.route("/status", methods=["GET"])
@jwt_required()
def loan_status():
    """Fetch all loans for the logged-in user."""
    user = get_jwt_identity()
    loans = loan_model.loans.find({"user_email": user["email"]})

    loan_list = [
        {
            "loan_id": str(loan["_id"]),
            "loan_amount": loan["loan_amount"],
            "tenure": loan["tenure"],
            "purpose": loan["purpose"],
            "credit_score": loan["credit_score"],
            "status": loan["status"],
            "created_at": loan["created_at"]
        }
        for loan in loans
    ]

    return jsonify(loan_list), 200


@loan_bp.route("/status/all", methods=["GET"])
@jwt_required()
def loan_status_all():
    """Get all loan applications for the logged-in user."""
    user = get_jwt_identity()
    loans = loan_model.loans.find({"user_email": user["email"]})
    result = [
        {
            "loan_id": str(loan["_id"]),
            "loan_amount": loan["loan_amount"],
            "tenure": loan["tenure"],
            "purpose": loan["purpose"],
            "credit_score": loan["credit_score"],
            "status": loan["status"]
        }
        for loan in loans
    ]
    return jsonify(result), 200


