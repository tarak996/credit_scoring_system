from datetime import datetime
from db import mongo

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
