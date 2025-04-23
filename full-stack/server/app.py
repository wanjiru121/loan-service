import os
import json
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from services.loan_service import LoanService
from utils.helpers import generate_due_dates, calculate_expected_repayment
from config.constants import LOAN_PAYMENT_STATUS

# Define path to the data file
DATA_FILE = "/tmp/loan_data.json"


# Default data to use if file doesn't exist
default_data = {
    "loans": [
        {
            "id": 1,
            "name": "Tom's Loan",
            "start_date": "2024-03-01",
            "interest_rate": 5.0,
            "principal": 10000,
            "months": 12,
            "due_dates": generate_due_dates("2024-03-01", 12),
            "expected_repayment_amount": calculate_expected_repayment(10000, 5.0, 12),
            "remaining_balance": 14269
        },
        {
            "id": 2,
            "name": "Chris Wailaka",
            "start_date": "2024-03-01",
            "interest_rate": 3.5,
            "principal": 500000,
            "months": 24,
            "due_dates": generate_due_dates("2024-03-01", 24),
            "expected_repayment_amount": calculate_expected_repayment(500000, 3.5, 24),
            "remaining_balance": 898438,
        },
        {
            "id": 3,
            "name": "NP Mobile Money",
            "start_date": "2024-03-01",
            "interest_rate": 4.5,
            "principal": 30000,
            "months": 6,
            "due_dates": generate_due_dates("2024-03-01", 6),
            "expected_repayment_amount": calculate_expected_repayment(30000, 4.5, 6),
            "remaining_balance": 32875,
        },
        {
            "id": 4,
            "name": "Esther's Autoparts",
            "start_date": "2024-03-01",
            "interest_rate": 1.5,
            "principal": 40000,
            "months": 12,
            "due_dates": generate_due_dates("2024-03-01", 12),
            "expected_repayment_amount": calculate_expected_repayment(40000, 1.5, 12),
            "remaining_balance": 37051,
        },
    ],
    "loan_payments": [
        {
            "id": 1,
            "loan_id": 1,
            "payment_date": "2025-04-05",
            "due_date": "2025-03-01",
            "amount": 856,
            "status": LOAN_PAYMENT_STATUS["DEFAULTED"],  # Late payment, more than 30 days late
        },
        {
            "id": 2,
            "loan_id": 1,
            "payment_date": "2025-05-01",
            "due_date": "2025-04-01",
            "amount": 875,
            "status": LOAN_PAYMENT_STATUS["ON_TIME"],  # Paid within 5 days of due date
        },
        {
            "id": 3,
            "loan_id": 2,
            "payment_date": "2025-03-15",
            "due_date": "2025-03-01",
            "amount": 21562,
            "status": LOAN_PAYMENT_STATUS["LATE"],  # Paid late (between 6-30 days late)
        },
        {
            "id": 4,
            "loan_id": 3,
            "payment_date": "2025-04-05",
            "due_date": "2025-03-01",
            "amount": 5225,
            "status": LOAN_PAYMENT_STATUS['DEFAULTED'],  # Late payment, more than 30 days late
        },
        {
            "id": 5,
            "loan_id": 4,
            "payment_date": "2025-03-10",
            "due_date": "2025-03-01",
            "amount": 3383,
            "status": LOAN_PAYMENT_STATUS["LATE"],  # Paid late (between 6-30 days late)
        },
        {
            "id": 6,
            "loan_id": 4,
            "payment_date": "2025-04-01",
            "due_date": "2025-04-01",
            "amount": 3383,
            "status": LOAN_PAYMENT_STATUS["ON_TIME"],  # Paid within 5 days of due date
        },
        {
            "id": 7,
            "loan_id": 4,
            "payment_date": "2025-05-10",
            "due_date": "2025-05-01",
            "amount": 3383,
            "status": LOAN_PAYMENT_STATUS["LATE"],  # Paid late (between 6-30 days late)
        },
    ]
}


# Ensure the data file exists, if not, create it with the default data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump(default_data, file, indent=2)

# Import the GraphQL schema after creating the data file
from views.schema import graphql_schema


class CustomGraphQLView(GraphQLView):
    """
    Custom GraphQL View to inject the LoanService into the GraphQL context.

    Inherits from Flask-GraphQL's `GraphQLView` to provide access to the `LoanService`
    for executing loan-related operations through the GraphQL API.

    Methods:
        get_context(self, request):
            - Overrides `get_context` to inject `LoanService` into the GraphQL context.
    """

    def get_context(self, request):
        """
        Overrides the get_context method to inject custom context for GraphQL operations.

        Args:
            request (Request): The Flask request object.

        Returns:
            dict: The context dictionary with the injected `LoanService`.
        """
        context = super().get_context(request)
        context.loan_service = (
            LoanService()
        )  # Inject LoanService here for GraphQL queries/mutations
        return context


# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the app


@app.route("/")
def home():
    """
    Home route that displays a welcome message.

    Returns:
        str: A simple welcome message.
    """
    return "Welcome to the Loan Application API"


# Add the custom GraphQL view with the injected LoanService context
app.add_url_rule(
    "/graphql",
    view_func=CustomGraphQLView.as_view(
        "graphql", schema=graphql_schema, graphiql=True
    ),
)

if __name__ == "__main__":
    """
    Main entry point for running the Flask application.

    Starts the Flask development server with debug mode enabled and accessible on all network interfaces.
    """
    app.run(host="0.0.0.0", debug=True)
