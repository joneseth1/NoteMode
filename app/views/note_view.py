from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from views.mode_view import get_user_id, get_mode_by_id
import sqlite3
from views.mode_view import get_user_id

# Create a Flask Blueprint named 'notes'
notes = Blueprint('notes', __name__)

# Define a route to show notes for a specific mode
@notes.route('/mode/<int:mode_id>/notes')
def show_notes(mode_id):
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

        # Get notes and mode details
        notes = get_notes_by_mode(mode_id)
        color = get_background_color(mode_id)
        font = get_font(mode_id)
        view = get_view(mode_id)
        name = get_mode_name(mode_id)

        # Render the notes template with mode information
        return render_template('notes.html', name=name, color=color, font=font, mode_id=mode_id, view=view, notes=notes)

    return redirect(url_for('login'))

# Define a route to add a new note for a specific mode
@notes.route('/mode/<int:mode_id>/add-note', methods=['GET', 'POST'])
def add_note(mode_id):
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

        mode = get_mode_by_id(mode_id)

        if request.method == 'POST':
            # Get note name from the form
            note_name = request.form.get('note_name')

            # Insert new note into the database
            with sqlite3.connect('modes.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO notes (mode_id, note_name) VALUES (?, ?)', (mode_id, note_name))
                conn.commit()

            flash('Note added successfully!', 'success')
            return redirect(url_for('notes.show_notes', mode_id=mode_id))

        return render_template('add_note.html', mode=mode)

    return redirect(url_for('login'))

# Define a route to edit a note for a specific mode
@notes.route('/mode/<int:mode_id>/edit-note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(mode_id, note_id):
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

        note = get_note_by_id(note_id)

        if request.method == 'POST':
            # Get new note name and check if the checkbox is selected for deletion
            new_note_name = request.form.get('note_name')
            delete_note = request.form.get('deleteNote')

            if delete_note is not None:  # Check if the checkbox is selected
                # Delete the note if the checkbox is selected
                with sqlite3.connect('modes.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
                    conn.commit()
                return redirect(url_for('notes.show_notes', mode_id=mode_id))

            # Update note details if the checkbox is not selected
            with sqlite3.connect('modes.db') as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE notes SET note_name = ? WHERE id = ?', (new_note_name, note_id))
                conn.commit()

            return redirect(url_for('notes.show_notes', mode_id=mode_id))

        return render_template('edit_note.html', note=note, mode_id=mode_id, note_id=note_id)

    return redirect(url_for('login'))

# Helper function to get mode information by ID
def get_mode_info(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM modes WHERE id = ?', (mode_id,))
        mode_info = cursor.fetchone()
    return mode_info

# Helper function to get background color by mode ID
def get_background_color(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT background_color FROM modes WHERE id = ?', (mode_id,))
        background_color = cursor.fetchone()
    return background_color[0] if background_color else None

# Helper function to get font by mode ID
def get_font(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT font_family FROM modes WHERE id = ?', (mode_id,))
        font = cursor.fetchone()
    return font[0] if font else None

# Helper function to get note view by mode ID
def get_view(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT note_view FROM modes WHERE id = ?', (mode_id,))
        view = cursor.fetchone()  
    return view[0] if view else None

# Helper function to get mode name by mode ID
def get_mode_name(mode_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT mode_name FROM modes WHERE id = ?', (mode_id,))
        mode_name = cursor.fetchone()
    return mode_name[0]

# Helper function to get notes by mode ID
def get_notes_by_mode(mode_id):
    conn = sqlite3.connect('modes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE mode_id = ?', (mode_id,))
    notes = cursor.fetchall()
    conn.close()
    print(notes)
    return notes

# Helper function to get note by ID
def get_note_by_id(note_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        note = cursor.fetchone()
    return note
