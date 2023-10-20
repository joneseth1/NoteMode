from flask import Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
import sqlite3

settings = Blueprint('settings', __name__)


def delete_account(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Delete the user with the given username
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()

    conn.close()




@settings.route('/settings-page', methods=['GET', 'POST'])
def settings_page():
    if request.method == 'POST':
        button_value = request.form.get('button_name')

        if button_value == 'edit':
            return render_template('create_account.html')
        elif button_value == 'delete':
            return redirect(url_for('settings.delete_account_route'))
        elif button_value == 'logout':
            return redirect(url_for('logout'))

    return render_template('settings.html')


@settings.route('/delete-account', methods=['GET', 'POST'])
def delete_account_route():
    if request.method == 'POST':
        button_value = request.form.get('button_name')

        if button_value == 'yes':
            if 'username' in session:
                username = session['username']
                delete_account(username)
                session.pop('username', None)  # Logout the user after deleting the account
                return redirect(url_for('login'))
        elif button_value == 'no':
            return redirect(url_for('settings.settings_page'))

    return render_template('delete_account.html')    