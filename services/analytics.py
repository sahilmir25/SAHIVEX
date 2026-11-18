
from models.finance import Transaction
from collections import defaultdict


def get_financial_summary(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id
    ).order_by(
        Transaction.date.asc()
    ).all()

    total_income = 0
    total_expense = 0

    monthly_data = defaultdict(
        lambda: {
            "income": 0,
            "expense": 0
        }
    )

    categories = defaultdict(float)

    for t in transactions:

        month = t.date.strftime("%Y-%m")

        if t.transaction_type == "income":
            total_income += t.amount
            monthly_data[month]["income"] += t.amount

        elif t.transaction_type == "expense":
            total_expense += t.amount
            monthly_data[month]["expense"] += t.amount
            categories[t.category] += t.amount

    balance = total_income - total_expense

    savings_rate = (
        (balance / total_income) * 100
        if total_income > 0 else 0
    )

    if total_income <= 0:
        health_score = 0
        health_status = "Insufficient Data"
    else:
        health_score = round(
            max(0, min(100, savings_rate)), 2
        )

        if savings_rate >= 30:
            health_status = "Healthy Savings"
        elif savings_rate >= 10:
            health_status = "Moderate Savings"
        elif savings_rate >= 0:
            health_status = "Low Savings"
        else:
            health_status = "High Risk"

    highest_category = (
        max(categories, key=categories.get)
        if categories else "No Expenses"
    )

    highest_amount = (
        categories[highest_category]
        if categories else 0
    )

    months = sorted(monthly_data.keys())

    monthly_income = [
        round(monthly_data[m]["income"], 2)
        for m in months
    ]

    monthly_expense = [
        round(monthly_data[m]["expense"], 2)
        for m in months
    ]

    monthly_savings = [
        round(
            monthly_data[m]["income"] -
            monthly_data[m]["expense"], 2
        )
        for m in months
    ]

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(balance, 2),
        "savings_rate": round(savings_rate, 2),
        "health_score": health_score,
        "health_status": health_status,
        "categories": dict(categories),
        "highest_category": highest_category,
        "highest_amount": round(highest_amount, 2),
        "months": months,
        "monthly_income": monthly_income,
        "monthly_expense": monthly_expense,
        "monthly_savings": monthly_savings
    }
