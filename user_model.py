from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, tipo_utente, immagine_profilo):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.tipo_utente = tipo_utente
        self.immagine_profilo = immagine_profilo
    
    def get_username(self):
        return self.username