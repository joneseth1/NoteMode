# Import necessary modules
from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

# Create a Flask Blueprint named 'mode'
mode = Blueprint('mode', __name__)

# Define a function to initialize the modes database
def init_db():
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()

        # Create the 'modes' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                mode_name TEXT,
                background_color TEXT,
                font_family TEXT,
                note_view TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Create the 'notes' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode_id INTEGER,
                note_name TEXT,
                note_content TEXT, 
                FOREIGN KEY (mode_id) REFERENCES modes (id)
            )
        ''')

        conn.commit()

# Initialize the database when the application starts
init_db()

# Define a function to get the user ID based on the username
def get_user_id(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id

# Define a route for adding a new mode
@mode.route('/add-mode', methods=['GET', 'POST'])
def add_mode():
    if request.method == 'POST':
        # Get mode details from the form
        mode_name = request.form.get('mode_name')
        background_color = request.form.get('background_color')
        font_family = request.form.get('font_family')
        note_view = 'note-tile'

        if 'username' in session:
            username = session['username']

            # Get user id
            user_id = get_user_id(username)

            # Insert new mode into the database with auto-incremented id
            with sqlite3.connect('modes.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO modes (user_id, mode_name, background_color, font_family, note_view) VALUES (?, ?, ?, ?, ?)',
                               (user_id, mode_name, background_color, font_family, note_view))
                mode_id = cursor.lastrowid

            return redirect(url_for('mode.list_modes'))

    return render_template('add_mode.html')

# Define a route for listing modes on the home page
@mode.route('/home', methods=['GET', 'POST'])
def list_modes():
    if 'username' in session:
        username = session['username']
        print(f"Username: {username}")

        # Get user id
        user_id = get_user_id(username)
        print(f"User ID: {user_id}")

        # Retrieve modes for the user from the database
        with sqlite3.connect('modes.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM modes WHERE user_id = ?', (user_id,))
            modes = cursor.fetchall()
            for mode in modes:
                print(f"Mode_name: {mode[2]}, Background Color: {mode[3]}, Font Family: {mode[4]}")

        return render_template('home.html', modes=modes)

    return redirect(url_for('login'))

# Helper function to get mode details by ID
def get_mode_by_id(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM modes WHERE id = ?', (mode_id,))
        mode = cursor.fetchone()
    return mode

# Helper function to update mode details by ID
def update_mode(mode_id, mode_name, background_color, font_family, note_view):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE modes SET mode_name = ?, background_color = ?, font_family = ?, note_view = ? WHERE id = ?',
                       (mode_name, background_color, font_family, note_view, mode_id))
        conn.commit()

# Define a route for editing a mode
@mode.route('/edit-mode/<int:mode_id>', methods=['GET', 'POST'])
def edit_mode(mode_id):
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

        # Get mode details by ID
        mode = get_mode_by_id(mode_id)

        if request.method == 'POST':
            # Update mode details
            mode_name = request.form.get('mode_name')
            background_color = request.form.get('background_color')
            font_family = request.form.get('font_family')
            note_view = request.form.get('note_view')
            delete_mode = request.form.get('deleteMode')  # Check if the checkbox is selected

            if delete_mode is not None:  # Check if the checkbox is selected
                # Delete the mode if the checkbox is selected
                with sqlite3.connect('modes.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM modes WHERE id = ? AND user_id = ?', (mode_id, user_id))
                return redirect(url_for('mode.list_modes'))
            else:
                # Update mode details if the checkbox is not selected
                update_mode(mode_id, mode_name, background_color, font_family, note_view)
                return redirect(url_for('mode.list_modes'))

        return render_template('edit_mode.html', mode=mode)

    return redirect(url_for('login'))

