from flask import Flask, render_template, redirect, request, url_for
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
import os # Per le estensioni dei file
import db_dao as dao

app= Flask(__name__)
app.config['SECRET_KEY'] = 'segreto_segretissimo'

# Sessioni
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# App
login_manager = LoginManager()
login_manager.init_app(app)

# Route
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/registrati')
def registrati():
    return render_template('registrati.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')

    utente_db = dao.recupera_utente_username(username)

    if not utente_db or not check_password_hash(utente_db['password'], password):
        # Credenziali non valide
        return render_template('login.html')
    else:
        utente = User(id = utente_db['id_utente'],
                    username = utente_db['username'],
                    email = utente_db['username'],
                    password = utente_db['password'],
                    tipo_utente = utente_db['tipo_utente'],
                    immagine_profilo = utente_db['immagine_profilo'])

        login_user(utente)
        # Login effettuato

    return redirect(url_for('homepage'))

@app.route('/profilo')
@login_required
def profilo():
    return render_template('profilo.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@login_manager.user_loader
def user_load(id):
    utente_db = dao.recupera_utente_id(id)

    utente = User(id = utente_db['id_utente'],
                    username = utente_db['username'],
                    email = utente_db['email'],
                    password = utente_db['password'],
                    tipo_utente = utente_db['tipo_utente'],
                    immagine_profilo = utente_db['immagine_profilo'])

    return utente

@app.route('/add_new_user', methods=['POST'])
def add_new_user():
    # Nome utente univoco
    username = request.form.get('username')
    app.logger.info(username)
    if not dao.utente_univoco(username):
        # Messaggio di errore
        app.logger.info('username già usato')
        return redirect(url_for('registrati'))
    
    # Email univoca
    email = request.form.get('email')
    app.logger.info(email)
    if not dao.email_univoca(email):
        # Messaggio di errore
        app.logger.info('email già usata')
        return redirect(url_for('registrati'))
    
    # Cripta password
    password = generate_password_hash(request.form.get('password'), method='sha256')

    # Ascoltatore o Creatore
    tipo_utente = request.form.get('tipo_utente')
    app.logger.info(tipo_utente)
    if tipo_utente == 'Ascoltare':
        tipo_utente = 0
    elif tipo_utente == 'Creare':
        tipo_utente = 1
    else:
        # Errore
        app.logger.info('utente non valido')
        return redirect(url_for('registrati'))
    
    # Immagine profilo
    immagine_profilo = request.files['immagine_profilo']
    if immagine_profilo:
        extension = os.path.splitext(immagine_profilo.filename)[-1].lower()
        nome_file = 'Immagini/Profilo/' + username + extension

        immagine_profilo.save('static/' + nome_file)
    else:
        nome_file = 'Immagini/Profilo/_default.png'
    
    immagine_profilo = nome_file

    new_user = {'username': username, 
                'email': email, 
                'password': password,
                'tipo_utente': tipo_utente,
                'immagine_profilo': immagine_profilo}

    app.logger.info(new_user)

    if not dao.aggiungi_nuovo_utente(new_user):
        # Errore
        app.logger.info('impossibile aggiungere')
        return redirect(url_for('registrati'))

    # Utente Registrato
    return redirect(url_for('homepage'))