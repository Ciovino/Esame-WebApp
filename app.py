from flask import Flask, render_template, redirect, request, url_for, flash, abort
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

# Categorie dei podcast
intrattenimento = ['Arte', 'Commedia', 'Narrativa', 'Cinema', 'Letteratura', 'Musica']
business        = ['Economia', 'Tecnologia', 'Finanza', 'Politica']
formazione      = ['Storia', 'Scienza', 'Filosofia']
divertimento    = ['Sport', 'Tennis', 'Calcio', 'Bowling', 'Videogiochi']
benessere       = ['Moda', 'Cibo', 'Fitness']

tutte_categorie = { 'Arte e Intrattenimento' : intrattenimento,
                    'Business e Tecnologia'  : business,
                    'Formazione'             : formazione,
                    'Sport e Divertimento'   : divertimento,
                    'Lifestyle e Benessere'  : benessere }

# Route
@app.route('/')
def homepage():
    piu_seguiti = dao.podcast_piu_seguiti()
    tutti_podcast = dao.tutti_podcast()

    return render_template('homepage.html', 
                        tutti_podcast=tutti_podcast,
                        piu_seguiti=piu_seguiti)

@app.route('/registrati', methods=['GET', 'POST'])
def registrati():
    if request.method == 'GET':
        return render_template('registrati.html')
    else: # POST nuovo utente
        # Nome utente univoco
        username = request.form.get('username')
        if not dao.utente_univoco(username):
            flash('L\'username scelto è già in uso.')
            return redirect(url_for('registrati'))
        
        # Email univoca
        email = request.form.get('email')
        if not dao.email_univoca(email):
            flash('L\'email scelta è già in uso.')
            return redirect(url_for('registrati'))
        
        # Cripta password
        password = generate_password_hash(request.form.get('password'), method='sha256')

        # Ascoltatore o Creatore
        tipo_utente = request.form.get('tipo_utente')
        if tipo_utente == 'Ascoltare':
            tipo_utente = 0
        elif tipo_utente == 'Creare':
            tipo_utente = 1
        else:
            flash('Il tipo utente inserito non è valido.')
            return redirect(url_for('registrati'))
        
        # Immagine profilo
        immagine_profilo = request.files['immagine_profilo']
        if immagine_profilo:
            extension = os.path.splitext(immagine_profilo.filename)[-1].lower()
            nome_file = 'Utenti/' + username + extension

            immagine_profilo.save('static/' + nome_file)
        else:
            nome_file = 'Utenti/_default.png'
        
        immagine_profilo = nome_file

        new_user = {'username': username, 
                    'email': email, 
                    'password': password,
                    'tipo_utente': tipo_utente,
                    'immagine_profilo': immagine_profilo}

        if not dao.aggiungi_nuovo_utente(new_user):
            flash('Impossibile registarsi al momento. Riprova più tardi.')
            return redirect(url_for('registrati'))

        return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else: # POST
        username = request.form.get('username')
        password = request.form.get('password')

        utente_db = dao.recupera_utente_username(username)

        if not utente_db or not check_password_hash(utente_db['password'], password):
            flash('Le credenziali inserite non sono valide.')
            return render_template('login.html')
        else:
            utente = User(id = utente_db['id_utente'],
                        username = utente_db['username'],
                        email = utente_db['username'],
                        password = utente_db['password'],
                        tipo_utente = utente_db['tipo_utente'],
                        immagine_profilo = utente_db['immagine_profilo'])

            login_user(utente)

        return redirect(url_for('homepage'))

@app.route('/categorie')
def categorie():
    return render_template('categorie.html', 
                        tutte_categorie=tutte_categorie)

@app.route('/categorie/<categoria>')
def singola_categoria(categoria):
    tutti_podcast = dao.tutti_podcast()
    podcast_categoria = []

    for podcast in tutti_podcast:
        in_categoria = podcast['categoria'].find(categoria) > -1

        if in_categoria:
            podcast_categoria.append(podcast)

    return render_template('singola_categoria.html',
                        categoria=categoria,
                        podcast_categoria=podcast_categoria,
                        num_podcast = len(podcast_categoria))

