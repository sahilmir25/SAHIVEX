from statistics import mean, stdev

from models.finance import Transaction


def detect_fraud(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).order_by(Transaction.date.asc()).all()

    if not transactions:
        return {
            "success": False,
            "transaction_count": 0,
            "suspicious_count": 0,
            "risk_score": 0,
            "risk_level": "Insufficient Data",
            "alerts": [],
            "message": "No expense transactions available."
        }

    amounts = [
        transaction.amount
        for transaction in transactions
    ]

    average_amount = mean(amounts)

    deviation = (
        stdev(amounts)
        if len(amounts) >= 2 else 0
    )

    alerts = []
    suspicious_count = 0

    for transaction in transactions:

        reasons = []
        risk = 0

        if (
            average_amount > 0
            and transaction.amount > average_amount * 3
        ):
            reasons.append(
                "Transaction amount is unusually high."
            )
            risk += 40

        if (
            deviation > 0
            and transaction.amount > average_amount + 2 * deviation
        ):
            reasons.append(
                "Transaction is outside the usual spending pattern."
            )
            risk += 30

        if transaction.amount <= 0:
            reasons.append(
                "Invalid transaction amount."
            )
            risk += 50

        if reasons:
            suspicious_count += 1

            alerts.append({
                "title": transaction.title,
                "amount": round(transaction.amount, 2),
                "category": transaction.category,
                "date": transaction.date.strftime("%d %b %Y"),
                "risk_score": min(risk, 100),
                "reasons": reasons
            })

    risk_score = round(
        (suspicious_count / len(transactions)) * 100,
        2
    )

    if risk_score >= 50:
        risk_level = "High"
    elif risk_score >= 20:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        "success": True,
        "transaction_count": len(transactions),
        "suspicious_count": suspicious_count,
        "average_amount": round(average_amount, 2),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "alerts": alerts,
        "message": (
            "Suspicious transaction patterns detected."
            if alerts
            else "No suspicious patterns detected by current rules."
        )
    }