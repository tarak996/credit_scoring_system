from db import mongo

def calculate_credit_score(income, existing_loans, user_email):
    # Check cache
    user = mongo.db.users.find_one({"email": user_email})
    if "credit_score_cache" in user:
        return user["credit_score_cache"]

    # Calculate credit score
    score = 0
    if income > 50000:
        score += 50
    score += (10 - existing_loans) * 5

    # Save to cache
    mongo.db.users.update_one(
        {"email": user_email},
        {"$set": {"credit_score_cache": score}}
    )

    return score
