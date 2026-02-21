from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from app import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # Check if JSON request (AJAX)
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
             username = request.form.get('username')
             password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username already exists'}), 400
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role='user')
        
        try:
            db.session.add(new_user)
            db.session.commit()
            if request.is_json:
                return jsonify({'success': True, 'message': 'Account created! Logging in...', 'redirect': url_for('auth.login')})
            flash('Account created! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            if request.is_json:
                return jsonify({'success': False, 'message': str(e)}), 500
            flash(f'Error creating account: {e}', 'error')
            
    return render_template('auth_combined.html', mode='register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
             username = request.form.get('username')
             password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            
            # Role-based redirect logic
            if user.role == 'admin':
                default_target = url_for('admin.dashboard')
            else:
                default_target = url_for('main.dashboard')
            
            next_page = request.args.get('next')
            target = next_page if next_page else default_target

            if request.is_json:
                return jsonify({'success': True, 'redirect': target})
            return redirect(target)
        else:
             if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
             flash('Invalid username or password', 'error')
            
    return render_template('auth_combined.html', mode='login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
