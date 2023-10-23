from flask import Blueprint, render_template
from views.note_view import get_mode_info, get_mode_by_id, get_background_color, get_note_by_id

note = Blueprint('note', __name__)

@note.route('/mode/<int:mode_id>/notes/<int:note_id>')
def show_note(mode_id, note_id):
    
    color = get_background_color(mode_id)
    name = get_note_by_id(note_id)[2]


    return render_template('note.html', color=color, name=name)

# Other routes or functions related to the note blueprint if needed
