from flask import Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
import sqlite3

mode = Blueprint('mode', __name__)


def get_user_id(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id

@mode.route('/add-mode', methods=['GET', 'POST'])
def add_mode():
    if request.method == 'POST':
        mode_name = request.form.get('mode_name')
        mode_notes = request.form.get('mode_notes')

        if 'username' in session:
            username = session['username']

            # Get user id
            user_id = get_user_id(username)

            # Insert new mode into the database
            conn = sqlite3.connect('modes.db')  # Assuming you have a separate database for modes
            cursor = conn.cursor()
            cursor.execute('INSERT INTO modes (user_id, mode_name, mode_notes) VALUES (?, ?, ?)',
                           (user_id, mode_name, mode_notes))
            conn.commit()
            conn.close()

            return redirect(url_for('mode.list_modes'))

    return render_template('add_mode.html')
