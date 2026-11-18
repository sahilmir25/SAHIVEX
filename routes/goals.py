
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from database import db
from models.finance import FinancialGoal
from services.goal_planner import calculate_goal_plan


goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():

    if request.method == "POST":

        try:
            title = request.form.get("title", "").strip()

            target_amount = float(
                request.form.get("target_amount", 0)
            )

            current_amount = float(
                request.form.get("current_amount", 0)
            )

            monthly_saving = float(
                request.form.get("monthly_saving", 0)
            )

            deadline_input = request.form.get("deadline")

            if not title:
                raise ValueError("Goal title is required.")

            if target_amount <= 0:
                raise ValueError("Target must be greater than zero.")

            if current_amount < 0 or monthly_saving < 0:
                raise ValueError("Amounts cannot be negative.")

            if current_amount > target_amount:
                raise ValueError(
                    "Current savings cannot exceed the target."
                )

            deadline = (
                datetime.strptime(
                    deadline_input, "%Y-%m-%d"
                ).date()
                if deadline_input else None
            )

            goal = FinancialGoal(
                user_id=current_user.id,
                title=title,
                target_amount=target_amount,
                current_amount=current_amount,
                monthly_saving=monthly_saving,
                deadline=deadline
            )

            db.session.add(goal)
            db.session.commit()

            flash("Financial goal created successfully!", "success")

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "error")

        except Exception as error:
            db.session.rollback()
            print("Goal Creation Error:", error)
            flash("Could not create goal. Please try again.", "error")

        return redirect(url_for("goals.goals"))

    all_goals = FinancialGoal.query.filter_by(
        user_id=current_user.id
    ).order_by(
        FinancialGoal.created_at.desc()
    ).all()

    goal_plans = {}

    for goal in all_goals:
        goal_plans[goal.id] = calculate_goal_plan(
            target_amount=goal.target_amount,
            current_amount=goal.current_amount,
            monthly_saving=goal.monthly_saving
        )

    return render_template(
        "goals.html",
        goals=all_goals,
        goal_plans=goal_plans
    )


@goals_bp.route("/goals/update/<int:goal_id>", methods=["POST"])
@login_required
def update_goal(goal_id):

    goal = FinancialGoal.query.filter_by(
        id=goal_id,
        user_id=current_user.id
    ).first()

    if not goal:
        flash("Goal not found.", "error")
        return redirect(url_for("goals.goals"))

    try:
        current_amount = float(
            request.form.get("current_amount", 0)
        )

        if current_amount < 0:
            raise ValueError("Savings cannot be negative.")

        if current_amount > goal.target_amount:
            raise ValueError("Savings cannot exceed target.")

        goal.current_amount = current_amount

        db.session.commit()

        flash("Goal progress updated!", "success")

    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")

    except Exception as error:
        db.session.rollback()
        print("Goal Update Error:", error)
        flash("Could not update goal.", "error")

    return redirect(url_for("goals.goals"))
