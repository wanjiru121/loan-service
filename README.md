# Loan Service Documentation

## Project Overview
The Loan Service is a backend system designed to manage loans and loan payments. It loads, processes, and stores loan data, evaluates payment statuses, and provides utility functions for querying loan-related information. The system operates using a JSON file as its data source and applies various status checks to determine loan repayment conditions.

## Tech Stack
- **Language:** Python 3, JavaScript (React)
- **Libraries:** `os`, `json`, `datetime`, `graphene`, `Flask`, `flask_graphql`, `flask_cors`
- **Data Storage:** JSON file (`/tmp/loan_data.json`)
- **GraphQL Support:** GraphQL schema for loan queries and mutations
- **Web Framework:** Flask, React

## System Architecture
### Components:
1. **Loan Data Management**: Handles loading and saving loan and payment data.
2. **Payment Status Calculation**: Determines if a loan is on time, late, defaulted, unpaid, or partially paid.
3. **GraphQL API**: Exposes loan and payment data via GraphQL queries and mutations.
4. **Query Functions**: Fetches loans and payments by ID.
5. **Flask API**: Provides an endpoint for serving the GraphQL schema.
6. **Loan Calculator Frontend**: Allows users to calculate loan payments based on principal, interest rate, and duration.
7. **Loan Payment Tracking Frontend**: Displays loan details and payment history.

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

### 4. Loan Calculator Frontend
A React-based Loan Calculator allows users to compute interest and total payments.

### 5. Loan Payment Tracking Frontend
A React-based Loan Payment Tracking component displays loan details, principal, interest rate, due date, and payment history.

## Flask API Implementation
### 1. Flask Application Setup
The Loan Service is implemented as a Flask application, exposing GraphQL endpoints.

## Future Improvements
- **Database Integration:** Replace JSON storage with a relational database like PostgreSQL.
- **API Development:** Extend GraphQL with authentication and more advanced filtering.
- **Frontend Enhancements:** Improve the Loan Calculator UI with better UX and visualization features.
- **Enhanced Loan Tracking:** Provide more detailed reports and charts for payments and overdue loans.

