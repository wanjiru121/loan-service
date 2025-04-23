import pytest
from datetime import date
from graphene.test import Client
from views.schema import graphql_schema
from services.loan_service import LoanService
from utils.helpers import generate_due_dates, calculate_expected_repayment
from config.constants import LOAN_PAYMENT_STATUS


# Context class that holds the loan service instance to be used in tests
class Context:
    def __init__(self, loan_service):
        """
        Initializes the context with a loan service instance.

        :param loan_service: An instance of LoanService for performing loan operations.
        """
        self.loan_service = loan_service


# Fixture to create and return a LoanService instance with some initial loan data
@pytest.fixture
def loan_service():
    """
    A pytest fixture that sets up a LoanService with sample loan and payment data.

    :return: An instance of LoanService with pre-configured loan and payment data.
    """
    service = LoanService()

    # Adding initial loan data
    service.loans = [
        {
            "id": 1,
            "name": "Loan 1",
            "interest_rate": 5.0,
            "principal": 1000,
            "start_date": "2025-2-28",
            "remaining_balance": calculate_expected_repayment(1000, 5.0, 12) - 500,
            "months": 10,
            "expected_repayment_amount": calculate_expected_repayment(1000, 5.0, 12),
            "due_dates": generate_due_dates("2025-5-1", 10),
        },
        {
            "id": 2,
            "name": "Loan 2",
            "interest_rate": 7.0,
            "principal": 2000,
            "start_date": "2025-6-1",
            "remaining_balance": calculate_expected_repayment(2000, 7.0, 5) - 0,
            "months": 5,
            "expected_repayment_amount": calculate_expected_repayment(2000, 7.0, 5),
            "due_dates": generate_due_dates("2025-6-1", 5),
        },
    ]

    # Adding initial payment data
    service.loan_payments = [
        {
            "id": 1,
            "loan_id": 1,
            "payment_date": date(2025, 3, 1),
            "due_date": date(2025, 2, 1),
            "amount": 500,
            "status": LOAN_PAYMENT_STATUS["ON_TIME"],
        }
    ]
    return service


# Fixture to create and return a GraphQL client instance
@pytest.fixture
def graphql_client():
    """
    A pytest fixture that creates and returns a GraphQL client.

    :return: An instance of the GraphQL client connected to the schema.
    """
    return Client(graphql_schema)


# Test for querying loans using GraphQL
def test_query_loans(graphql_client, loan_service):
    """
    Test case to query all loans and ensure the response matches the expected data.

    :param graphql_client: The GraphQL client for executing queries.
    :param loan_service: The loan service instance to be used in the query.
    """
    query = """
    query {
        loans {
            id
            name
            interest_rate
            principal
            remaining_balance
        }
    }
    """
    # Execute the query with the loan service in the context
    response = graphql_client.execute(query, context_value=Context(loan_service))

    # Assertions to ensure the query response is valid and matches expectations
    assert response is not None
    assert "data" in response
    assert response["data"]["loans"] == [
        {
            "id": 1,
            "name": "Loan 1",
            "interest_rate": 5.0,
            "principal": 1000,
            "remaining_balance": 1100,
        },
        {
            "id": 2,
            "name": "Loan 2",
            "interest_rate": 7.0,
            "principal": 2000,
            "remaining_balance": 2700,
        },
    ]


# Test for querying a specific loan by ID
def test_query_loan_by_id(graphql_client, loan_service):
    """
    Test case to query a single loan by its ID and ensure the response matches the expected data.

    :param graphql_client: The GraphQL client for executing queries.
    :param loan_service: The loan service instance to be used in the query.
    """
    query = """
    query getLoan($id: Int!) {
        loan(id: $id) {
            id
            name
            interest_rate
            principal
            remaining_balance
        }
    }
    """
    variables = {"id": 1}
    response = graphql_client.execute(
        query, variable_values=variables, context_value=Context(loan_service)
    )

    # Assertions to ensure the query response is valid and matches expectations
    assert response is not None
    assert "data" in response
    assert response["data"]["loan"] == {
        "id": 1,
        "name": "Loan 1",
        "interest_rate": 5.0,
        "principal": 1000,
        "remaining_balance": 1100,
    }


