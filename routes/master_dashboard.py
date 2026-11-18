from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from database import db
from models.finance import Transaction, FinancialGoal

from services.fraud_detection import detect_fraud
from services.ml_fraud_detection import detect_ml_fraud
from services.behavior_analyzer import analyze_financial_behavior


master_bp = Blueprint("master", __name__)


@master_bp.route("/master-dashboard")
@login_required
def master_dashboard():

    user_id = current_user.id

    # Income and expense calculations
    total_income = db_value("income", user_id)
    total_expense = db_value("expense", user_id)

    balance = total_income - total_expense

    # User-specific financial goals
    goals = FinancialGoal.query.filter_by(
        user_id=user_id
    ).all()

    # User-specific intelligence reports
    fraud_report = detect_fraud(user_id)
    ml_report = detect_ml_fraud(user_id)
    behavior_report = analyze_financial_behavior(user_id)

    return render_template(
        "master_dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=round(balance, 2),
        goals=goals,
        fraud_report=fraud_report,
        ml_report=ml_report,
        behavior_report=behavior_report
    )


def db_value(transaction_type, user_id):

    result = (
        db.session.query(func.sum(Transaction.amount))
        .filter_by(
            user_id=user_id,
            transaction_type=transaction_type
        )
        .scalar()
    )

    return round(result or 0, 2)