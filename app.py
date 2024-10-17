from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Use a strong secret key in production

# Database connection settings (modify with your actual Supabase credentials)
DB_HOST = 'your_supabase_db_host'
DB_NAME = 'your_supabase_db_name'
DB_USER = 'your_supabase_db_user'
DB_PASSWORD = 'your_supabase_db_password'

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/')
def index():
    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            conn.commit()
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('Email is already registered!', 'danger')
        finally:
            cur.close()
            conn.close()

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the database for the user
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            # If password matches, log in the user
            session['user_id'] = user[0]
            session['email'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

# Dashboard route (protected)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access this page', 'danger')
        return redirect(url_for('login'))

    return render_template('dashboard.html', email=session['email'])

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
