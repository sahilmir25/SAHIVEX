
from database import db
from datetime import datetime


class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # User ownership
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )

    title = db.Column(db.String(150), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    category = db.Column(db.String(100), nullable=False)

    transaction_type = db.Column(db.String(20), nullable=False)

    date = db.Column(db.DateTime, default=datetime.utcnow)

    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Transaction {self.title}>"


class FinancialGoal(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # User ownership
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )

    title = db.Column(db.String(150), nullable=False)

    target_amount = db.Column(db.Float, nullable=False)

    current_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    monthly_saving = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    deadline = db.Column(db.Date, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<FinancialGoal {self.title}>"

    @property
    def progress(self):

        if self.target_amount <= 0:
            return 0

        percentage = (
            self.current_amount / self.target_amount
        ) * 100

        return round(min(100, max(0, percentage)), 2)

    @property
    def remaining_amount(self):

        return round(
            max(0, self.target_amount - self.current_amount),
            2
        )
