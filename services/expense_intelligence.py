from collections import defaultdict
from statistics import mean, stdev

from models.finance import Transaction


def analyze_expenses(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).order_by(Transaction.date.asc()).all()

    if not transactions:
        return {
            "success": False,
            "message": "No expense records available.",
            "total_expense": 0,
            "categories": [],
            "anomalies": [],
            "insights": []
        }

    total_expense = sum(t.amount for t in transactions)

    category_data = defaultdict(list)

    for transaction in transactions:
        category_data[transaction.category].append(
            transaction.amount
        )

    categories = []

    for category, amounts in category_data.items():
        total = sum(amounts)

        categories.append({
            "name": category,
            "total": round(total, 2),
            "average": round(mean(amounts), 2),
            "count": len(amounts),
            "percentage": round(
                (total / total_expense) * 100, 2
            ) if total_expense > 0 else 0
        })

    categories.sort(
        key=lambda item: item["total"],
        reverse=True
    )

    # Anomaly Detection
    anomalies = []
    all_amounts = [t.amount for t in transactions]

    if len(all_amounts) >= 3:
        average = mean(all_amounts)
        deviation = stdev(all_amounts)

        for transaction in transactions:
            if deviation > 0 and (
                transaction.amount > average + 2 * deviation
            ):
                anomalies.append({
                    "title": transaction.title,
                    "amount": round(transaction.amount, 2),
                    "category": transaction.category,
                    "date": transaction.date.strftime("%d %b %Y"),
                    "message": "Unusually high expense detected."
                })

    # Insights
    insights = []

    if categories:
        highest = categories[0]

        insights.append(
            f"{highest['name']} is your highest spending category."
        )

        if highest["percentage"] >= 50:
            insights.append(
                f"{highest['percentage']}% of your recorded expenses "
                f"are going to {highest['name']}."
            )

    if len(transactions) < 5:
        insights.append(
            "More expense records are needed for reliable pattern analysis."
        )
    else:
        insights.append(
            "Keep recording expenses regularly to improve analysis."
        )

    if anomalies:
        insights.append(
            f"{len(anomalies)} unusually high expense record(s) detected. "
            "Review them to check whether they are expected."
        )
    else:
        insights.append(
            "No unusually high expenses were detected by the current rule."
        )

    return {
        "success": True,
        "total_expense": round(total_expense, 2),
        "transaction_count": len(transactions),
        "categories": categories,
        "anomalies": anomalies,
        "insights": insights
    }