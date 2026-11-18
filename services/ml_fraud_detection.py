import numpy as np
from sklearn.ensemble import IsolationForest

from models.finance import Transaction


def detect_ml_fraud(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        transaction_type="expense"
    ).order_by(Transaction.date.asc()).all()

    if len(transactions) < 10:
        return {
            "success": False,
            "message": "ML analysis needs at least 10 expense transactions.",
            "transaction_count": len(transactions),
            "alerts": [],
            "suspicious_count": 0
        }

    features = []

    for transaction in transactions:
        features.append([
            float(transaction.amount),
            transaction.date.hour,
            transaction.date.weekday()
        ])

    X = np.array(features)

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    predictions = model.fit_predict(X)

    alerts = []

    for transaction, prediction in zip(
        transactions, predictions
    ):
        if prediction == -1:
            alerts.append({
                "title": transaction.title,
                "amount": round(transaction.amount, 2),
                "category": transaction.category,
                "date": transaction.date.strftime("%d %b %Y"),
                "message": "ML model identified an unusual transaction."
            })

    return {
        "success": True,
        "transaction_count": len(transactions),
        "suspicious_count": len(alerts),
        "alerts": alerts,
        "message": (
            "Unusual patterns detected by ML model."
            if alerts
            else "No unusual patterns detected by ML model."
        )
    }