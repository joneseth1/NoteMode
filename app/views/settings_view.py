from flask import Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
import sqlite3

# Create a Flask Blueprint named 'settings'
settings = Blueprint('settings', __name__)

# Define a function to delete an account based on the given username
def delete_account(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Delete the user with the given username
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()

    conn.close()

# Define a route for the settings page
@settings.route('/settings-page', methods=['GET', 'POST'])
def settings_page():
    if request.method == 'POST':
        # Get the value of the button clicked on the settings page
        button_value = request.form.get('button_name')

        # Check which button was clicked
        if button_value == 'edit':
            return render_template('create_account.html')  # Redirect to the edit account page
        elif button_value == 'delete':
            return redirect(url_for('settings.delete_account_route'))  # Redirect to the delete account page
        elif button_value == 'logout':
            return redirect(url_for('logout'))  # Redirect to the logout route

    return render_template('settings.html')

# Define a route for the delete account page
@settings.route('/delete-account', methods=['GET', 'POST'])
def delete_account_route():
    if request.method == 'POST':
        # Get the value of the button clicked on the delete account page
        button_value = request.form.get('button_name')

        # Check which button was clicked
        if button_value == 'yes':
            if 'username' in session:
                username = session['username']
                delete_account(username)  # Delete the account if 'yes' is clicked
                session.pop('username', None)  # Logout the user after deleting the account
                return redirect(url_for('login'))  # Redirect to the login page
        elif button_value == 'no':
            return redirect(url_for('settings.settings_page'))  # Redirect back to the settings page

    return render_template('delete_account.html')  # Render the delete account template
 