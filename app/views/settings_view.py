from flask import Blueprint, render_template, request, redirect, url_for

settings = Blueprint('settings', __name__)

@settings.route('/settings-page', methods=['GET','POST'])
def settings_page():

    if request.method == 'POST':
        button_value = request.form.get('button_name') 
            
        if button_value == 'edit':
            return render_template('create_acount.html')
        elif button_value == 'delete':
            return render_template('login.html')
        elif button_value == 'logout':
            return redirect(url_for('logout'))

    return render_template('settings.html')

