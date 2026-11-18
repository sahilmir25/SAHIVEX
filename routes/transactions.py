
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from math import isfinite

from database import db
from models.finance import Transaction

transactions_bp = Blueprint("transactions", __name__)


def validate_transaction_form():

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    transaction_type = request.form.get("transaction_type", "").strip()
    description = request.form.get("description", "").strip()

    try:
        amount = float(request.form.get("amount", ""))
    except (ValueError, TypeError):
        return None, "Please enter a valid amount."

    if not title or not category:
        return None, "Title and category are required."

    if not isfinite(amount) or amount <= 0:
        return None, "Amount must be a valid positive number."

    if transaction_type not in ("income", "expense"):
        return None, "Invalid transaction type."

    date_text = request.form.get("transaction_date", "").strip()

    try:
        date_value = (
            datetime.strptime(date_text, "%Y-%m-%d")
            if date_text
            else datetime.utcnow()
        )
    except ValueError:
        return None, "Invalid transaction date."

    return {
        "title": title,
        "amount": amount,
        "category": category,
        "transaction_type": transaction_type,
        "description": description,
        "date": date_value
    }, None


# VIEW TRANSACTIONS
@transactions_bp.route("/transactions")
@login_required
def transactions():

    user_transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Transaction.date.desc()
    ).all()

    return render_template(
        "transactions.html",
        transactions=user_transactions
    )


# ADD TRANSACTION
@transactions_bp.route("/add-transaction", methods=["POST"])
@login_required
def add_transaction():

    data, error = validate_transaction_form()

    if error:
        flash(error, "danger")
        return redirect(url_for("transactions.transactions"))

    try:
        new_transaction = Transaction(
            user_id=current_user.id,
            **data
        )

        db.session.add(new_transaction)
        db.session.commit()

        flash("Transaction added successfully!", "success")

    except Exception:
        db.session.rollback()
        flash("Unable to save transaction. Please try again.", "danger")

    return redirect(url_for("transactions.transactions"))


# EDIT TRANSACTION
@transactions_bp.route(
    "/edit-transaction/<int:transaction_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_transaction(transaction_id):

    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        data, error = validate_transaction_form()

        if error:
            flash(error, "danger")
            return redirect(
                url_for(
                    "transactions.edit_transaction",
                    transaction_id=transaction.id
                )
            )

        try:
            transaction.title = data["title"]
            transaction.amount = data["amount"]
            transaction.category = data["category"]
            transaction.transaction_type = data["transaction_type"]
            transaction.description = data["description"]
            transaction.date = data["date"]

            db.session.commit()

            flash("Transaction updated successfully!", "success")

        except Exception:
            db.session.rollback()
            flash("Unable to update transaction.", "danger")

        return redirect(url_for("transactions.transactions"))

    return render_template(
        "edit_transaction.html",
        transaction=transaction
    )


# DELETE TRANSACTION
@transactions_bp.route(
    "/delete-transaction/<int:transaction_id>",
    methods=["POST"]
)
@login_required
def delete_transaction(transaction_id):

    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=current_user.id
    ).first_or_404()

    try:
        db.session.delete(transaction)
        db.session.commit()

        flash("Transaction deleted successfully!", "success")

    except Exception:
        db.session.rollback()
        flash("Unable to delete transaction.", "danger")

    return redirect(url_for("transactions.transactions"))
