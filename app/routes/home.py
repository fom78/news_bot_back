# app/routes/home.py
from flask import Blueprint, jsonify, redirect

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """Página de inicio de la API"""
    return jsonify({
        "name": "News Bot API",
        "version": "1.0.0",
        "documentation": "/swagger",
        "endpoints": {
            "auth": "/api/auth",
            "subscriptions": "/api/subscriptions"
        },
        "repository": "https://github.com/fom78/news_bot_back"
    })

@home_bp.route("/swagger")
def swagger_ui():
    return redirect("/api/swagger")