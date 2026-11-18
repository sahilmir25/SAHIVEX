import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    SEO_BASE_URL = "https://sahivex.onrender.com"

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is missing. Set it in Environment Variables.")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///sahivex.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    )

    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE