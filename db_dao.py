import sqlite3

# Controlla che l'username sia univoco all'interno del database
def utente_univoco(username):
    # L'username non esiste
    if username == None:
        return False

    connection = sqlite3.connect('database/db_esame.db')
    cursor = connection.cursor()
    query = '''SELECT COUNT(*) FROM utenti WHERE username = ?'''

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

    connection = sqlite3.connect('database/db_esame.db')
    cursor = connection.cursor()
    query = '''SELECT COUNT(*) FROM utenti WHERE email = ?'''

    cursor.execute(query, (email,))
    existing_email = cursor.fetchone()

    if int(existing_email[0]) == 1:
        # email già usata
        return False
        
    return True

# Aggiungi nuovo utente al db
def aggiungi_nuovo_utente(user):
    connection = sqlite3.connect('database/db_esame.db')
    cursor = connection.cursor()
    query = '''INSERT INTO utenti(username, email, password, tipo_utente, immagine_profilo) VALUES (?,?,?,?,?)'''

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