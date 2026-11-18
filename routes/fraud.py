from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.fraud_detection import detect_fraud


fraud_bp = Blueprint("fraud", __name__)


@fraud_bp.route("/fraud-detection")
@login_required
def fraud_detection():

    report = detect_fraud(current_user.id)

    return render_template(
        "fraud.html",
        report=report
    )