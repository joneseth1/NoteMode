import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, render_template
from views.note_view import get_mode_info, get_mode_by_id, get_background_color, get_note_by_id, request

note = Blueprint('note', __name__)


# this route shows the note and updates the styling according to its mode, it also request a password to be entered,
# if a password is associted to the note 
@note.route('/mode/<int:mode_id>/notes/<int:note_id>')
def show_note(mode_id, note_id):
    
    color = get_background_color(mode_id)
    name = get_note_by_id(note_id)
    password = get_note_password(note_id)

    if password is not None: 
        return render_template('password_prompt.html', mode_id=mode_id, note_id=note_id) # if password is needed then prompt the user 

    return render_template('note.html', color=color, name=name)

# route for the notfication to be sent
@note.route('/mode/<int:mode_id>/notes/<int:note_id>/notifications', methods=['GET', 'POST'])
def notifications(mode_id, note_id):
    color = get_background_color(mode_id)
    name = get_note_by_id(note_id)
    password = get_note_password(note_id)

    
    if request.method == 'POST':
        email = request.form['email']
        selected_date = request.form['selected_date']

        # Gmail credentials
        gmail_user = 'notemode4@gmail.com'
        gmail_password = 'ggtunleyylvgkkvo'

        # Set up the email content
        subject = f'NoteMode Reminder for {selected_date} your note called: {name[2]}'
        body = f'Hello,\n\nThis is a reminder for the selected date: "{selected_date}: in your note: "{name[2]}".\n\nBest regards,\n NoteMode'

        message = MIMEMultipart()
        message['From'] = gmail_user
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, email, message.as_string())

            return render_template('note.html', color=color, name=name)

    return render_template('notifications.html', mode_id=mode_id, note_id=note_id)


# route for a password to be written to get in a note 
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


# the route that counts the words in a note
@note.route('/mode/<int:mode_id>/notes/<int:note_id>')
def word_count(s):  
    if request.method == 'POST':
        note_content = request.form.get('noteTextarea')
        word_count = count_words(note_content)
        return render_template('note.html', word_count=word_count)
    else: 
        return render_template('note.html')
    
# helper function fo counter the words in a note 
def count_words(text):
    words = text.split()
    return len(words)

# helper function for note password 
def get_note_password(note_id):
    with sqlite3.connect('modes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT note_password FROM notes WHERE id = ?', (note_id,))
        note_password = cursor.fetchone()
    return note_password[0] if note_password else None



