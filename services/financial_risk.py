from models.finance import Transaction


def analyze_financial_risk(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id
    ).all()

    total_income = sum(
        t.amount for t in transactions
        if t.transaction_type == "income"
    )

    total_expense = sum(
        t.amount for t in transactions
        if t.transaction_type == "expense"
    )

    balance = total_income - total_expense

    risk_score = 0
    risk_factors = []
    recommendations = []

    if total_income <= 0:
        risk_score += 40

        risk_factors.append(
            "No income records available."
        )

        recommendations.append(
            "Record your income to improve financial analysis."
        )

        expense_ratio = 0

    else:
        expense_ratio = (
            total_expense / total_income
        ) * 100

        if expense_ratio >= 100:
            risk_score += 40

            risk_factors.append(
                "Your expenses are equal to or higher than income."
            )

            recommendations.append(
                "Reduce unnecessary expenses immediately."
            )

        elif expense_ratio >= 80:
            risk_score += 25

            risk_factors.append(
                "A large portion of your income is being spent."
            )

            recommendations.append(
                "Try to reduce your monthly spending."
            )

        elif expense_ratio >= 60:
            risk_score += 15

            risk_factors.append(
                "Your spending level is relatively high."
            )

            recommendations.append(
                "Monitor your expenses and increase savings."
            )

        else:
            recommendations.append(
                "Your recorded expense-to-income ratio looks manageable."
            )

    if balance < 0:
        risk_score += 30

        risk_factors.append(
            "Your recorded expenses exceed your income."
        )

    if total_income > 0:
        savings_rate = (
            balance / total_income
        ) * 100

        if savings_rate < 10:
            risk_score += 20

            risk_factors.append(
                "Your savings rate is below 10%."
            )

            recommendations.append(
                "Try building a regular savings habit."
            )

    else:
        savings_rate = 0

    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        risk_level = "Critical"
        risk_message = "Your financial records indicate high risk."

    elif risk_score >= 45:
        risk_level = "High"
        risk_message = "Your financial situation needs attention."

    elif risk_score >= 20:
        risk_level = "Moderate"
        risk_message = "Some financial areas need improvement."

    else:
        risk_level = "Low"
        risk_message = "Your recorded financial indicators look healthy."

    if not transactions:
        risk_level = "Insufficient Data"
        risk_message = "Add financial transactions to analyze risk."

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(balance, 2),
        "expense_ratio": round(expense_ratio, 2),
        "savings_rate": round(savings_rate, 2),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_message": risk_message,
        "risk_factors": risk_factors,
        "recommendations": recommendations,
        "transaction_count": len(transactions)
    }
