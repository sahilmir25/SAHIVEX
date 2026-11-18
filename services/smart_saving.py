
from models.finance import Transaction, FinancialGoal


def generate_saving_recommendations(user_id):

    transactions = Transaction.query.filter_by(
        user_id=user_id
    ).all()

    goals = FinancialGoal.query.filter_by(
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

    recommendations = []

    if total_income <= 0:
        recommendations.append(
            "Add income records to receive personalized saving advice."
        )

    elif balance < 0:
        recommendations.append(
            "Your expenses exceed your income. Reduce non-essential spending."
        )

    else:
        savings_rate = (balance / total_income) * 100

        if savings_rate < 10:
            recommendations.append(
                "Try saving at least 10% of your income."
            )

        elif savings_rate < 30:
            recommendations.append(
                "Your savings are improving. Aim for a 30% savings rate."
            )

        else:
            recommendations.append(
                "Excellent savings rate! Keep maintaining this habit."
            )

    if total_expense > 0:
        recommendations.append(
            f"Your recorded total expenses are Rs. {total_expense:.2f}. "
            "Review your spending regularly."
        )

    for goal in goals:

        remaining = max(
            0,
            goal.target_amount - goal.current_amount
        )

        if remaining == 0:
            recommendations.append(
                f"Congratulations! You completed your goal: {goal.title}."
            )

        elif goal.monthly_saving > 0:
            months = (
                remaining + goal.monthly_saving - 1
            ) // goal.monthly_saving

            recommendations.append(
                f"For '{goal.title}', you need Rs. {remaining:.2f} more. "
                f"At your planned saving rate, it may take approximately "
                f"{int(months)} months."
            )

        else:
            recommendations.append(
                f"Set a monthly saving amount for '{goal.title}'."
            )

    if not goals:
        recommendations.append(
            "Create a financial goal to receive goal-based recommendations."
        )

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(balance, 2),
        "recommendations": recommendations
    }
