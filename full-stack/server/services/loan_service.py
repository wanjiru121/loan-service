import os
import json
import datetime


class LoanService:
    """
    LoanService is a class to manage loans and loan payments.
    It supports loading and saving loan data, and querying loan-related information.

    Attributes:
        data_file (str): Path to the JSON file storing loan data.
        loans (list): List of loan dictionaries loaded from the JSON file.
        loan_payments (list): List of loan payment dictionaries loaded from the JSON file.
    """

    def __init__(self, data_file="/tmp/loan_data.json"):
        """
        Initializes the LoanService with the specified data file.

        Args:
            data_file (str): Path to the JSON file where loan and payment data is stored.
        """
        self.data_file = data_file
        self.loans = []  # List to hold loan data
        self.loan_payments = []  # List to hold loan payment data
        self.load_data()  # Load data from the file

    def load_data(self):
        """
        Loads loan and payment data from the specified JSON file.
        Converts date strings in the file to datetime.date objects(For accurate comparisons).

        Raises:
            FileNotFoundError: If the data file does not exist.
            ValueError: If the file is missing required fields or contains invalid data.
            json.JSONDecodeError: If the file content is not valid JSON.
        """
        if not os.path.exists(self.data_file):
            raise FileNotFoundError(f"The data file '{self.data_file}' does not exist.")

        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)

            # Check for required fields in the data
            if "loans" not in data or "loan_payments" not in data:
                raise ValueError("Missing 'loans' or 'loan_payments' in data file.")

            # Convert date strings to datetime.date objects for payments
            for payment in data["loan_payments"]:
                try:
                    payment["payment_date"] = datetime.date.fromisoformat(
                        payment["payment_date"]
                    )
                    payment["due_date"] = datetime.date.fromisoformat(
                        payment["due_date"]
                    )
                except ValueError:
                    raise ValueError(
                        f"Invalid payment_date or due_date format for payment {payment['id']}. Skipping payment."
                    )

            self.loans = data["loans"]
            self.loan_payments = data["loan_payments"]

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{self.data_file}' was not found.")
        except json.JSONDecodeError:
            raise ValueError(
                f"Failed to parse the JSON data in the file '{self.data_file}'."
            )
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Unexpected error while loading data: {str(e)}")

    def save_data(self):
        """
        Saves the current loan and payment data to the specified JSON file.
        Converts datetime.date objects back to ISO format strings.

        Raises:
            PermissionError: If there is a permission issue while saving the data.
            IOError: If there is an I/O error while writing to the file.
            json.JSONDecodeError: If the data cannot be properly encoded to JSON format.
        """
        try:
            # Ensure there is data to save
            if not self.loans or not self.loan_payments:
                raise ValueError("No loans or loan payments to save.")

            # Prepare the data for saving by converting date objects back to strings
            data = {
                "loans": [
                    loan
                    for loan in self.loans
                ],
                "loan_payments": [
                    {
                        **payment,
                        "payment_date": payment["payment_date"].isoformat(),
                        "due_date": payment["due_date"].isoformat(),
                    }
                    for payment in self.loan_payments
                ],
            }

            # Create directories if they do not exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

            with open(self.data_file, "w") as file:
                json.dump(data, file, indent=4)

        except PermissionError:
            raise PermissionError(
                f"Permission denied when trying to write to '{self.data_file}'."
            )
        except IOError as e:
            raise IOError(f"IO error occurred while saving data: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format encountered while saving data.")
        except Exception as e:
            raise Exception(f"Unexpected error while saving data: {str(e)}")

    def get_all_loans(self):
        """
        Retrieves all the loans in the system.

        Returns:
            list: A list of all loan dictionaries.
        """
        return self.loans

    def get_loan_by_id(self, loan_id):
        """
        Retrieves a loan by its unique ID.

        Args:
            loan_id (str): The unique ID of the loan to retrieve.

        Returns:
            dict: The loan with the specified ID, or None if not found.
        """
        return next((loan for loan in self.loans if loan["id"] == loan_id), None)

    def get_payments_by_loan_id(self, loan_id):
        """
        Retrieves all payments made for a specific loan.

        Args:
            loan_id (str): The unique ID of the loan to retrieve payments for.

        Returns:
            list: A list of payments associated with the specified loan.
        """
        return [p for p in self.loan_payments if p["loan_id"] == loan_id]