# Test for creating a new loan via a mutation
def test_create_loan(graphql_client, loan_service):
    """
    Test case to create a new loan via a GraphQL mutation and ensure the loan is created successfully.

    :param graphql_client: The GraphQL client for executing mutations.
    :param loan_service: The loan service instance to be used in the mutation.
    """
    mutation = """
    mutation createLoan($name: String!, $interest_rate: Float!, $principal: Int!, $months: Int!) {
        createLoan(name: $name, interest_rate: $interest_rate, principal: $principal, months: $months) {
            loan {
                id
                name
                interest_rate
                principal
                months
            }
        }
    }
    """
    variables = {
        "name": "New Loan",
        "interest_rate": 5.5,
        "principal": 1500,
        "months": 10
    }
    response = graphql_client.execute(
        mutation, variable_values=variables, context_value=Context(loan_service)
    )

    # Assertions to ensure the mutation response is valid and matches expectations
    assert response is not None
    assert "data" in response
    assert response["data"]["createLoan"]["loan"] == {
        "id": 3,
        "name": "New Loan",
        "interest_rate": 5.5,
        "principal": 1500,
        "months": 10
    }


# Test for making a payment on a loan via mutation
def test_make_payment(graphql_client, loan_service):
    """
    Test case to make a payment on a loan via a mutation and ensure the payment is recorded.

    :param graphql_client: The GraphQL client for executing mutations.
    :param loan_service: The loan service instance to be used in the mutation.
    """
    mutation = """
    mutation makePayment($loan_id: Int!, $payment_date: Date!, $amount: Float!) {
        makePayment(loan_id: $loan_id, payment_date: $payment_date, amount: $amount) {
            payment {
                id
                loan_id
                payment_date
                amount
            }
        }
    }
    """
    variables = {"loan_id": 1, "payment_date": "2025-04-01", "amount": 160}
    response = graphql_client.execute(
        mutation, variable_values=variables, context_value=Context(loan_service)
    )

    # Assertions to ensure the payment was processed correctly
    assert response is not None
    assert "data" in response
    assert response["data"]["makePayment"]["payment"] == {
        "id": 2,
        "loan_id": 1,
        "payment_date": "2025-04-01",
        "amount": 160,
    }


# Test for making a payment that exceeds the loan balance
def test_make_payment_exceeds_balance(graphql_client, loan_service):
    """
    Test case to ensure an error is raised if a payment exceeds the remaining loan balance.

    :param graphql_client: The GraphQL client for executing mutations.
    :param loan_service: The loan service instance to be used in the mutation.
    """
    mutation = """
    mutation makePayment($loan_id: Int!, $payment_date: Date!, $amount: Float!) {
        makePayment(loan_id: $loan_id, payment_date: $payment_date, amount: $amount) {
            payment {
                id
                loan_id
                payment_date
                amount
            }
        }
    }
    """
    variables = {"loan_id": 2, "payment_date": "2025-04-01", "amount": 2000}
    response = graphql_client.execute(
        mutation, variable_values=variables, context_value=Context(loan_service)
    )

    # Assertions to ensure the error is returned when payment exceeds balance
    assert response is not None
    assert "errors" in response
    assert (
        "The payment amount must be equal to the expected monthly installment of 540.00."
        in str(response["errors"])
    )


# Test for making a payment with an invalid (negative) amount
def test_make_payment_invalid_amount(graphql_client, loan_service):
    """
    Test case to ensure an error is raised if the payment amount is negative.

    :param graphql_client: The GraphQL client for executing mutations.
    :param loan_service: The loan service instance to be used in the mutation.
    """
    mutation = """
    mutation makePayment($loan_id: Int!, $payment_date: Date!, $amount: Float!) {
        makePayment(loan_id: $loan_id, payment_date: $payment_date, amount: $amount) {
            payment {
                id
                loan_id
                payment_date
                amount
            }
        }
    }
    """
    variables = {"loan_id": 1, "payment_date": "2025-04-01", "amount": -100}
    response = graphql_client.execute(
        mutation, variable_values=variables, context_value=Context(loan_service)
    )

    # Assertions to ensure the error is returned for invalid payment amount
    assert response is not None
    assert "errors" in response
    assert "Payment amount must be greater than zero" in str(response["errors"])
