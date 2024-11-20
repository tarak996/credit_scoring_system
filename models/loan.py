from bson.objectid import ObjectId
import datetime

class LoanModel:
    def __init__(self, db):
        self.loans = db.loans

    def create_loan(self, user_email, loan_amount, tenure, purpose, credit_score):
        """Creates a new loan application."""
        loan_data = {
            "user_email": user_email,
            "loan_amount": loan_amount,
            "tenure": tenure,
            "purpose": purpose,
            "credit_score": credit_score,
            "status": "Pending",  # Default status
            "created_at": datetime.datetime.utcnow()
        }
        result = self.loans.insert_one(loan_data)
        return str(result.inserted_id)

    def get_loan_by_id(self, loan_id):
        """Fetches loan details by ID."""
        return self.loans.find_one({"_id": ObjectId(loan_id)})

    def update_loan_status(self, loan_id, new_status):
        """Updates the status of a loan application."""
        self.loans.update_one({"_id": ObjectId(loan_id)}, {"$set": {"status": new_status}})
