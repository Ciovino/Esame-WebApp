# Esame 23/01/2023 - Introduzione alle Applicazioni Web

## Podcast
Realizzare un'applicazione web per la gestione di podcast.

### Homepage
- Navbar laterale:
  - Nome del sito (*ancora da scegliere*);
  - Pagina di registrazione (**Senza login**);
  - Pagina di login (**Senza login**);
  - Pagina personale (**Con Login**);
  - Link per logout (**Con Login**);
- Aside per la ricerca:
  - Pagina delle categorie:
    - Elenco di tutte le categorie e al click si scoprono tutti i podcast della categoria;
    - Barra di ricerca in alto, per una ricerca più rapida;
  - Pagina dei podcast seguiti (**Con Login**);
  - Pagina dei podcast creati (**Con Login e profilo Creatore**);
- Main, con i podcast:
  - *Podcast recenti*: I 3/4 podcast che hanno l'aggiornamento più recente.
  - *Tutti i podcast*: Tutti i podcast del sito (**da scegliere un ordinamento**);
- Footer, con le icone per i social.

### Registrati
- Form di registrazione contenente:
  - *Username* (**univoco**);
  - *Email* (*univoca*);
  - *Password*;
  - *Tipo* di utente;
  - *Immagine profilo*.
  
### Login
- Form di login contentente:
  - *Username*;
  - *Password*.

### Pagina Personale
- Messaggio di benvenuto;
- Elenco delle informazioni dell'utente:
  - *Username*;
  - *Email*;
  - *Password*;
  - *Tipo* di utente;
  - *Immagine profilo*.

### Pagina dei podcast creati
- Elenco dei podcast (*Se non ci sono podcast, viene visualizzato "Nessun podcast. Creane uno."*);
- Bottone per la creazione di un nuovo podcast:
  - *Titolo*;
  - *Descrizione*;
  - *Immagine*;
  - *Categoria*.

### Pagina del podcast
- *Titolo* e nome dell'*autore*;
- Elenco di episodi;