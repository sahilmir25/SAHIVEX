
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from services.assistant import get_financial_answer

assistant_bp = Blueprint("assistant", __name__)


@assistant_bp.route("/assistant", methods=["GET", "POST"])
@login_required
def assistant():

    answer = None
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            answer = get_financial_answer(
                question,
                current_user.id
            )

    return render_template(
        "assistant.html",
        answer=answer,
        question=question
    )
