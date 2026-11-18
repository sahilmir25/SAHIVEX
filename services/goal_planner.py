
from datetime import date


def calculate_goal_plan(
    target_amount,
    current_amount=0,
    monthly_saving=0
):

    # Validate inputs
    if target_amount <= 0:
        return {
            "success": False,
            "message": "Target amount must be greater than zero."
        }

    if current_amount < 0 or monthly_saving < 0:
        return {
            "success": False,
            "message": "Amounts cannot be negative."
        }

    if current_amount >= target_amount:
        return {
            "success": True,
            "completed": True,
            "target_amount": target_amount,
            "current_amount": current_amount,
            "remaining_amount": 0,
            "progress": 100,
            "months_required": 0,
            "message": "Congratulations! Your goal is completed."
        }

    remaining = target_amount - current_amount

    if monthly_saving <= 0:
        months_required = None
        estimated_date = None
        message = "Enter a monthly saving amount to calculate your plan."

    else:
        months_required = (
            remaining + monthly_saving - 1
        ) // monthly_saving

        estimated_date = None
        message = "Your estimated savings plan is ready."

    progress = (
        current_amount / target_amount
    ) * 100

    return {
        "success": True,
        "completed": False,
        "target_amount": round(target_amount, 2),
        "current_amount": round(current_amount, 2),
        "remaining_amount": round(remaining, 2),
        "progress": round(progress, 2),
        "monthly_saving": round(monthly_saving, 2),
        "months_required": months_required,
        "estimated_date": estimated_date,
        "message": message
    }
