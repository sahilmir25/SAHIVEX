from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.recurring_expenses import detect_recurring_expenses


recurring_bp = Blueprint("recurring", __name__)


@recurring_bp.route("/recurring-expenses")
@login_required
def recurring_expenses():

    report = detect_recurring_expenses(current_user.id)

    return render_template(
        "recurring.html",
        report=report
    )