from collections import defaultdict
from statistics import mean

from models.finance import Transaction


def analyze_financial_behavior(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).order_by(Transaction.date.asc()).all()

    if not transactions:
        return {
            "success": False,
            "message": "No expense transactions available.",
            "transaction_count": 0,
            "category_data": [],
            "weekday_expense": 0,
            "weekend_expense": 0,
            "average_transaction": 0,
            "highest_category": "N/A",
            "insights": []
        }

    category_totals = defaultdict(float)
    weekday_total = 0
    weekend_total = 0
    amounts = []

    for transaction in transactions:

        amount = float(transaction.amount)
        amounts.append(amount)

        category_totals[transaction.category] += amount

        if transaction.date.weekday() >= 5:
            weekend_total += amount
        else:
            weekday_total += amount

    category_data = [
        {
            "category": category,
            "amount": round(amount, 2)
        }
        for category, amount in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]

    highest_category = category_data[0]["category"]
    average_transaction = mean(amounts)
    total_expense = sum(amounts)
    highest_amount = category_data[0]["amount"]

    highest_percentage = (
        highest_amount / total_expense * 100
        if total_expense > 0 else 0
    )

    insights = []

    insights.append(
        f"{highest_category} is your highest spending category."
    )

    insights.append(
        f"{highest_percentage:.1f}% of your expenses "
        f"belong to {highest_category}."
    )

    if weekend_total > weekday_total:
        insights.append(
            "Your weekend expenses are higher than weekday expenses."
        )
    else:
        insights.append(
            "Your weekday expenses are higher than weekend expenses."
        )

    return {
        "success": True,
        "transaction_count": len(transactions),
        "total_expense": round(total_expense, 2),
        "category_data": category_data,
        "weekday_expense": round(weekday_total, 2),
        "weekend_expense": round(weekend_total, 2),
        "average_transaction": round(average_transaction, 2),
        "highest_category": highest_category,
        "insights": insights
    }