@app.route('/profilo')
@login_required
def profilo():
    return render_template('profilo.html')

@app.route('/profilo/seguiti')
@login_required
def seguiti():
    podcast_seguiti = dao.recupera_seguiti(current_user.get_id())

    return render_template('seguiti.html', 
                        num_seguiti=len(podcast_seguiti), 
                        podcast_seguiti=podcast_seguiti)

@app.route('/profilo/tuoi_podcast', methods=['GET', 'POST'])
@login_required
def tuoi_podcast():
    if request.method == 'GET':
        tutti_podcast = dao.recupera_podcast_utente(current_user.get_id())
        num_podcast = len(tutti_podcast)

        return render_template('tuoi_podcast.html',
                            num_podcast=num_podcast, 
                            tutti_podcast=tutti_podcast,
                            tutte_categorie=tutte_categorie)
    else: # POST nuovo podcast
        id_utente = str(current_user.get_id())

        # Titolo
        titolo = request.form.get('titolo')
        if not dao.titolo_podcast_valido(titolo, id_utente, -1):
            flash('Hai già un podcast con quel titolo.')
            return redirect(url_for('tuoi_podcast'))

        # Descrizione
        descrizione = request.form.get('descrizione').strip()
        if descrizione == "":
            flash('Descrizione non valida.')
            return redirect(url_for('tuoi_podcast'))

        # Categoria
        categorie = request.form.getlist('categoria')
        categoria_db = da_lista_a_stringa(categorie)
        if categoria_db == "":
            flash('Seleziona almeno una categoria.')
            return redirect(url_for('tuoi_podcast'))

        # Immagine
        immagine = request.files['immagine']
        if immagine:
            extension = os.path.splitext(immagine.filename)[-1].lower()
            id_podcast = dao.prossimo_id_podcast()

            # static/Podcast/Immagini/<id_utente>_<id_podcast>.<estensione>
            nome_file = 'Podcast/Immagini/' + id_utente + '_' + str(id_podcast) + extension

            immagine.save('static/' + nome_file)
        else:
            flash('Carica un\'immagine per il podcast.')
            return redirect(url_for('tuoi_podcast'))
        
        immagine = nome_file

        # Data di creazione
        data_creazione = datetime.now().strftime('%Y-%m-%d')

        podcast = {'id_utente': id_utente,
                    'titolo' : titolo,
                    'descrizione' : descrizione,
                    'categoria' : categoria_db,
                    'immagine' : immagine,
                    'data_creazione' : data_creazione}

        if not dao.aggiungi_podcast(podcast):
            flash('Impossibile creare un nuovo podcast. Riprova più tardi.')

        return redirect(url_for('tuoi_podcast'))

@app.route('/podcast')
def tutti_podcast():
    tutti_podcast = dao.tutti_podcast()

    return render_template('tutti_podcast.html',
                        tutti_podcast=tutti_podcast)

@app.route('/podcast/<int:id_podcast>')
def podcast(id_podcast):
    podcast_completo = dao.recupera_podcast_id(id_podcast)
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
                            seguito=seguito,
                            tutte_categorie=tutte_categorie)

@app.route('/segui', methods=['POST'])
@login_required
def segui():
    id_utente = current_user.get_id()
    id_podcast = request.form.get('id_podcast')

    da_seguire = request.form.get('da_seguire')

    if not dao.segui(id_podcast, id_utente, da_seguire):
        flash('Impossibile seguire/smettere di seguire il podcast. Riprova più tardi')
    
    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/modifica_podcast', methods=['POST'])
