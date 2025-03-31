# Loan Service Documentation

## Project Overview
The Loan Service is a backend system designed to manage loans and loan payments. It loads, processes, and stores loan data, evaluates payment statuses, and provides utility functions for querying loan-related information. The system operates using a JSON file as its data source and applies various status checks to determine loan repayment conditions.

## Tech Stack
- **Language:** Python 3
- **Libraries:** `os`, `json`, `datetime`, `graphene`, `Flask`, `flask_graphql`, `flask_cors`
- **Data Storage:** JSON file (`/tmp/loan_data.json`)
- **GraphQL Support:** GraphQL schema for loan queries and mutations
- **Web Framework:** Flask

## System Architecture
### Components:
1. **Loan Data Management**: Handles loading and saving loan and payment data.
2. **Payment Status Calculation**: Determines if a loan is on time, late, defaulted, unpaid, or partially paid.
3. **GraphQL API**: Exposes loan and payment data via GraphQL queries and mutations.
4. **Query Functions**: Fetches loans and payments by ID.
5. **Flask API**: Provides an endpoint for serving the GraphQL schema.

## Key Features
### 1. Loan Data Management
- **Load Data**: Reads loan and payment records from a JSON file.
- **Save Data**: Writes updated loan and payment records back to the JSON file.
- **Error Handling**: Manages various exceptions such as missing files, invalid JSON, and incorrect date formats.

### 2. Loan Payment Status Evaluation
- Determines if payments are:
  - **On Time**: Paid on or before the due date.
  - **Late**: Paid after the due date but within the grace period.
  - **Defaulted**: Not paid after the grace period.
  - **Unpaid**: No payment made.
  - **Partially Paid**: Paid but not in full.
  - **Late Partially Paid**: Partially paid but late.
  - **Defaulted Partially Paid**: Partially paid but defaulted.

### 3. Loan & Payment Querying
- Fetches all loans.
- Retrieves loans by their unique ID.
- Gets all payments related to a specific loan.

## Flask API Implementation
### 1. Flask Application Setup
The Loan Service is implemented as a Flask application, exposing GraphQL endpoints.

#### Initialization
```python
import os
import json
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from services.loan_service import LoanService

# Define path to the data file
DATA_FILE = "/tmp/loan_data.json"

# Default data to use if file doesn't exist
default_data = { "loans": [...], "loan_payments": [...] }

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump(default_data, file, indent=2)

# Import the GraphQL schema
from views.schema import graphql_schema

# Custom GraphQL View
class CustomGraphQLView(GraphQLView):
    def get_context(self, request):
        context = super().get_context(request)
        context.loan_service = LoanService()
        return context

# Initialize Flask application
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Welcome to the Loan Application API"

# GraphQL route
app.add_url_rule(
    "/graphql",
    view_func=CustomGraphQLView.as_view(
        "graphql", schema=graphql_schema, graphiql=True
    ),
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

### 2. Flask API Endpoints
- **`/`**: Returns a welcome message.
- **`/graphql`**: Serves the GraphQL API, enabling loan-related queries and mutations.

## GraphQL API Implementation
### 1. Object Types
#### LoanPayment
Represents an individual loan payment.
```python
class LoanPayment(graphene.ObjectType):
    id = graphene.Int()
    loan_id = graphene.Int(name="loan_id")
    payment_date = graphene.Date(name="payment_date")
    amount = graphene.Float()
```
#### ExistingLoans
Represents an existing loan, including payments and remaining balance.
```python
class ExistingLoans(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    interest_rate = graphene.Float(name="interest_rate")
    principal = graphene.Int()
    due_date = graphene.Date(name="due_date")
    loan_payments = graphene.List(LoanPayment, name="loan_payments")
    payment_status = graphene.String(name="payment_status")
    remaining_balance = graphene.Float(name="remaining_balance")
```
### 2. Query Resolvers
#### Loan Queries
```python
class Query(graphene.ObjectType):
    loans = graphene.List(ExistingLoans)
    loan = graphene.Field(ExistingLoans, id=graphene.Int(required=True))
```
#### Loan Mutation
```python
class CreateLoan(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        interest_rate = graphene.Float(name="interest_rate")
        principal = graphene.Int()
        due_date = graphene.Date(name="due_date")
    loan = graphene.Field(ExistingLoans)
```
#### Make Payment Mutation
```python
class MakePayment(graphene.Mutation):
    class Arguments:
        loan_id = graphene.Int(name="loan_id")
        payment_date = graphene.Date(name="payment_date")
        amount = graphene.Float()
    payment = graphene.Field(LoanPayment)
```
### 3. Schema Definition
```python
class Mutation(graphene.ObjectType):
    create_loan = CreateLoan.Field()
    make_payment = MakePayment.Field()

graphql_schema = graphene.Schema(query=Query, mutation=Mutation)
```

## Challenges & Solutions
### Challenge: Handling Date Formats in JSON
- **Issue:** JSON does not support `datetime.date` objects.
- **Solution:** Convert date objects to ISO format (`YYYY-MM-DD`) before saving and parse them back when loading.

### Challenge: Handling Missing or Corrupt Data
- **Issue:** If required fields are missing or contain invalid data, it can cause crashes.
- **Solution:** Implement validation checks and exception handling when reading/writing JSON.

## Future Improvements
- **Database Integration:** Replace JSON storage with a relational database like PostgreSQL.
- **API Development:** Extend GraphQL with authentication and more advanced filtering.

---
