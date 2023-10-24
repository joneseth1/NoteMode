from flask import Blueprint, render_template
from views.note_view import get_mode_info, get_mode_by_id, get_background_color, get_note_by_id

note = Blueprint('note', __name__)


#View for the actual note editing, not fully complete since this is a sprint 3 requirment

@note.route('/mode/<int:mode_id>/notes/<int:note_id>')
def show_note(mode_id, note_id):
    
    color = get_background_color(mode_id)
    name = get_note_by_id(note_id)[2]


    return render_template('note.html', color=color, name=name)

