
from models.finance import Transaction
from collections import defaultdict


def get_budget_recommendations(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).all()

    category_totals = defaultdict(float)
    category_counts = defaultdict(int)

    for transaction in transactions:
        category_totals[transaction.category] += transaction.amount
        category_counts[transaction.category] += 1

    recommendations = []

    for category, total in category_totals.items():

        count = category_counts[category]
        average = total / count if count else 0

        suggested_budget = round(average * 0.90, 2)
        possible_saving = round(average - suggested_budget, 2)

        recommendations.append({
            "category": category,
            "average_expense": round(average, 2),
            "suggested_budget": suggested_budget,
            "possible_saving": possible_saving
        })

    return recommendations
