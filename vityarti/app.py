"""
app.py
CampusBite - Next-Gen Smart Canteen Management System.
Main application factory, Blueprint orchestrator, and web route handlers.
"""

import os
from flask import Flask, render_template, session, redirect, url_for, jsonify
from database import init_db, get_db_connection
from auth import auth_bp, get_current_user
from routes_menu import menu_bp
from routes_order import order_bp
from routes_admin import admin_bp

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "campusbite_super_secret_session_key_2026")

# Register API blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)


@app.context_processor
def inject_global_vars():
    """Provides session and user info to all Jinja templates automatically."""
    user = get_current_user()
    return {
        "current_user": user,
        "active_role": session.get("user_role", "student"),
        "app_title": "CampusBite | Smart Canteen POS & Ordering"
    }


@app.route("/")
def index():
    """Main Student/Customer ordering portal with interactive menu & cart."""
    return render_template("index.html")


@app.route("/kitchen")
def kitchen_view():
    """Live Kitchen Display System (KDS) for canteen kitchen staff."""
    return render_template("kitchen.html")


@app.route("/admin")
def admin_view():
    """Management, sales metrics, and inventory dashboard for canteen admin."""
    return render_template("admin.html")


@app.route("/my-orders")
def my_orders_view():
    """Customer order tracking and digital receipt history."""
    return render_template("orders.html")


@app.errorhandler(404)
def handle_404(e):
    return render_template("index.html"), 404


@app.errorhandler(500)
def handle_500(e):
    return jsonify({"success": False, "error": "Internal server error occurred"}), 500


if __name__ == "__main__":
    # Ensure database is initialized with full schema and seed data
    init_db()
    port = int(os.environ.get("PORT", 5050))
    print(f"🚀 CampusBite Smart Canteen Management System starting on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
