import os
import json
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from services.loan_service import LoanService

# Define path to the data file
DATA_FILE = "/tmp/loan_data.json"

# Default data to use if file doesn't exist
default_data = {
    "loans": [
        {
            "id": 1,
            "name": "Tom's Loan",
            "interest_rate": 5.0,
            "principal": 10000,
            "due_date": "2025-03-01",
            "remaining_balance": 1000,
        },
        {
            "id": 2,
            "name": "Chris Wailaka",
            "interest_rate": 3.5,
            "principal": 500000,
            "due_date": "2025-03-01",
            "remaining_balance": 20000,
        },
        {
            "id": 3,
            "name": "NP Mobile Money",
            "interest_rate": 4.5,
            "principal": 30000,
            "due_date": "2025-03-01",
            "remaining_balance": 0,
        },
        {
            "id": 4,
            "name": "Esther's Autoparts",
            "interest_rate": 1.5,
            "principal": 40000,
            "due_date": "2025-03-01",
            "remaining_balance": 40000,
        },
    ],
    "loan_payments": [
        {"id": 1, "loan_id": 1, "payment_date": "2024-03-04", "amount": 9000},
        {"id": 2, "loan_id": 2, "payment_date": "2024-03-15", "amount": 30000},
        {"id": 3, "loan_id": 3, "payment_date": "2024-04-05", "amount": 30000},
    ],
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
