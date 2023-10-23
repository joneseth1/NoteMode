# notes.py
from flask import Blueprint, render_template, redirect, url_for, session, flash
import sqlite3
from views.mode_view import get_user_id

notes = Blueprint('notes', __name__)

@notes.route('/mode/<int:mode_id>/notes')
def show_notes(mode_id):
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

        notes = get_notes_by_mode(mode_id)
        return render_template('notes.html', notes=notes, mode_id=mode_id)

    return redirect(url_for('login'))

# Helper function to get notes by mode ID
def get_notes_by_mode(mode_id):
    conn = sqlite3.connect('modes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE mode_id = ?', (mode_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes
