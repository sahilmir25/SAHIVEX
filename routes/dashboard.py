
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.analytics import get_financial_summary
from services.budget import get_budget_recommendations

import plotly.express as px
import pandas as pd


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    user_id = current_user.id

    # User-specific Financial Analytics
    summary = get_financial_summary(user_id)

    total_income = summary["total_income"]
    total_expense = summary["total_expense"]
    balance = summary["balance"]

    health_score = summary["health_score"]
    health_status = summary["health_status"]

    categories = summary["categories"]

    highest_category = summary["highest_category"]
    highest_amount = summary["highest_amount"]

    months = summary["months"]
    monthly_income = summary["monthly_income"]
    monthly_expense = summary["monthly_expense"]
    monthly_savings = summary["monthly_savings"]

    # User-specific Budget Recommendations
    budget_recommendations = get_budget_recommendations(user_id)

    # 1. Income vs Expense Chart
    bar_data = pd.DataFrame({
        "Type": ["Income", "Expense"],
        "Amount": [total_income, total_expense]
    })

    bar_fig = px.bar(
        bar_data,
        x="Type",
        y="Amount",
        color="Type",
        title="Income vs Expense",
        text_auto=".2s"
    )

    bar_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d35",
        plot_bgcolor="#151d35",
        font_color="white"
    )

    # 2. Expense Category Donut Chart
    if categories:
        pie_fig = px.pie(
            names=list(categories.keys()),
            values=list(categories.values()),
            title="Expense by Category",
            hole=0.55
        )
    else:
        pie_fig = px.pie(
            names=["No Expenses"],
            values=[1],
            title="Expense by Category",
            hole=0.55
        )

    pie_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d35",
        font_color="white"
    )

    # 3. Monthly Income vs Expense Chart
    monthly_data = pd.DataFrame({
        "Month": months,
        "Income": monthly_income,
        "Expense": monthly_expense
    })

    if not monthly_data.empty:
        monthly_fig = px.bar(
            monthly_data,
            x="Month",
            y=["Income", "Expense"],
            barmode="group",
            title="Monthly Income vs Expense"
        )
    else:
        monthly_fig = px.bar(
            title="Monthly Income vs Expense"
        )

    monthly_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d35",
        plot_bgcolor="#151d35",
        font_color="white"
    )

    # 4. Monthly Savings Trend
    savings_data = pd.DataFrame({
        "Month": months,
        "Savings": monthly_savings
    })

    savings_fig = px.line(
        savings_data,
        x="Month",
        y="Savings",
        title="Monthly Savings Trend",
        markers=True
    )

    savings_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d35",
        plot_bgcolor="#151d35",
        font_color="white"
    )

    # Convert Charts to HTML
    bar_chart = bar_fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    pie_chart = pie_fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    monthly_chart = monthly_fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    savings_chart = savings_fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    return render_template(
        "dashboard.html",
        income=total_income,
        expense=total_expense,
        balance=balance,
        health_score=health_score,
        health_status=health_status,
        highest_category=highest_category,
        highest_amount=highest_amount,
        bar_chart=bar_chart,
        pie_chart=pie_chart,
        monthly_chart=monthly_chart,
        savings_chart=savings_chart,
        budget_recommendations=budget_recommendations
    )


