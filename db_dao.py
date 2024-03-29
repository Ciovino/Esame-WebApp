import sqlite3

db_path = 'database/db_esame.db'

def utente_univoco(username):
    if username == None: # L'username non esiste
        return False

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM utenti WHERE username = ?"

    cursor.execute(query, (username,))
    existing_username = cursor.fetchone()

    cursor.close()
    connection.close()

    if int(existing_username[0]) == 1: # Username già usato
        return False

    return True

def email_univoca(email):
    if email == None: # L'email non esiste
        return False

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM utenti WHERE email = ?"

    cursor.execute(query, (email,))
    existing_email = cursor.fetchone()

    cursor.close()
    connection.close()

    if int(existing_email[0]) == 1: # Email già usata
        return False
        
    return True

def recupera_utente_username(username):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM utenti WHERE id_utente = ?"

    cursor.execute(query, (id,))

    utente = cursor.fetchone()

    cursor.close()
    connection.close()

    return utente

def recupera_podcast_utente(id_utente):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM podcast WHERE id_utente = ? ORDER BY data_creazione, id_podcast DESC"

    cursor.execute(query, (id_utente,))

    tutti_podcast = cursor.fetchall()

    cursor.close()
    connection.close()

    return tutti_podcast

def recupera_podcast_id(id_podcast):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
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

def tutti_podcast():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT p.id_utente, u.username, p.titolo, p.descrizione, p.categoria, p.immagine, p.data_creazione, p.id_podcast
            FROM utenti u, podcast p
            WHERE u.id_utente = p.id_utente
            ORDER BY p.data_creazione DESC, p.id_podcast DESC'''

    cursor.execute(query)

    tutti_podcast = cursor.fetchall()

    cursor.close()
    connection.close()

    dati = [dict(podcast) for podcast in tutti_podcast]

    return dati

def prossimo_id_podcast():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT seq FROM sqlite_sequence WHERE name = 'podcast'"

    cursor.execute(query)

    max_id = cursor.fetchone()

    cursor.close()
    connection.close()

    if max_id[0] == None: # Nessun podcast salvato nel db
        return 1
    else:
        return int(max_id[0]) + 1

def aggiungi_podcast(podcast):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
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

def modifica_podcast(id_podcast, nuovo_titolo, nuova_descrizione, nuova_categoria):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = "UPDATE podcast SET titolo = ?, descrizione = ?, categoria = ? WHERE id_podcast = ?"

    success = False

    try:
        cursor.execute(query, (nuovo_titolo, nuova_descrizione, nuova_categoria, id_podcast))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def elimina_podcast(id_podcast):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = "DELETE FROM podcast WHERE id_podcast = ?"

    success = False

    try:
        cursor.execute(query, (id_podcast, ))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

# Un utente non può avere due podcast con lo stesso titolo
def titolo_podcast_valido(nuovo_titolo:str, id_utente, id_podcast):    
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = '''SELECT titolo FROM podcast WHERE id_utente = ? AND id_podcast != ?'''

    cursor.execute(query, (id_utente, id_podcast))

    tutti_titoli = cursor.fetchall()

    cursor.close()
    connection.close()

    for titolo in tutti_titoli:
        if titolo[0].lower() == nuovo_titolo.lower():
            return False

    return True

def aggiungi_episodio(episodio):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
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

# Un podcast non può avere due episodi con lo stesso nome
def titolo_episodio_valido(nuovo_titolo, id_podcast, id_episodio):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = '''SELECT titolo FROM episodi WHERE id_podcast = ? AND id_episodio != ?'''

    cursor.execute(query, (id_podcast, id_episodio))

    tutti_titoli = cursor.fetchall()

    cursor.close()
    connection.close()

    for titolo in tutti_titoli:
        if titolo[0].lower() == nuovo_titolo.lower():
            return False

    return True

def modifica_episodio(id_episodio, nuovo_titolo, nuova_descrizione, nuova_data):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = "UPDATE episodi SET titolo = ?, descrizione = ?, data = ? WHERE id_episodio = ?"

    success = False

    try:
        cursor.execute(query, (nuovo_titolo, nuova_descrizione, nuova_data, id_episodio))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def elimina_episodio(id_episodio):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()
    query = "DELETE FROM episodi WHERE id_episodio = ?"

    success = False

    try:
        cursor.execute(query, (id_episodio, ))
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
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT seq FROM sqlite_sequence WHERE name = 'episodi'"

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
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM episodi WHERE id_podcast = ? ORDER BY data, id_episodio"

    cursor.execute(query, (id_podcast,))

    tutti_episodi = cursor.fetchall()

    cursor.close()
    connection.close()

    dati = [dict(episodio) for episodio in tutti_episodi]

    return dati

def recupera_episodio_id(id_episodio):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
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
    connection.execute("PRAGMA foreign_keys = 1")
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

def aggiungi_nuovo_utente(user):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
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

def podcast_piu_seguiti():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT p.id_utente, u.username, p.id_podcast, s.totale, p.titolo, p.descrizione, p.categoria, p.immagine, p.data_creazione
            FROM utenti u, podcast p, (SELECT s.id_podcast, COUNT(p.id_podcast) as totale
						                FROM seguiti s, podcast p
						                WHERE s.id_podcast = p.id_podcast
						                GROUP BY p.id_podcast
						                ORDER BY totale DESC) as s
            WHERE u.id_utente = p.id_utente AND p.id_podcast = s.id_podcast
            ORDER BY s.totale DESC
            LIMIT 3'''

    cursor.execute(query)

    piu_seguiti = cursor.fetchall()

    cursor.close()
    connection.close()

    return piu_seguiti

def recupera_seguiti(id_utente):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT s.id_utente, u.username, s.id_podcast, p.titolo, p.descrizione, p.categoria, p.immagine, p.data_creazione
            FROM seguiti s, podcast p, utenti u
            WHERE s.id_utente = ? AND s.id_podcast = p.id_podcast AND u.id_utente = p.id_utente
            ORDER BY p.data_creazione DESC'''

    cursor.execute(query, (id_utente, ))

    podcast_seguiti = cursor.fetchall()

    cursor.close()
    connection.close()

    return podcast_seguiti

def podcast_seguito(id_podcast, id_utente):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''SELECT COUNT(*)
            FROM seguiti
            WHERE id_podcast = ? AND id_utente = ?'''

    cursor.execute(query, (id_podcast, id_utente))

    seguito = cursor.fetchone()

    cursor.close()
    connection.close()

    if int(seguito[0]) == 1:
        return 1

    return 0

def segui(id_podcast, id_utente, da_seguire):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if int(da_seguire) == 0:
        # Smettere di seguire
        query = '''DELETE FROM seguiti WHERE id_podcast = ? AND id_utente = ?'''
    elif int(da_seguire) == 1:
        # Seguire
        query = '''INSERT INTO seguiti(id_podcast, id_utente) VALUES (?,?)'''
    else:
        # Errore
        print(f'Valore (da_seguire):{da_seguire} non valido')
        return False

    success = False

    try:
        cursor.execute(query, (id_podcast, id_utente))
        connection.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success