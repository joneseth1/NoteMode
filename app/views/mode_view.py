from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

mode = Blueprint('mode', __name__)

# Connect to the database
conn = sqlite3.connect('modes.db')
cursor = conn.cursor()

# Create the modes table with an auto-incremented id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS modes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mode_name TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()



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

        if 'username' in session:
            username = session['username']

            # Get user id
            user_id = get_user_id(username)

            # Insert new mode into the database with auto-incremented id
            conn = sqlite3.connect('modes.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO modes (user_id, mode_name) VALUES (?, ?)',
                           (user_id, mode_name))
            conn.commit()
            
            # Fetch the mode_id of the inserted record
            mode_id = cursor.lastrowid
            
            conn.close()

            return redirect(url_for('mode.list_modes'))

    return render_template('add_mode.html')



@mode.route('/home', methods=['GET', 'POST'])
def list_modes():
    if 'username' in session:
        username = session['username']
        print(f"Username: {username}")

        # Get user id
        user_id = get_user_id(username)
        print(f"User ID: {user_id}")

        # Retrieve modes for the user from the database
        conn = sqlite3.connect('modes.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM modes WHERE user_id = ?', (user_id,))
        modes = cursor.fetchall()
        for mode in modes:
            print(f"Mode_name: {mode[2]}")
        conn.close()

        return render_template('home.html', modes=modes)

    return redirect(url_for('login'))


# Helper function to get mode details by ID
def get_mode_by_id(mode_id):
    conn = sqlite3.connect('modes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM modes WHERE id = ?', (mode_id,))
    mode = cursor.fetchone()
    conn.close()
    return mode


# Helper function to update mode details by ID
def update_mode(mode_id, mode_name):
    conn = sqlite3.connect('modes.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE modes SET mode_name = ? WHERE id = ?',
                   (mode_name, mode_id))
    conn.commit()
    conn.close()


@mode.route('/edit-mode/<int:mode_id>', methods=['GET', 'POST'])
def edit_mode(mode_id):
    if 'username' in session:
        username = session['username']

        # Get user id
        user_id = get_user_id(username)

        # Get mode details by ID
        mode = get_mode_by_id(mode_id)
        print(mode)

        if request.method == 'POST':
            # Update mode details
            mode_name = request.form.get('mode_name')

            update_mode(mode_id, mode_name)

            return redirect(url_for('mode.list_modes'))

        return render_template('edit_mode.html', mode=mode)

    return redirect(url_for('login'))
