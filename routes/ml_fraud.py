from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.ml_fraud_detection import detect_ml_fraud


ml_fraud_bp = Blueprint("ml_fraud", __name__)


@ml_fraud_bp.route("/ml-fraud-detection")
@login_required
def ml_fraud_detection():

    report = detect_ml_fraud(current_user.id)

    return render_template(
        "ml_fraud.html",
        report=report
    )