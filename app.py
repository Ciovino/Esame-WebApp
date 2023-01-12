from flask import Flask, render_template, redirect, request, url_for

app= Flask(__name__)

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
    
    return redirect(url_for('homepage'))

@app.route('/add_new_user', methods=['POST'])
def add_new_user():
    new_user = request.form.to_dict()

    # Nome utente univoco
    if not utente_univoco(new_user.get('username')):
        # Messaggio di errore
        return redirect(url_for('registrati'))
    
    # Email univoca
    if not email_univoca(new_user.get('email')):
        # Messaggio di errore
        return redirect(url_for('registrati'))
    
    # TODO: Cripta password

    # Ascoltatore o Creatore
    if new_user.get('tipo_utente') == 'Ascoltare':
        new_user['tipo_utente'] = 0
    elif new_user.get('tipo_utente') == 'Creare':
        new_user['tipo_utente'] = 1
    else:
        # Errore
        return redirect(url_for('registrati'))
    
    # Immagine profilo
    new_user['immagine_profilo'] = 'Prova'

    if not aggiungi_utente_database(new_user):
        # Errore
        return redirect(url_for('registrati'))

    # Successo
    return redirect(url_for('login'))

# Controlla che l'username sia univoco all'interno del database
def utente_univoco(username):
    return True

# Controlla che la email sia univoca all'interno del database
def email_univoca(email):
    return True

# Aggiunge al databse
def aggiungi_utente_database(utente):
    app.logger.info(utente)
    return True