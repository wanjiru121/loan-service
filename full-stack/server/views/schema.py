import graphene


class LoanPayment(graphene.ObjectType):
    """
    Represents an individual loan payment made by a borrower.
    """

    id = graphene.Int()
    loan_id = graphene.Int(name="loan_id")
    payment_date = graphene.Date(name="payment_date")
    amount = graphene.Float()


class ExistingLoans(graphene.ObjectType):
    """
    Represents the details of an existing loan, including payments and remaining balance.
    """

    id = graphene.Int()
    name = graphene.String()
    interest_rate = graphene.Float(name="interest_rate")
    principal = graphene.Int()
    due_date = graphene.Date(name="due_date")
    loan_payments = graphene.List(
        LoanPayment, description="List of loan payments", name="loan_payments"
    )
    payment_status = graphene.String(
        description="Payment status of the loan", name="payment_status"
    )
    remaining_balance = graphene.Float(
        description="Remaining loan balance", name="remaining_balance"
    )

    def resolve_loan_payments(self, info):
        """
        Resolves and returns all payments associated with this loan.
        """
        loan_service = info.context.loan_service
        return loan_service.get_payments_by_loan_id(self["id"])

    def resolve_payment_status(self, info):
        """
        Resolves and returns the payment status of the loan.
        """
        loan_service = info.context.loan_service
        return loan_service.get_payment_status(self)

    def resolve_remaining_balance(self, info):
        """
        Resolves and calculates the remaining balance of the loan.
        """
        loan_service = info.context.loan_service
        total_paid = sum(
            payment["amount"]
            for payment in loan_service.get_payments_by_loan_id(self["id"])
        )
        return max(0, self["principal"] - total_paid)


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
        due_date = graphene.Date(name="due_date")

    loan = graphene.Field(ExistingLoans)

    def mutate(self, info, name, interest_rate, principal, due_date):
        """
        Creates a new loan and adds it to the loan service.
        """
        loan_service = info.context.loan_service
        new_loan = {
            "id": len(loan_service.loans) + 1,
            "name": name,
            "interest_rate": interest_rate,
            "principal": principal,
            "due_date": due_date,
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

        new_payment = {
            "id": len(loan_service.loan_payments) + 1,
            "loan_id": loan_id,
            "payment_date": payment_date,
            "amount": amount,
        }

        loan_service.loan_payments.append(new_payment)
        loan["remaining_balance"] -= amount
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
