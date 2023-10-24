from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from views.settings_view import settings
from views.mode_view import mode
from views.note_view import notes
from views.note_editer_view import note
import sqlite3

# Create a Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Register Blueprints for modular organization
app.register_blueprint(settings, url_prefix='/settings')
app.register_blueprint(mode, url_prefix='/mode')
app.register_blueprint(notes, url_prefix='/notes')
app.register_blueprint(note, url_prefix='/note')

# Create SQLite database and table for users
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password_hash TEXT
    )
''')
conn.commit()
conn.close()

# Connect to the 'modes.db' database
conn = sqlite3.connect('modes.db')
cursor = conn.cursor()

# Create the 'modes' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS modes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mode_name TEXT,
        mode_notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Hash password using passlib
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Verify password using passlib
def verify_password(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)

# Define the home route
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('mode.list_modes'))  # Redirect to the list_modes route if user is logged in
    return redirect(url_for('login'))  # Redirect to the login route if not logged in

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and verify_password(password, user[2]):
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))  # Redirect to the home route after successful login

    return render_template('login.html')

# Define the logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))  # Redirect to the login route after logout

# Define the create_account route
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    user_exists = False  # Flag to indicate whether the user already exists

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            user_exists = True
        else:
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))  # Redirect to the home route after successful account creation

        conn.close()

    return render_template('create_account.html', user_exists=user_exists)

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
