from collections import defaultdict

from models.finance import Transaction


def detect_recurring_expenses(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).order_by(Transaction.date.asc()).all()

    if not transactions:
        return {
            "success": False,
            "message": "No expense records available.",
            "recurring_expenses": [],
            "total_recurring": 0
        }

    grouped_expenses = defaultdict(list)

    for transaction in transactions:
        key = (
            transaction.title.strip().lower(),
            transaction.category.strip().lower()
        )
        grouped_expenses[key].append(transaction)

    recurring_expenses = []

    for key, records in grouped_expenses.items():

        if len(records) < 2:
            continue

        amounts = [record.amount for record in records]
        average_amount = sum(amounts) / len(amounts)

        recurring_expenses.append({
            "title": records[0].title,
            "category": records[0].category,
            "occurrences": len(records),
            "average_amount": round(average_amount, 2),
            "total_amount": round(sum(amounts), 2),
            "message": "This expense appears more than once."
        })

    recurring_expenses.sort(
        key=lambda item: item["total_amount"],
        reverse=True
    )

    total_recurring = sum(
        item["total_amount"] for item in recurring_expenses
    )

    return {
        "success": True,
        "recurring_expenses": recurring_expenses,
        "total_recurring": round(total_recurring, 2)
    }