@login_required
def modifica_podcast():
    id_utente = str(current_user.get_id())
    id_podcast = request.form.get('id_podcast')

    nuovo_titolo = request.form.get('titolo')
    if not dao.titolo_podcast_valido(nuovo_titolo, id_utente, id_podcast):
        flash('Hai già un podcast con quel titolo.')
        redirect(url_for('podcast', id_podcast=id_podcast))

    nuova_descrizione = request.form.get('descrizione').strip()
    if nuova_descrizione == "":
        flash('Descrizione non valida.')
        redirect(url_for('podcast', id_podcast=id_podcast))

    nuove_categorie = request.form.getlist('categoria')    
    categoria_db = da_lista_a_stringa(nuove_categorie)
    if categoria_db == "":
        flash('Seleziona almeno una categoria.')
        redirect(url_for('podcast', id_podcast=id_podcast))
    
    nuova_immagine = request.files['immagine']

    if nuova_immagine:
        extension = os.path.splitext(nuova_immagine.filename)[-1].lower()

        # static/Podcast/Immagini/<id_utente>_<id_podcast>.<estensione>
        nome_file = 'Podcast/Immagini/' + id_utente + '_' + id_podcast + extension

        nuova_immagine.save('static/' + nome_file)    

    if not dao.modifica_podcast(id_podcast, nuovo_titolo, nuova_descrizione, categoria_db):
        flash('Impossibile modificare il podcast al momento.')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/elimina_podcast', methods=['POST'])
@login_required
def elimina_podcast():
    id_podcast = request.form.get('id_podcast')

    if not dao.elimina_podcast(id_podcast):
        flash('Impossibile eliminare il podcast al momento')

    return redirect(url_for('tuoi_podcast'))

@app.route('/podcast/<int:id_podcast>/<int:id_episodio>')
@login_required
def episodio(id_podcast, id_episodio):
    podcast = dao.recupera_podcast_id(id_podcast)

    episodio = dao.recupera_episodio_id(id_episodio)
    # Se l'episodio non è pubblico, solo il creatore del podcast può ascoltare l'episodio
    privato = episodio['data'] > datetime.now().strftime('%Y-%m-%d')
    if privato:
        if current_user.get_id() != podcast['id_utente']:
            abort(403)
        
        episodio_precedente = None
        episodio_successivo = None
    else:
        episodio_precedente = dao.episodio_precedente(id_podcast, id_episodio, episodio['data'])
        episodio_successivo = dao.episodio_successivo(id_podcast, id_episodio, episodio['data'], datetime.now().strftime('%Y-%m-%d'))

    commenti = dao.commenti_episodio(id_episodio)

    for commento in commenti:
        commento['data'] = datetime.strptime(episodio['data'], '%Y-%m-%d').strftime('%d %b %Y')

    return render_template('episodio.html',
                            podcast = podcast,
                            episodio = episodio,
                            privato = privato,
                            episodio_precedente=episodio_precedente,
                            episodio_successivo=episodio_successivo,
                            num_commenti = len(commenti),
                            commenti = commenti)

@app.route('/nuovo-episodio', methods=['POST'])
@login_required
def nuovo_episodio():
    # Id podcast
    id_podcast = request.form.get('id_podcast')
    
    # Numero episodio
    id_episodio = dao.prossimo_id_episodio()

    # Titolo
    titolo = request.form.get('titolo')
    if dao.titolo_episodio_valido(titolo, id_podcast, id_episodio):
        flash('Hai già un episodio con quel titolo.')
        return redirect(url_for('podcast', id_podcast=id_podcast))

    # Descrizione
    descrizione = request.form.get('descrizione').strip()
    if descrizione == "":
        flash('La descrizione non è valida.')
        return redirect(url_for('podcast', id_podcast=id_podcast))

    # Audio
    audio = request.files['audio']
    if audio:
        extension = os.path.splitext(audio.filename)[-1].lower()

        # static/Podcast/Audio/<id_podcast>_<id_episodio>.<estensione>
        nome_file = 'Podcast/Audio/' + id_podcast + '_' + str(id_episodio) + extension
        audio.save('static/' + nome_file)
    else:
        flash('Carica un file audio.')
        return redirect(url_for('podcast', id_podcast=id_podcast))
    
    audio = nome_file

    # Data
    data = request.form.get('data_pubblicazione')
    if data > datetime.now().strftime('%Y-%m-%d'):
        flash('La data inserita non è valida.')
        return redirect(url_for('podcast', id_podcast=id_podcast))

    episodio = {'id_podcast' : id_podcast,
                'titolo' : titolo,
                'descrizione' : descrizione,
                'audio' : audio, 
                'data' : data}
    
    if not dao.aggiungi_episodio(episodio):
        flash('Impossibile aggiungere un episodio al momento.')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/modifica_episodio', methods=['POST'])
