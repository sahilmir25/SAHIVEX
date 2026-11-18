from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.subscription_detector import detect_subscriptions


subscriptions_bp = Blueprint("subscriptions", __name__)


@subscriptions_bp.route("/subscriptions")
@login_required
def subscriptions():

    report = detect_subscriptions(current_user.id)

    return render_template(
        "subscriptions.html",
        report=report
    )