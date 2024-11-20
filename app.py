from flask import Flask
from flask_jwt_extended import JWTManager
from db import mongo  # Import the MongoDB instance

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config.py')

# Initialize MongoDB
mongo.init_app(app)

# Initialize JWT for authentication
jwt = JWTManager(app)

# Register routes
from routes.user_routes import user_bp
app.register_blueprint(user_bp, url_prefix="/user")

from routes.loan_routes import loan_bp
app.register_blueprint(loan_bp, url_prefix="/loan")

from routes.admin_routes import admin_bp
app.register_blueprint(admin_bp, url_prefix="/admin")

from flask import render_template

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/apply_loan")
def apply_loan_page():
    return render_template("apply_loan.html")

@app.route("/admin_dashboard")
def admin_dashboard_page():
    return render_template("admin_dashboard.html")

@app.route("/loan_status")
def loan_status_page():
    return render_template("loan_status.html")

if __name__ == "__main__":
    app.run(debug=True)
