from collections import defaultdict
from statistics import mean

from models.finance import Transaction


SUBSCRIPTION_KEYWORDS = [
    "netflix",
    "spotify",
    "amazon prime",
    "prime video",
    "youtube premium",
    "hotstar",
    "disney+",
    "subscription",
    "membership",
    "ott"
]

BILL_KEYWORDS = [
    "internet",
    "wifi",
    "broadband",
    "mobile recharge",
    "phone bill",
    "electricity",
    "water bill"
]


def detect_subscriptions(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).order_by(Transaction.date.asc()).all()

    grouped = defaultdict(list)

    for transaction in transactions:
        title = transaction.title.strip().lower()
        grouped[title].append(transaction)

    subscriptions = []
    bills = []

    for title, records in grouped.items():

        records.sort(key=lambda x: x.date)

        is_subscription = any(
            keyword in title
            for keyword in SUBSCRIPTION_KEYWORDS
        )

        is_bill = any(
            keyword in title
            for keyword in BILL_KEYWORDS
        )

        if not is_subscription and not is_bill:
            continue

        amounts = [item.amount for item in records]
        average_amount = mean(amounts)

        intervals = []

        for i in range(1, len(records)):
            days = (
                records[i].date - records[i - 1].date
            ).days

            intervals.append(days)

        frequency = "Not Confirmed"
        confidence = "Low"

        if len(intervals) >= 2:
            average_interval = mean(intervals)

            if 25 <= average_interval <= 35:
                frequency = "Monthly"
                confidence = "Higher"

            elif 6 <= average_interval <= 8:
                frequency = "Weekly"
                confidence = "Higher"

            elif 85 <= average_interval <= 95:
                frequency = "Quarterly"
                confidence = "Higher"

        item = {
            "title": records[-1].title,
            "average_amount": round(average_amount, 2),
            "occurrences": len(records),
            "frequency": frequency,
            "confidence": confidence
        }

        if is_subscription:
            subscriptions.append(item)

        elif is_bill:
            bills.append(item)

    monthly_cost = sum(
        item["average_amount"]
        for item in subscriptions
        if item["frequency"] == "Monthly"
    )

    return {
        "success": True,
        "subscriptions": subscriptions,
        "bills": bills,
        "total_monthly_cost": round(monthly_cost, 2),
        "message": (
            "Subscription analysis completed."
            if subscriptions or bills
            else "No known subscription or bill keywords found."
        )
    }
