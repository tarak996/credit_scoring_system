Credit Scoring and Loan Application System
Table of Contents

   1) Overview
   2) Features
   3) Technologies Used
   4) Project Structure
   5) Database Design
   6) API Endpoints
   7) Frontend Pages
   8) Performance Optimizations
   9) Setup Instructions
   10) Testing Workflow

1. Overview

The Credit Scoring and Loan Application System is designed to:

  *)  Allow users to register, log in, apply for loans, and view loan status.
  *) Enable admins to review loan applications, approve/reject loans, and filter applications by status.
  *) It ensures data security, performance optimization, and comprehensive logging for audit purposes.

2. Features
    
    I) User Features

        *) Register/Login:
                Secure authentication with JWT tokens.
        *) Apply for Loans:
                Dynamically calculate credit scores based on predefined criteria.
        *) View Loan Status:
                See all loans submitted by the user, along with their statuses.

    II) Admin Features

        *) View All Loans:
            List all loan applications with filters (e.g., Pending, Approved, Rejected).
        *) Approve/Reject Loans:
            Change the status of loans.
        *) Audit Logs:
            Track all admin actions for compliance.

3. Technologies Used

    I) Backend: Flask (Python)
    II) Frontend: HTML, CSS, JavaScript
    III) Database: MongoDB
    IV) Authentication: JWT (JSON Web Token)

4. Project Structure
        credit_scoring_system/
        ├── app.py                  # Main Flask app
        ├── config.py               # Configuration file
        ├── db.py                   # MongoDB connection
        ├── requirements.txt        # Python dependencies
        ├── models/                 # Data models
        │   ├── user.py             # User model
        ├── routes/                 # Flask blueprints
        │   ├── user_routes.py      # User endpoints
        │   ├── loan_routes.py      # Loan endpoints
        │   ├── admin_routes.py     # Admin endpoints
        ├── services/               # Utility services
        │   ├── credit_score.py     # Credit score calculation
        │   ├── log_service.py      # Logging actions
        ├── templates/              # HTML templates
        │   ├── register.html       # User register/login page
        │   ├── apply_loan.html     # Loan application page
        │   ├── loan_status.html    # Loan status page
        │   ├── admin_dashboard.html# Admin dashboard
        ├── static/                 # Static files
        │   ├── css/                # CSS stylesheets
        │   │   └── styles.css      # Main stylesheet
        │   └── js/                 # JavaScript files
        │       ├── app.js          # User-side logic
        │       └── admin.js        # Admin-side logic


5. Database Design

    I) Users Collection
        Tracks user details, including their role (user/admin).

        {
    "_id": "ObjectId",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "password": "hashed_password",
    "role": "user",
    "credit_score_cache": 750
}
    II. Loans Collection
        Stores loan applications and their statuses.

        {
    "_id": "ObjectId",
    "user_email": "john.doe@example.com",
    "loan_amount": 100000,
    "tenure": 12,
    "purpose": "Home Renovation",
    "credit_score": 750,
    "status": "Pending",
    "timestamp": "2024-11-19T12:00:00Z"
}

    III). Logs Collection
        Tracks admin and user actions for audit purposes.

        {
    "_id": "ObjectId",
    "action": "Loan Approved",
    "user_email": "admin@example.com",
    "details": {"loan_id": "648e5c6b5f1b2a91a23df77f", "status": "Approved"},
    "timestamp": "2024-11-19T12:30:00Z"
}

6. API Endpoints
        
        I) User Endpoints

            POST /user/register: Register a new user.
            POST /user/login: Authenticate user and issue JWT.

        II) Loan Endpoints

            POST /loan/apply: Submit a new loan application.
            GET /loan/status/all: Fetch loans for the logged-in user.

        III) Admin Endpoints

            GET /admin/all-loans: View all loans with optional status filter.
            POST /admin/review-loan/<loan_id>: Approve or reject a loan.

7. Frontend Pages

    I)  Register/Login:
            Allows users to register or log in.
    II) Loan Application:
            Allows users to apply for a loan.
    III)Loan Status:
            Displays all loans submitted by the logged-in user.
    IV) Admin Dashboard:
            Allows admins to review and manage loans.

8. Performance Optimizations

    I) Credit Score Caching:
            Cached credit scores in the Users collection to reduce recalculations.
            Cached values expire after 24 hours using TTL indexing.
    II) MongoDB Indexing:
            Indexed email in Users, user_email and status in Loans, and timestamp in Logs.

9. Setup Instructions

    I) Install Dependencies:
            pip install -r requirements.txt

    II) Start MongoDB:
            mongod
    III) Run the Application:
            python3 app.py

10. Testing Workflow

    I) User Testing:
            Register a user (POST /user/register).
            Log in as the user (POST /user/login).
            Apply for a loan (POST /loan/apply).
            View loan status (GET /loan/status/all).

    II) Admin Testing:
            Log in as an admin (POST /user/login).
            View all loans (GET /admin/all-loans).
            Approve or reject a loan (POST /admin/review-loan/<loan_id>).

    III) Database Verification:
            Check that users, loans, and logs are correctly inserted into MongoDB.