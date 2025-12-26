from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password are provided
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('auth.register'))

        try:
            # Hash the password
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Save the user in the database
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()

            flash('User registered successfully!', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

auth = Blueprint('auth', __name__, template_folder='templates')

# Database setup
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash("Username or email already exists!", "error")
            return redirect(url_for('auth.register'))
        finally:
            conn.close()

    return render_template('register.html')
# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Ensure the result is dictionary-like
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):  # Verify password
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash("Invalid username or password!", "error")
            return redirect(url_for('auth.login'))  # Redirect back to login page

    return render_template('login.html')


# Logout route
@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
