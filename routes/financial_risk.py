from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.financial_risk import analyze_financial_risk


financial_risk_bp = Blueprint("financial_risk", __name__)


@financial_risk_bp.route("/financial-risk")
@login_required
def financial_risk():

    report = analyze_financial_risk(current_user.id)

    return render_template(
        "financial_risk.html",
        report=report
    )
