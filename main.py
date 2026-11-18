
import os
from datetime import date

from flask import Flask, render_template, Response, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf

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


# ==========================================
# SAHIVEX APPLICATION
# ==========================================

app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)


# ==========================================
# CSRF PROTECTION
# ==========================================

csrf = CSRFProtect()
csrf.init_app(app)


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

db.init_app(app)


# ==========================================
# LOGIN MANAGER
# ==========================================

login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ==========================================
# REGISTER BLUEPRINTS
# ==========================================

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


# ==========================================
# SEO CONFIGURATION
# ==========================================

def get_base_url():
    return (
        app.config.get("SEO_BASE_URL")
        or request.url_root.rstrip("/")
    )


# ==========================================
# GOOGLE SEARCH CONSOLE VERIFICATION
# ==========================================

@app.route("/google46c142889389b237.html")
def google_site_verification():

    return Response(
        "google-site-verification: google46c142889389b237.html",
        mimetype="text/html"
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# SITEMAP.XML
# ==========================================

@app.route("/sitemap.xml")
def sitemap():

    base_url = get_base_url()

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>{base_url}/</loc>
        <lastmod>{date.today().isoformat()}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>

</urlset>
"""

    return Response(
        xml_content,
        mimetype="application/xml"
    )


# ==========================================
# ROBOTS.TXT
# ==========================================

@app.route("/robots.txt")
def robots():

    base_url = get_base_url()

    robots_content = f"""User-agent: *
Allow: /

Disallow: /dashboard
Disallow: /transactions
Disallow: /assistant

Sitemap: {base_url}/sitemap.xml
"""

    return Response(
        robots_content,
        mimetype="text/plain"
    )


# ==========================================
# DATABASE TABLE CREATION
# ==========================================

with app.app_context():
    db.create_all()


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
