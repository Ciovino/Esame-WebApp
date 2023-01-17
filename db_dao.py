import sqlite3

db_path = 'database/db_esame.db'

# Controlla che l'username sia univoco all'interno del database
def utente_univoco(username):
    # L'username non esiste
    if username == None:
        return False

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM utenti WHERE username = ?"

    cursor.execute(query, (username,))
    existing_username = cursor.fetchone()

    if int(existing_username[0]) == 1:
        # username già usato
        return False

    return True

# Controlla che l'email sia univoca all'interno del database
def email_univoca(email):
    # L'email non esiste
    if email == None:
        return False

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM utenti WHERE email = ?"

    cursor.execute(query, (email,))
    existing_email = cursor.fetchone()

    if int(existing_email[0]) == 1:
        # email già usata
        return False
        
    return True

# Recupera l'utente dall'username
def recupera_utente_username(username):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM utenti WHERE username = ?"

    cursor.execute(query, (username,))

    utente = cursor.fetchone()

    cursor.close()
    connection.close()

    return utente

# Recupera l'utente dall'id
def recupera_utente_id(id):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM utenti WHERE id_utente = ?"

    cursor.execute(query, (id,))

    utente = cursor.fetchone()

    cursor.close()
    connection.close()

    return utente

# Recupera i podcast creati da un utente
def recupera_podcast_utente(id_utente):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM podcast WHERE id_utente = ?"

    cursor.execute(query, (id_utente,))

    tutti_podcast = cursor.fetchall()

    cursor.close()
    connection.close()

    return tutti_podcast

# Recupera un podcast dall'id
def recupera_podcast(id_podcast):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT p.id_utente, u.username, p.titolo, p.descrizione, p.categoria, p.immagine, p.data_creazione, p.id_podcast 
            FROM podcast p, utenti u
            WHERE id_podcast = ? and u.id_utente = p.id_utente'''

    cursor.execute(query, (id_podcast,))

    podcast = cursor.fetchone()

    cursor.close()
    connection.close()

    return dict(podcast)

# Recupera le informazioni di tutti i podcast
def tutti_podcast():
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT p.id_utente, u.username, p.titolo, p.descrizione, p.categoria, p.immagine, p.data_creazione, p.id_podcast
            FROM utenti u, podcast p
            WHERE u.id_utente = p.id_utente
            ORDER BY p.data_creazione DESC'''

    cursor.execute(query)

    tutti_podcast = cursor.fetchall()

    cursor.close()
    connection.close()

    dati = [dict(podcast) for podcast in tutti_podcast]

    return dati

# Aggiunge un podcast al db
def aggiungi_podcast(podcast):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "INSERT INTO podcast(id_utente, titolo, descrizione, categoria, immagine, data_creazione) VALUES (?,?,?,?,?,?)"

    success = False

    try:
        cursor.execute(query, (podcast['id_utente'], podcast['titolo'], podcast['descrizione'], podcast['categoria'], podcast['immagine'], podcast['data_creazione']))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

# Controlla che il titolo per il podcast sia valido
def titolo_podcast_valido(titolo, id_utente):
    # Un utente non può avere due podcast con lo stesso titolo
    return True

# Aggiungi episodio al db
def aggiungi_episodio(episodio):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "INSERT INTO episodi(id_podcast, titolo, descrizione, data, audio) VALUES (?,?,?,?,?)"

    success = False

    try:
        cursor.execute(query, (episodio['id_podcast'], episodio['titolo'], episodio['descrizione'], episodio['data'], episodio['audio']))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def prossimo_id_episodio():
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT MAX(id_episodio) FROM episodi"

    cursor.execute(query)

    max_id = cursor.fetchone()

    cursor.close()
    connection.close()

    if max_id[0] == None: # Nessun episodio salvato nel db
        return 1
    else:
        return int(max_id[0]) + 1

def recupera_episodi_podcast(id_podcast):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM episodi WHERE id_podcast = ? ORDER BY data, id_episodio"

    cursor.execute(query, (id_podcast,))

    tutti_episodi = cursor.fetchall()

    cursor.close()
    connection.close()

    dati = [dict(episodio) for episodio in tutti_episodi]

    return dati

def recupera_episodio(id_episodio):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM episodi WHERE id_episodio = ?"

    cursor.execute(query, (id_episodio,))

    episodio = cursor.fetchone()

    cursor.close()
    connection.close()

    return dict(episodio)

def episodio_successivo(id_podcast, id_episodio, data, data_oggi):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT * 
            FROM episodi 
            WHERE id_podcast = ? AND ((id_episodio < ? AND data > ?) OR (data >= ? AND id_episodio > ?)) AND data <= ?
            ORDER BY data, id_episodio
            LIMIT 1'''

    cursor.execute(query, (id_podcast, id_episodio, data, data, id_episodio, data_oggi))

    episodio = cursor.fetchone()

    cursor.close()
    connection.close()

    if episodio == None:
        return None

    return dict(episodio)

def episodio_precedente(id_podcast, id_episodio, data):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT * 
            FROM episodi 
            WHERE id_podcast = ? AND ((id_episodio < ? AND data <= ?) OR (data < ? AND id_episodio > ?))
            ORDER BY data, id_episodio DESC
            LIMIT 1'''

    cursor.execute(query, (id_podcast, id_episodio, data, data, id_episodio))

    episodio = cursor.fetchone()

    cursor.close()
    connection.close()

    if episodio == None:
        return None

    return dict(episodio)

def aggiungi_commento(commento):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "INSERT INTO commenti(id_utente, id_episodio, contenuto, data) VALUES (?,?,?,?)"

    success = False

    try:
        cursor.execute(query, (commento['id_utente'], commento['id_episodio'], commento['contenuto'], commento['data']))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def modifica_commento(id_commento, nuovo_contenuto):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "UPDATE commenti SET contenuto = ? WHERE id_commento = ?"

    success = False

    try:
        cursor.execute(query, (nuovo_contenuto, id_commento))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def cancella_commento(id_commento):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "DELETE FROM commenti WHERE id_commento = ?"

    success = False

    try:
        cursor.execute(query, (id_commento, ))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def commenti_episodio(id_episodio):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT c.id_utente, c.id_episodio, c.contenuto, c.data, c.id_commento, u.username, u.immagine_profilo
            FROM commenti c, utenti u
            WHERE c.id_episodio = ? AND c.id_utente = u.id_utente
            ORDER BY c.data'''

    cursor.execute(query, (id_episodio,))

    commenti = cursor.fetchall()

    cursor.close()
    connection.close()

    dati = [dict(commento) for commento in commenti]

    return dati

# Aggiungi nuovo utente al db
def aggiungi_nuovo_utente(user):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "INSERT INTO utenti(username, email, password, tipo_utente, immagine_profilo) VALUES (?,?,?,?,?)"

    success = False

    try:
        cursor.execute(query, (user['username'], user['email'], user['password'], user['tipo_utente'], user['immagine_profilo']))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success