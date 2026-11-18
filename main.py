import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from config import Config
from database import db

from models.finance import Transaction, FinancialGoal
from models.user import User

from routes.transactions import transactions_bp
from routes.dashboard import dashboard_bp
from routes.prediction import prediction_bp
from routes.assistant import assistant_bp
from routes.health import health_bp
from routes.goals import goals_bp
from routes.saving import saving_bp
from routes.expense_intelligence import expense_intelligence_bp
from routes.recurring import recurring_bp
from routes.subscriptions import subscriptions_bp
from routes.financial_risk import financial_risk_bp
from routes.fraud import fraud_bp
from routes.ml_fraud import ml_fraud_bp
from routes.behavior import behavior_bp
from routes.master_dashboard import master_bp
from routes.auth import auth_bp


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize CSRF Protection
csrf = CSRFProtect()
csrf.init_app(app)

# Initialize Database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Register Blueprints
app.register_blueprint(transactions_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(assistant_bp)
app.register_blueprint(health_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(saving_bp)
app.register_blueprint(expense_intelligence_bp)
app.register_blueprint(recurring_bp)
app.register_blueprint(subscriptions_bp)
app.register_blueprint(financial_risk_bp)
app.register_blueprint(fraud_bp)
app.register_blueprint(ml_fraud_bp)
app.register_blueprint(behavior_bp)
app.register_blueprint(master_bp)
app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return render_template("index.html")


# Create database tables
with app.app_context():
    db.create_all()


# Run Application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )