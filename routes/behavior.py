from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.behavior_analyzer import analyze_financial_behavior


behavior_bp = Blueprint("behavior", __name__)


@behavior_bp.route("/financial-behavior")
@login_required
def financial_behavior():

    report = analyze_financial_behavior(current_user.id)

    return render_template(
        "behavior.html",
        report=report
    )