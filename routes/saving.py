from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.smart_saving import generate_saving_recommendations

saving_bp = Blueprint("saving", __name__)


@saving_bp.route("/smart-saving")
@login_required
def smart_saving():

    report = generate_saving_recommendations(current_user.id)

    return render_template(
        "smart_saving.html",
        report=report
    )
