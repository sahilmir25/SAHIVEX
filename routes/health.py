
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.health_analyzer import analyze_financial_health
from models.finance import Transaction


health_bp = Blueprint("health", __name__)


@health_bp.route("/health-analysis")
@login_required
def health_analysis():

    transactions = Transaction.query.filter_by(
        user_id=current_user.id
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

    savings_rate = (
        (balance / total_income) * 100
        if total_income > 0 else 0
    )

    expense_ratio = (
        (total_expense / total_income) * 100
        if total_income > 0 else 0
    )

    if total_income <= 0:
        health_status = "Insufficient Income Data"
    elif balance < 0:
        health_status = "High Risk"
    elif savings_rate >= 30:
        health_status = "Healthy Savings"
    elif savings_rate >= 10:
        health_status = "Moderate Savings"
    else:
        health_status = "Low Savings"

    categories = {}

    for item in transactions:
        if item.transaction_type == "expense":
            categories[item.category] = (
                categories.get(item.category, 0) + item.amount
            )

    analysis = analyze_financial_health(current_user.id)

    return render_template(
        "health.html",
        analysis=analysis,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        savings_rate=round(savings_rate, 2),
        expense_ratio=round(expense_ratio, 2),
        health_status=health_status,
        categories=categories
    )
