
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.finance import Transaction
from services.prediction import predict_future_expense

import plotly.graph_objects as go
import pandas as pd


prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/prediction")
@login_required
def prediction():

    # Fetch only logged-in user's expenses
    transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type="expense"
    ).order_by(
        Transaction.date.asc()
    ).all()

    # Group expenses by month
    monthly_expenses = {}

    for item in transactions:

        month = item.date.strftime("%Y-%m")

        monthly_expenses[month] = (
            monthly_expenses.get(month, 0) + item.amount
        )

    months = sorted(monthly_expenses.keys())

    expenses = [
        round(monthly_expenses[month], 2)
        for month in months
    ]

    # Machine Learning Prediction
    result = predict_future_expense(expenses)

    # Create Interactive Chart
    chart = go.Figure()

    if months:
        chart.add_trace(
            go.Scatter(
                x=months,
                y=expenses,
                mode="lines+markers",
                name="Actual Expenses",
                line=dict(width=3)
            )
        )

    # Future Prediction
    if result["prediction"] is not None and months:

        next_month = (
            pd.Period(months[-1], freq="M") + 1
        ).strftime("%Y-%m")

        chart.add_trace(
            go.Scatter(
                x=[months[-1], next_month],
                y=[
                    expenses[-1],
                    result["prediction"]
                ],
                mode="lines+markers",
                name="Predicted Expense",
                line=dict(dash="dash", width=3)
            )
        )

    chart.update_layout(
        title="Monthly Expense Prediction",
        xaxis_title="Month",
        yaxis_title="Expense (INR)",
        template="plotly_dark",
        paper_bgcolor="#151d35",
        plot_bgcolor="#151d35",
        font_color="white",
        hovermode="x unified"
    )

    prediction_chart = chart.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    return render_template(
        "prediction.html",
        result=result,
        months_count=len(expenses),
        months=months,
        expenses=expenses,
        prediction_chart=prediction_chart
    )
