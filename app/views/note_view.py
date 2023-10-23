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

        info = get_mode_info(mode_id)
        color = get_background_color(mode_id)
        font = get_font(mode_id)
        return render_template('notes.html', color=color, font=font, mode_id=mode_id)

    return redirect(url_for('login'))


def get_mode_info(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM modes WHERE id = ?', (mode_id,))
        mode_info = cursor.fetchone()
    return mode_info

def get_background_color(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT background_color FROM modes WHERE id = ?', (mode_id,))
        background_color = cursor.fetchone()
    return background_color[0] if background_color else None

def get_font(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT font_family FROM modes WHERE id = ?', (mode_id,))
        font = cursor.fetchone()
    return font[0] if font else None


# Helper function to get notes by mode ID
def get_notes_by_mode(mode_id):
    conn = sqlite3.connect('modes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE mode_id = ?', (mode_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes
