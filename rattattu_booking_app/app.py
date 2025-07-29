
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'rattattu_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Crea la cartella di upload se non esiste
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Utente admin predefinito
ADMIN_USERNAME = "Administrator"
ADMIN_PASSWORD = "Ratt2025"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Credenziali errate", "error")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload_plant', methods=['POST'])
def upload_plant():
    if 'user' not in session:
        return redirect(url_for('login'))
    file = request.files.get('plant')
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("Piantina caricata correttamente!", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