@login_required
def modifica_episodio():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')
    
    nuovo_titolo = request.form.get('titolo')
    if dao.titolo_episodio_valido(nuovo_titolo, id_podcast, id_episodio):
        flash('Hai già un episodio con quel titolo.')
        return redirect(url_for('podcast', id_podcast=id_podcast))

    nuova_descrizione = request.form.get('descrizione').strip()
    if nuova_descrizione == "":
        flash('La descrizione non è valida.')
        return redirect(url_for('podcast', id_podcast=id_podcast))

    nuovo_audio = request.files['audio']
    if nuovo_audio:
        extension = os.path.splitext(nuovo_audio.filename)[-1].lower()

        # static/Podcast/Audio/<id_podcast>_<id_episodio>.<estensione>
        nome_file = 'Podcast/Audio/' + id_podcast + '_' + str(id_episodio) + extension
        nuovo_audio.save('static/' + nome_file)

    nuova_data = request.form.get('data_pubblicazione')
    if nuova_data > datetime.now().strftime('%Y-%m-%d'):
        flash('La data inserita non è valida.')
        return redirect(url_for('podcast', id_podcast=id_podcast))

    if not dao.modifica_episodio(id_episodio, nuovo_titolo, nuova_descrizione, nuova_data):
        flash('Impossibile modificare l\'episodio.')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/elimina_episodio', methods=['POST'])
@login_required
def elimina_episodio():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')

    if not dao.elimina_episodio(id_episodio):
        flash('Impossibile eliminare l\'episodio al momento.')

    return redirect(url_for('podcast', id_podcast=id_podcast))

@app.route('/nuovo-commento', methods=['POST'])
@login_required
def nuovo_commento():
    # Id podcast
    id_podcast = request.form.get('id_podcast')

    # Id_utente
    id_utente = str(current_user.get_id())

    # Id episodio
    id_episodio = request.form.get('id_episodio')

    # Contenuto 
    contenuto = request.form.get('contenuto').strip()
    if contenuto == "":
        flash('Il commento inserito non è valido.')
        return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

    # Data
    data = datetime.now().strftime('%Y-%m-%d')

    commento = { 'id_utente' : id_utente,
                'id_episodio' : id_episodio,
                'contenuto': contenuto,
                'data' : data}

    if not dao.aggiungi_commento(commento):
        flash('Impossibile commentare al momento. Riprova più tardi.')

    return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

@app.route('/modifica_commento', methods=['POST'])
@login_required
def modifica_commento():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')

    id_commento = request.form.get('id_commento')

    nuovo_contenuto = request.form.get('contenuto').strip()
    if nuovo_contenuto == "":
        flash('Il commento inserito non è valido.')
        return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

    if not dao.modifica_commento(id_commento, nuovo_contenuto):
        flash('Impossibile modificare il commento al momento.')

    return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

@app.route('/elimina_commento', methods=['POST'])
@login_required
def elimina_commento():
    id_podcast = request.form.get('id_podcast')
    id_episodio = request.form.get('id_episodio')

    id_commento = request.form.get('id_commento')

    if not dao.cancella_commento(id_commento):
        flash('Impossibile eliminare il commento al momento.')

    return redirect(url_for('episodio', id_podcast=id_podcast, id_episodio=id_episodio))

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html')

@app.errorhandler(403)
def forbidden(e):
    return render_template('error403.html')

# Funzioni
def da_lista_a_stringa(lista:list):
    if not lista or len(lista) == 0:
        return ""
    
    stringa = lista[0]

    for i in range(1, len(lista)):
        stringa = stringa + '_' + lista[i]

    return stringa