from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from models.user import User
from database import db


auth_bp = Blueprint("auth", __name__)


# REGISTER
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == login_id) |
            (User.email == login_id.lower())
        ).first()

        if user and user.check_password(password):

            login_user(user)

            flash(
                "Welcome to SAHIVEX!",
                "success"
            )

            return redirect(url_for("home"))

        flash(
            "Invalid username/email or password.",
            "danger"
        )

    return render_template("login.html")


# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("auth.login"))