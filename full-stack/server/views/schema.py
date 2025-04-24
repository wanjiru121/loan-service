import graphene
from datetime import datetime
from config.constants import LOAN_PAYMENT_STATUS


class LoanPayment(graphene.ObjectType):
    """
    Represents an individual loan payment made by a borrower.
    """

    id = graphene.Int()
    loan_id = graphene.Int(name="loan_id")
    payment_date = graphene.Date(name="payment_date")
    due_date = graphene.Date(name="due_date")
    amount = graphene.Float()
    status = graphene.String()


class ExistingLoans(graphene.ObjectType):
    """
    Represents the details of an existing loan, including payments and remaining balance.
    """

    id = graphene.Int()
    name = graphene.String()
    start_date = graphene.Date(name="start_date")
    interest_rate = graphene.Float(name="interest_rate")
    principal = graphene.Int()
    due_dates = graphene.List(
        graphene.String,
        description="List of due dates for loan payments",
        name="due_dates",
    )
    expected_repayment_amount = graphene.Float(
        description="Expected total repayment amount including interest",
        name="expected_repayment_amount",
    )
    loan_payments = graphene.List(
        LoanPayment, description="List of loan payments made", name="loan_payments"
    )

    remaining_balance = graphene.Int(name="remaining_balance")
    months = graphene.Int()

    def resolve_loan_payments(self, info):
        """
        Resolves and returns all payments associated with this loan.
        """
        loan_service = info.context.loan_service
        return loan_service.get_payments_by_loan_id(self["id"])


class Query(graphene.ObjectType):
    """
    Defines the GraphQL queries for fetching loans and a specific loan.
    """

    loans = graphene.List(ExistingLoans)
    loan = graphene.Field(ExistingLoans, id=graphene.Int(required=True))

    def resolve_loans(self, info):
        """
        Resolves and returns all loans.
        """
        loan_service = info.context.loan_service
        return loan_service.get_all_loans()

    def resolve_loan(self, info, id):
        """
        Resolves and returns a specific loan by its ID.
        """
        loan_service = info.context.loan_service
        return loan_service.get_loan_by_id(id)


class CreateLoan(graphene.Mutation):
    """
    Mutation for creating a new loan.
    """

    class Arguments:
        name = graphene.String()
        interest_rate = graphene.Float(name="interest_rate")
        principal = graphene.Int()
        months = graphene.Int()

    loan = graphene.Field(ExistingLoans)

    def mutate(self, info, name, interest_rate, principal, months):
        """
        Creates a new loan and adds it to the loan service.
        """
        loan_service = info.context.loan_service
        new_loan = {
            "id": len(loan_service.loans) + 1,
            "name": name,
            "interest_rate": interest_rate,
            "principal": principal,
            "months": months,
        }

        loan_service.loans.append(new_loan)
        loan_service.save_data()
        return CreateLoan(loan=new_loan)


class MakePayment(graphene.Mutation):
    """
    Mutation for making a payment on an existing loan.
    """

    class Arguments:
        loan_id = graphene.Int(name="loan_id")
        payment_date = graphene.Date(name="payment_date")
        amount = graphene.Float()

    payment = graphene.Field(LoanPayment)

    def mutate(self, info, loan_id, payment_date, amount):
        """
        Processes the payment for the specified loan.
        """
        loan_service = info.context.loan_service

        if amount <= 0:
            raise Exception("Payment amount must be greater than zero.")

        loan = next(
            (loan for loan in loan_service.loans if loan["id"] == loan_id), None
        )
        if not loan:
            raise Exception("Loan ID does not exist.")

        remaining_balance = loan["remaining_balance"]

        if remaining_balance <= 0:
            raise Exception(
                "The loan is already fully paid. No further payments can be made."
            )

        if amount > remaining_balance:
            raise Exception(
                f"The payment amount exceeds the remaining loan balance of {remaining_balance:.2f}."
            )

        # Calculate the expected monthly installment
        expected_monthly_installment = (
            loan["expected_repayment_amount"] / loan["months"]
        )

        if amount != expected_monthly_installment:
            raise Exception(
                f"The payment amount must be equal to the expected monthly installment of {expected_monthly_installment:.2f}."
            )

        # Determine the due date for the current payment
        due_date_str = loan["due_dates"][len(loan_service.loan_payments)]
        due_date = datetime.fromisoformat(due_date_str).date()

        # Determine the payment status
        payment_status = LOAN_PAYMENT_STATUS["ON_TIME"]  # Default status is ON_TIME

        # If the payment is made after the due date but within grace period
        grace_period_days = 30  # Assuming grace period is 30 days

        due_date_obj = datetime.strptime(str(due_date), "%Y-%m-%d")
        payment_date_obj = datetime.strptime(str(payment_date), "%Y-%m-%d")

        if payment_date_obj > due_date_obj:
            if (payment_date_obj - due_date_obj).days <= grace_period_days:
                payment_status = LOAN_PAYMENT_STATUS["LATE"]
            else:
                payment_status = LOAN_PAYMENT_STATUS["DEFAULTED"]

        # Record the new payment
        new_payment = {
            "id": len(loan_service.loan_payments) + 1,
            "loan_id": loan_id,
            "payment_date": payment_date,
            "due_date": due_date,
            "amount": amount,
            "status": payment_status,
        }

        loan_service.loan_payments.append(new_payment)

        # Update the remaining balance
        loan["remaining_balance"] -= amount

        # Save data (this will persist the updated loan and payment details)
        loan_service.save_data()

        return MakePayment(payment=new_payment)


class Mutation(graphene.ObjectType):
    """
    Defines mutations for creating loans and making payments.
    """

    create_loan = CreateLoan.Field()
    make_payment = MakePayment.Field()


# Complete GraphQL schema with queries and mutations
graphql_schema = graphene.Schema(query=Query, mutation=Mutation)
