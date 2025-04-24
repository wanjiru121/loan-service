from datetime import datetime, timedelta


def generate_due_dates(start_date, months):
    due_dates = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")

    for _ in range(months):
        due_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date = current_date + timedelta(days=30)

    return due_dates


def calculate_expected_repayment(principal, interest_rate, months):
    total_interest = principal * (interest_rate / 100) * months
    expected_amount = principal + total_interest
    return round(expected_amount)
