from flask import Flask, render_template, redirect, request, url_for
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import locale
import os # Per le estensioni dei file
import db_dao as dao

# locale.setlocale(locale.LC_ALL, 'it_CH')

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
    tutti_podcast = dao.tutti_podcast()

    return render_template('homepage.html', tutti_podcast=tutti_podcast)

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

@app.route('/categorie')
def categorie():
    return render_template('categorie.html')

@app.route('/seguiti')
@login_required
def seguiti():
    return render_template('seguiti.html')

@app.route('/tuoi_podcast')
@login_required
def tuoi_podcast():
    tutti_podcast = dao.recupera_podcast_utente(current_user.get_id())
    num_podcast = len(tutti_podcast)

    return render_template('tuoi_podcast.html', num_podcast=num_podcast, tutti_podcast=tutti_podcast)

@app.route('/nuovo-podcast', methods=['POST'])
@login_required
def nuovo_podcast():
    # Id_utente
    id_utente = request.form.get('id_utente')

    app.logger.info(str(id_utente) + ' ' + str(current_user.get_id()))
    if int(id_utente) != int(current_user.get_id()):
        # Errore (strano)
        return redirect(url_for('tuoi_podcast'))

    app.logger.info('utente')

    # Titolo
    titolo = request.form.get('titolo')
    if not dao.titolo_podcast_valido(titolo, id_utente):
        # Errore
        return redirect(url_for('tuoi_podcast'))

    app.logger.info('titolo')

    # Descrizione
    descrizione = request.form.get('descrizione')
    app.logger.info('descrizione')

    # Categoria
    categoria = request.form.get('categoria')
    app.logger.info('categoria')

    # Immagine
    immagine = request.files['immagine']
    if immagine:
        extension = os.path.splitext(immagine.filename)[-1].lower()

        # static/Immagini/Podcast/<titolo>_<id_utente>.<estensione>
        nome_file = 'Immagini/Podcast/' + titolo + '_' + id_utente + extension

        immagine.save('static/' + nome_file)
    else:
        # Errore
        return redirect(url_for('tuoi_podcast'))
    
    immagine = nome_file
    app.logger.info('immagine')

    # Data di creazione
    data_creazione = datetime.now().strftime('%Y-%m-%d')
    app.logger.info('data_creazione')

    podcast = {'id_utente': id_utente,
                'titolo' : titolo,
                'descrizione' : descrizione,
                'categoria' : categoria,
                'immagine' : immagine,
                'data_creazione' : data_creazione}

    app.logger.info(podcast)

    if not dao.aggiungi_podcast(podcast):
        # Errore
        app.logger.info('impossibile aggiungere')

    return redirect(url_for('tuoi_podcast'))

@app.route('/modifica_podcast', methods=['POST'])
@login_required
def modifica_podcast():
    id_podcast = request.form.get('id_podcast')
    nuovo_titolo = request.form.get('titolo')
    nuova_descrizione = request.form.get('descrizione')

    if not dao.modifica_podcast(id_podcast, nuovo_titolo, nuova_descrizione):
        # Errore
        app.logger.info('impossibile modificare')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/elimina_podcast', methods=['POST'])
@login_required
def elimina_podcast():
    id_podcast = request.form.get('id_podcast')

    if not dao.elimina_podcast(id_podcast):
        # Errore
        app.logger.info('impossibile eliminare')

    return redirect(url_for('tuoi_podcast'))

@app.route('/podcast/<int:id_podcast>')
def podcast(id_podcast):
    podcast_completo = dao.recupera_podcast(id_podcast)
    episodi_pubblici = dao.recupera_episodi_podcast(id_podcast)
    episodi_privati = []    
    
    for episodio in episodi_pubblici:
        giorni = (datetime.now() - datetime.strptime(episodio['data'], '%Y-%m-%d')).days

        episodio['data'] = datetime.strptime(episodio['data'], '%Y-%m-%d').strftime('%d %b %Y')

        if giorni < 0:
            episodi_pubblici.remove(episodio)
            episodi_privati.append(episodio)
    
    num_episodi_privati = len(episodi_privati)
    num_episodi_pubblici = len(episodi_pubblici)

    if current_user.is_authenticated:
        seguito = dao.podcast_seguito(id_podcast, current_user.get_id())
    else:
        seguito = -1

    return render_template('podcast.html', 
                            podcast=podcast_completo,
                            num_episodi_pubblici=num_episodi_pubblici, 
                            episodi_pubblici=episodi_pubblici, 
                            num_episodi_privati=num_episodi_privati, 
                            episodi_privati=episodi_privati, 
                            data_oggi=datetime.now().strftime('%Y-%m-%d'),
                            seguito=seguito)

