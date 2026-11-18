from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.expense_intelligence import analyze_expenses


expense_intelligence_bp = Blueprint(
    "expense_intelligence",
    __name__
)


@expense_intelligence_bp.route("/expense-intelligence")
@login_required
def expense_intelligence():

    report = analyze_expenses(current_user.id)

    return render_template(
        "expense_intelligence.html",
        report=report
    )