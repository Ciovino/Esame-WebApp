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

# Recupera le informazioni dell'utente
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

# Recupera tutti i podcast di un utente
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

# Recupea le informazioni di un podcast
def recupera_podcast(id_podcast):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM podcast WHERE id_podcast = ?"

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

# Aggiunge un podcast al dc
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
    query = "INSERT INTO episodi(id_podcast, titolo, descrizione, numero_episodio, data, audio) VALUES (?,?,?,?,?,?)"

    success = False

    try:
        cursor.execute(query, (episodio['id_podcast'], episodio['titolo'], episodio['descrizione'], episodio['numero_episodio'], episodio['data'], episodio['audio']))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def recupera_episodi_podcast(id_podcast):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM episodi WHERE id_podcast = ? ORDER BY data"

    cursor.execute(query, (id_podcast,))

    tutti_episodi = cursor.fetchall()

    cursor.close()
    connection.close()

    return tutti_episodi

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