@app.route('/podcast/<int:id_podcast>/<int:id_episodio>')
@login_required
def episodio(id_podcast, id_episodio):
    podcast = dao.recupera_podcast(id_podcast)

    episodio = dao.recupera_episodio(id_episodio)
    episodio_precedente = dao.episodio_precedente(id_podcast, id_episodio, episodio['data'])
    episodio_successivo = dao.episodio_successivo(id_podcast, id_episodio, episodio['data'], datetime.now().strftime('%Y-%m-%d'))

    commenti = dao.commenti_episodio(id_episodio)

    for commento in commenti:
        commento['data'] = datetime.strptime(episodio['data'], '%Y-%m-%d').strftime('%d %b %Y')

    return render_template('episodio.html',
                            podcast = podcast,
                            episodio = episodio,
                            episodio_precedente=episodio_precedente,
                            episodio_successivo=episodio_successivo,
                            num_commenti = len(commenti),
                            commenti = commenti)

@app.route('/nuovo-commento', methods=['POST'])
@login_required
def nuovo_commento():
    # Id podcast
    id_podcast = request.form.get('id_podcast')

    # Id_utente
    id_utente = request.form.get('id_utente')

    # Id episodio
    id_episodio = request.form.get('id_episodio')

    # Contenuto 
    contenuto = request.form.get('contenuto')

    # Data
    data = datetime.now().strftime('%Y-%m-%d')

    commento = { 'id_utente' : id_utente,
                'id_episodio' : id_episodio,
                'contenuto': contenuto,
                'data' : data}

    if not dao.aggiungi_commento(commento):
        # Errore
        app.logger.info('impossibile aggiungere')

    return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

@app.route('/modifica', methods=['POST'])
@login_required
def modifica():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')

    id_commento = request.form.get('id_commento')

    nuovo_contenuto = request.form.get('contenuto')

    if not dao.modifica_commento(id_commento, nuovo_contenuto):
        # Errore
        app.logger.info('impossibile modificare')

    return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

@app.route('/elimina', methods=['POST'])
@login_required
def elimina():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')

    id_commento = request.form.get('id_commento')

    if not dao.cancella_commento(id_commento):
        # Errore
        app.logger.info('impossibile eliminare')

    return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

@app.route('/nuovo-episodio', methods=['POST'])
@login_required
def nuovo_episodio():
    # Id podcast
    id_podcast = request.form.get('id_podcast')
    
    # Numero episodio
    id_episodio = dao.prossimo_id_episodio()

    # Titolo
    titolo = request.form.get('titolo')

    # Descrizione
    descrizione = request.form.get('descrizione')

    # Audio
    audio = request.files['audio']
    if audio:
        extension = os.path.splitext(audio.filename)[-1].lower()

        # static/Audio/<titolo>_<id_podcast>_<id_episodio>.<estensione>
        nome_file = 'Audio/' + titolo + '_' + id_podcast + '_' + str(id_episodio) + extension
        audio.save('static/' + nome_file)
    else:
        # Errore
        return redirect(url_for('podcast', id_podcast=id_podcast))
    
    audio = nome_file

    # Data
    data = request.form.get('data_pubblicazione')

    episodio = {'id_podcast' : id_podcast,
                'titolo' : titolo,
                'descrizione' : descrizione,
                'audio' : audio, 
                'data' : data}
    
    if not dao.aggiungi_episodio(episodio):
        # Errore
        app.logger.info('impossibile aggiungere')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/modifica_episodio', methods=['POST'])
@login_required
def modifica_episodio():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')
    nuovo_titolo = request.form.get('titolo')
    nuova_descrizione = request.form.get('descrizione')

    if not dao.modifica_episodio(id_episodio, nuovo_titolo, nuova_descrizione):
        # Errore
        app.logger.info('impossibile modificare')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/elimina_episodio', methods=['POST'])
@login_required
def elimina_episodio():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')

    if not dao.elimina_episodio(id_episodio):
        # Errore
        app.logger.info('impossibile eliminare')

    return redirect(url_for('podcast', id_podcast=id_podcast))

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

@app.route('/segui', methods=['POST'])
@login_required
def segui():
    id_utente = current_user.get_id()
    id_podcast = request.form.get('id_podcast')

    da_seguire = request.form.get('da_seguire')

    if not dao.segui(id_podcast, id_utente, da_seguire):
        # Errore
        app.logger.info('impossibile seguire/smettere di seguire il podcast')
    
    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html')