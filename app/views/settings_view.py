from flask import Blueprint, render_template

settings = Blueprint('settings', __name__)

@settings.route('/settings-page')
def settings_page():
    return render_template('settings.html')