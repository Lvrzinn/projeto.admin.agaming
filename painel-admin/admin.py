from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from models import User
from werkzeug.urls import url_parse

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Nome de usuário ou senha inválidos')
            return redirect(url_for('admin_bp.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin_bp.dashboard')
        return redirect(next_page)
    return render_template('login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@admin_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin_bp.login'))
