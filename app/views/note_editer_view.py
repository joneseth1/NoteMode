import sqlite3
from flask import Blueprint, render_template
from views.note_view import get_mode_info, get_mode_by_id, get_background_color, get_note_by_id, request

note = Blueprint('note', __name__)


#View for the actual note editing, not fully complete since this is a sprint 3 requirment

@note.route('/mode/<int:mode_id>/notes/<int:note_id>')
def show_note(mode_id, note_id):
    
    color = get_background_color(mode_id)
    name = get_note_by_id(note_id)
    password = get_note_password(note_id)

    if password is not None: 
        return render_template('password_prompt.html', mode_id=mode_id, note_id=note_id)

    return render_template('note.html', color=color, name=name)

@note.route('/mode/<int:mode_id>/notes/<int:note_id>', methods=['GET', 'POST'])
def password_note(mode_id, note_id):
    color = get_background_color(mode_id)
    name = get_note_by_id(note_id)
    password = get_note_password(note_id)

    if request.method == 'POST':
        entered_password = request.form.get('note_password')

        if entered_password == password:
            # Password is correct, continue to show the note content
            return render_template('note.html', color=color, name=name)
        else:
            # Incorrect password, show an error message
            error_message = 'Incorrect password. Please try again.'
            return render_template('password_prompt.html', mode_id=mode_id, note_id=note_id, error_message=error_message)


    return render_template('password_prompt.html', mode_id=mode_id, note_id=note_id)



@note.route('/mode/<int:mode_id>/notes/<int:note_id>')
def word_count(s):  
    if request.method == 'POST':
        note_content = request.form.get('noteTextarea')
        word_count = count_words(note_content)
        return render_template('note.html', word_count=word_count)
    else: 
        return render_template('note.html')
    

def count_words(text):
    words = text.split()
    return len(words)

def get_note_password(note_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT note_password FROM notes WHERE id = ?', (note_id,))
        note_password = cursor.fetchone()
    return note_password[0] if note_password else None



