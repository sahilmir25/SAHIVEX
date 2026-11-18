
import pandas as pd
from sklearn.linear_model import LinearRegression


def predict_future_expense(expenses):

    # Clean and validate expense data
    try:
        expenses = [
            float(value)
            for value in expenses
            if value is not None and float(value) >= 0
        ]
    except (ValueError, TypeError):
        return {
            "prediction": None,
            "average": 0,
            "last_month": 0,
            "trend": "Invalid Data",
            "prediction_status": "Unavailable",
            "difference": 0,
            "message": "Invalid expense data."
        }

    # Minimum data validation
    if len(expenses) < 2:
        return {
            "prediction": None,
            "average": round(sum(expenses) / len(expenses), 2)
                if expenses else 0,
            "last_month": round(expenses[-1], 2)
                if expenses else 0,
            "trend": "Insufficient Data",
            "prediction_status": "Unavailable",
            "difference": 0,
            "message": "At least 2 months of expense data required."
        }

    # Prepare dataset
    data = pd.DataFrame({
        "month": range(1, len(expenses) + 1),
        "expense": expenses
    })

    X = data[["month"]]
    y = data["expense"]

    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_month = pd.DataFrame({
        "month": [len(expenses) + 1]
    })

    prediction = float(model.predict(next_month)[0])
    prediction = max(0, prediction)

    # Financial calculations
    average_expense = sum(expenses) / len(expenses)
    last_month_expense = expenses[-1]
    previous_month_expense = expenses[-2]

    # Spending trend
    if last_month_expense > previous_month_expense:
        trend = "Increasing"
    elif last_month_expense < previous_month_expense:
        trend = "Decreasing"
    else:
        trend = "Stable"

    # Prediction status
    difference = prediction - last_month_expense

    if difference > 0:
        prediction_status = "Expected to Increase"
    elif difference < 0:
        prediction_status = "Expected to Decrease"
    else:
        prediction_status = "Expected to Remain Stable"

    # Prediction confidence information
    if len(expenses) < 6:
        data_quality = "Low - More monthly data recommended"
    elif len(expenses) < 12:
        data_quality = "Moderate"
    else:
        data_quality = "Better historical coverage"

    return {
        "prediction": round(prediction, 2),
        "average": round(average_expense, 2),
        "last_month": round(last_month_expense, 2),
        "trend": trend,
        "prediction_status": prediction_status,
        "difference": round(difference, 2),
        "data_quality": data_quality,
        "months_analyzed": len(expenses),
        "message": "Prediction generated using Linear Regression."
    }

