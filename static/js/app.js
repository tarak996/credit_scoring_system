const BASE_URL = "http://127.0.0.1:5000"; // Define the base URL for the backend

// Utility to handle JSON parsing safely
async function parseJSON(response) {
    try {
        return await response.json();
    } catch (error) {
        console.error("Failed to parse JSON:", error);
        return { error: "Unexpected response from the server" };
    }
}

// Register user
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("registerName").value;
        const email = document.getElementById("registerEmail").value;
        const phone = document.getElementById("registerPhone").value;
        const password = document.getElementById("registerPassword").value;

        try {
            const response = await fetch(`${BASE_URL}/user/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, phone, password }),
            });

            const result = await parseJSON(response);
            if (response.ok) {
                alert(result.message || "User registered successfully!");
            } else {
                alert(result.error || "Failed to register.");
            }
        } catch (error) {
            console.error("Error registering user:", error);
            alert("An error occurred while registering. Please try again.");
        }
    });
}

// Login user
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;

        try {
            const response = await fetch(`${BASE_URL}/user/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const result = await response.json();
            if (response.ok) {
                localStorage.setItem("token", result.access_token);
                alert("Login successful!");

                // Check role and redirect accordingly
                console.log("User role:", result.role); // Debugging log
                if (result.role === "admin") {
                    window.location.href = "/admin_dashboard";
                } else {
                    window.location.href = "/apply_loan";
                }
            } else {
                alert(result.error || "Failed to log in.");
            }
        } catch (error) {
            console.error("Error logging in user:", error);
            alert("An error occurred while logging in. Please try again.");
        }
    });
}

// Loan application logic
const loanForm = document.getElementById("loanForm");
if (loanForm) {
    loanForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");

        const loanAmount = document.getElementById("loanAmount").value;
        const tenure = document.getElementById("loanTenure").value;
        const purpose = document.getElementById("loanPurpose").value;
        const income = document.getElementById("income").value;
        const existingLoans = document.getElementById("existingLoans").value;

        try {
            const response = await fetch(`${BASE_URL}/loan/apply`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ 
                    loan_amount: loanAmount, 
                    tenure, 
                    purpose, 
                    income, 
                    existing_loans: existingLoans 
                }),
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message || "Loan application submitted successfully!");
                window.location.href = "/loan_status";
            } else {
                alert(result.error || "Failed to submit loan application.");
            }
        } catch (error) {
            console.error("Error submitting loan application:", error);
            alert("An error occurred. Please try again.");
        }
    });
}


async function reviewLoan(loanId, status) {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch(`${BASE_URL}/admin/review-loan/${loanId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ status })
        });

        // Safely parse JSON response
        if (response.ok) {
            const result = await response.json();
            alert(result.message || "Action completed successfully!");
        } else {
            const error = await response.json();
            alert(error.error || "Failed to update loan status.");
        }

        fetchLoans(); // Refresh the loan list
    } catch (error) {
        console.error("Error reviewing loan:", error);
        alert("An unexpected error occurred. Please try again.");
    }
}
